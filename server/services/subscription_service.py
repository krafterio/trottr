from datetime import datetime, timedelta, timezone
from uuid import uuid4

import stripe

from core.config import get_settings
from models.workspace import Workspace
from models.service_plan import ServicePlan
from models.workspace_subscription import WorkspaceSubscription, SubscriptionStatus
from models.service_tax import ServiceTax
from services.stripe_service import stripe_service


class SubscriptionService:
    async def create_or_update_subscription(
        self,
        workspace: Workspace,
        update_customer: bool = True
    ) -> WorkspaceSubscription:
        settings = get_settings()

        subscription = await self.get_active_subscription(workspace)

        if not subscription:
            user_count = await workspace.workspace_users.query.filter(workspace=workspace).count()
            subscription = await self.create_subscription(workspace, workspace.service_plan, user_count)

        elif settings.subscription_stripe_enabled:
            owner = await workspace.get_owner()

            if not owner:
                raise ValueError("Le workspace doit avoir un propriétaire")

            if workspace.stripe_customer_id and workspace.stripe_customer_id.startswith('gen_'):
                stripe_customer = await stripe_service.create_customer(
                    email=owner.email,
                    name=workspace.name,
                    metadata={
                        "workspace_id": str(workspace.id),
                    },
                    address={
                        "line1": workspace.street,
                        "line2": workspace.street2,
                        "city": workspace.city,
                        "state": workspace.zip,
                        "country": workspace.country.iso_code if workspace.country else 'FR',
                    }
                )
                workspace.stripe_customer_id = stripe_customer.id
                await workspace.save()

                subscription.stripe_customer_id = stripe_customer.id
                await subscription.save()
            elif workspace.stripe_customer_id and update_customer:
                await stripe_service.update_customer(
                    customer_id=workspace.stripe_customer_id,
                    email=owner.email,
                    name=workspace.name,
                    metadata={
                        "workspace_id": str(workspace.id),
                    },
                    address={
                        "line1": workspace.street,
                        "line2": workspace.street2,
                        "city": workspace.city,
                        "state": workspace.zip,
                        "country": workspace.country.iso_code if workspace.country else 'FR',
                    }
                )

            if subscription.stripe_subscription_id.startswith('gen_'):
                trial_period_days = None
                if subscription.trial_end:
                    trial_period_days = (subscription.trial_end - datetime.now(timezone.utc)).days

                tax_rates = await ServiceTax.query.filter(country_code='FR').all()
                stripe_tax_rates = []

                if tax_rates:
                    for tax in tax_rates:
                        if not tax.stripe_id and settings.subscription_stripe_enabled:
                            stripe_tax_id = await stripe_service.sync_tax_rate_to_stripe(tax)
                            tax.stripe_id = stripe_tax_id
                            await tax.save()

                        stripe_tax_rates.append(tax.stripe_id)

                stripe_subscription = await stripe_service.create_subscription(
                    customer_id=workspace.stripe_customer_id,
                    price_id=subscription.service_plan.stripe_price_id,
                    quantity=subscription.available_users_count,
                    tax_rates=stripe_tax_rates,
                    trial_period_days=trial_period_days,
                    metadata={
                        "workspace_id": str(workspace.id),
                        "workspace_plan_id": str(subscription.service_plan.id)
                    }
                )

                subscription.stripe_subscription_id = stripe_subscription.id
                await subscription.save()

        return subscription

    async def create_subscription(
        self,
        workspace: Workspace,
        service_plan: ServicePlan,
        quantity: int = 1,
    ) -> WorkspaceSubscription:
        settings = get_settings()

        if not workspace.stripe_customer_id:
            owner = await workspace.get_owner()

            if not owner:
                raise ValueError("Le workspace doit avoir un propriétaire")

            if settings.subscription_stripe_enabled:
                stripe_customer = await stripe_service.create_customer(
                    email=owner.email,
                    name=workspace.name,
                    metadata={
                        "workspace_id": str(workspace.id),
                    },
                    address={
                        "line1": workspace.street,
                        "line2": workspace.street2,
                        "city": workspace.city,
                        "state": workspace.zip,
                        "country": workspace.country.iso_code if workspace.country else 'FR',
                    }
                )
                workspace.stripe_customer_id = stripe_customer.id
            else:
                workspace.stripe_customer_id = 'gen_' + str(uuid4())

            await workspace.save()

        trial_period_days = 14
        tax_rates = await ServiceTax.query.filter(country_code='FR').all()
        stripe_tax_rates = []

        if tax_rates:
            for tax in tax_rates:
                if not tax.stripe_id and settings.subscription_stripe_enabled:
                    stripe_tax_id = await stripe_service.sync_tax_rate_to_stripe(tax)
                    tax.stripe_id = stripe_tax_id
                    await tax.save()

                stripe_tax_rates.append(tax.stripe_id)

        if not service_plan.stripe_price_id and settings.subscription_stripe_enabled:
            stripe_ids = await stripe_service.sync_workspace_plan_to_stripe(service_plan)
            service_plan.stripe_product_id = stripe_ids["product_id"]
            service_plan.stripe_price_id = stripe_ids["price_id"]
            await service_plan.save()

        if settings.subscription_stripe_enabled:
            stripe_subscription = await stripe_service.create_subscription(
                customer_id=workspace.stripe_customer_id,
                price_id=service_plan.stripe_price_id,
                quantity=quantity,
                tax_rates=stripe_tax_rates,
                trial_period_days=trial_period_days,
                metadata={
                    "workspace_id": str(workspace.id),
                    "workspace_plan_id": str(service_plan.id)
                }
            )

            subscription = WorkspaceSubscription(
                workspace=workspace,
                service_plan=service_plan,
                stripe_subscription_id=stripe_subscription.id,
                stripe_customer_id=workspace.stripe_customer_id,
                status=SubscriptionStatus(stripe_subscription.status),
                available_users_count=quantity,
                start_date=datetime.fromtimestamp(stripe_subscription.start_date).astimezone() if stripe_subscription.start_date else None,
                end_date=datetime.fromtimestamp(stripe_subscription.ended_at).astimezone() if stripe_subscription.ended_at else None,
                trial_start=datetime.fromtimestamp(stripe_subscription.trial_start).astimezone() if stripe_subscription.trial_start else None,
                trial_end=datetime.fromtimestamp(stripe_subscription.trial_end).astimezone() if stripe_subscription.trial_end else None,
                cancel_at_period_end=stripe_subscription.cancel_at_period_end,
            )
        else:
            subscription = WorkspaceSubscription(
                workspace=workspace,
                service_plan=service_plan,
                stripe_subscription_id='gen_' + str(uuid4()),
                stripe_customer_id=workspace.stripe_customer_id,
                status=SubscriptionStatus.active,
                available_users_count=quantity,
                start_date=datetime.now().astimezone(),
                end_date=None,
                trial_start=datetime.now().astimezone(),
                trial_end=datetime.now().astimezone() + timedelta(days=trial_period_days),
                cancel_at_period_end=False,
            )

        await subscription.save()

        return subscription

    async def update_subscription_plan(
        self, 
        subscription: WorkspaceSubscription, 
        new_plan: ServicePlan,
        quantity: int | None = None
    ) -> WorkspaceSubscription:
        settings = get_settings()

        if not subscription.stripe_subscription_id:
            raise ValueError("L'abonnement n'a pas d'ID Stripe")

        if not new_plan.stripe_price_id and settings.subscription_stripe_enabled:
            stripe_ids = await stripe_service.sync_workspace_plan_to_stripe(new_plan)
            new_plan.stripe_product_id = stripe_ids["product_id"]
            new_plan.stripe_price_id = stripe_ids["price_id"]
            await new_plan.save()

        if settings.subscription_stripe_enabled:
            stripe_subscription = await stripe_service.update_subscription(
                subscription_id=subscription.stripe_subscription_id,
                price_id=new_plan.stripe_price_id,
                quantity=quantity,
                metadata={
                    "workspace_id": str(subscription.workspace.id),
                    "workspace_plan_id": str(new_plan.id)
                }
            )
            subscription.status = SubscriptionStatus(stripe_subscription.status)
            subscription.start_date = datetime.fromtimestamp(stripe_subscription.start_date).astimezone() if stripe_subscription.start_date else None
            subscription.end_date = datetime.fromtimestamp(stripe_subscription.ended_at).astimezone() if stripe_subscription.ended_at else None

        subscription.service_plan = new_plan

        if quantity is not None:
            subscription.available_users_count = quantity

        await subscription.save()

        return subscription

    async def cancel_subscription(
        self, 
        subscription: WorkspaceSubscription, 
        at_period_end: bool = True
    ) -> WorkspaceSubscription:
        settings = get_settings()

        if not subscription.stripe_subscription_id:
            raise ValueError("L'abonnement n'a pas d'ID Stripe")

        if settings.subscription_stripe_enabled:
            stripe_subscription = await stripe_service.cancel_subscription(
                subscription_id=subscription.stripe_subscription_id,
                at_period_end=at_period_end,
            )

            subscription.status = SubscriptionStatus(stripe_subscription.status)
            subscription.cancel_at_period_end = stripe_subscription.cancel_at_period_end

            if stripe_subscription.canceled_at:
                subscription.canceled_at = datetime.fromtimestamp(stripe_subscription.canceled_at).astimezone()
        else:
            subscription.status = SubscriptionStatus.canceled
            subscription.canceled_at = datetime.now().astimezone()

        await subscription.save()

        return subscription

    async def sync_subscription_from_stripe(self, stripe_subscription_id: str) -> WorkspaceSubscription:
        stripe_subscription = await stripe_service.get_subscription(stripe_subscription_id)

        subscription = await WorkspaceSubscription.query.filter(
            stripe_subscription_id=stripe_subscription_id
        ).first()

        if not subscription:
            raise ValueError(f"Abonnement {stripe_subscription_id} non trouvé")

        subscription.status = SubscriptionStatus(stripe_subscription.status)
        subscription.start_date = datetime.fromtimestamp(stripe_subscription.start_date).astimezone() if stripe_subscription.start_date else None
        subscription.end_date = datetime.fromtimestamp(stripe_subscription.ended_at).astimezone() if stripe_subscription.ended_at else None
        subscription.cancel_at_period_end = stripe_subscription.cancel_at_period_end

        price_id = None
        available_users_count = 0
        for item in stripe_subscription['items']:
            price_id = item.plan['id']
            available_users_count += item.quantity
        subscription.available_users_count = available_users_count

        if price_id:
            service_plan = await ServicePlan.query.filter(
                stripe_price_id=price_id,
            ).first()

            if service_plan:
                subscription.service_plan = service_plan

        if stripe_subscription.trial_start:
            subscription.trial_start = datetime.fromtimestamp(stripe_subscription.trial_start).astimezone()

        if stripe_subscription.trial_end:
            subscription.trial_end = datetime.fromtimestamp(stripe_subscription.trial_end).astimezone()

        if stripe_subscription.canceled_at:
            subscription.canceled_at = datetime.fromtimestamp(stripe_subscription.canceled_at).astimezone()

        await subscription.save()

        return subscription

    async def get_last_subscription(self, workspace: Workspace) -> WorkspaceSubscription | None:
        return await WorkspaceSubscription.query.filter(
            workspace=workspace,
        ).order_by('-created_at').first()

    async def get_active_subscription(self, workspace: Workspace) -> WorkspaceSubscription | None:
        return await WorkspaceSubscription.query.filter(
            workspace=workspace,
            status__in=[SubscriptionStatus.active, SubscriptionStatus.trialing],
            is_active=True
        ).first()

    async def create_billing_portal_session(
        self, 
        workspace: Workspace, 
        return_url: str
    ) -> stripe.billing_portal.Session:
        settings = get_settings()

        if not workspace.stripe_customer_id or not settings.subscription_stripe_enabled:
            raise ValueError("Le workspace n'a pas d'ID client Stripe")

        return await stripe_service.create_billing_portal_session(
            customer_id=workspace.stripe_customer_id,
            return_url=return_url,
        )

    async def get_workspace_invoices(self, workspace: Workspace, limit: int = 10) -> list[dict]:
        settings = get_settings()

        if not workspace.stripe_customer_id or not settings.subscription_stripe_enabled:
            return []

        try:
            stripe_invoices = await stripe_service.list_customer_invoices(
                customer_id=workspace.stripe_customer_id,
                limit=limit
            )

            invoices = []
            for invoice in stripe_invoices.data:
                invoices.append({
                    'id': invoice.id,
                    'amount_paid': invoice.amount_paid / 100,
                    'currency': invoice.currency.upper(),
                    'status': invoice.status,
                    'created': invoice.created,
                    'invoice_pdf': invoice.invoice_pdf,
                    'hosted_invoice_url': invoice.hosted_invoice_url,
                    'number': invoice.number,
                    'period_start': invoice.period_start,
                    'period_end': invoice.period_end,
                })

            return invoices
        except Exception as e:
            print(f"Erreur lors de la récupération des factures: {e}")
            return []


subscription_service = SubscriptionService() 
