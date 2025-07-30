from typing import Any

import stripe
from core.config import get_settings
from models.service_plan import ServicePlan
from models.service_tax import ServiceTax


class StripeService:
    def __init__(self):
        settings = get_settings()
        stripe.enable_telemetry = False
        stripe.api_key = settings.stripe_secret_key

    async def create_customer(self, email: str, name: str | None = None, metadata: dict[str, str] | None = None, address: dict[str, str] | None = None) -> stripe.Customer:
        customer_data = {
            "email": email,
            "metadata": metadata or {},
            "preferred_locales": ["fr"],
        }

        if name:
            customer_data["name"] = name

        if address:
            customer_data["address"] = address

        return stripe.Customer.create(**customer_data)

    async def update_customer(self, customer_id: str, email: str, name: str | None = None, metadata: dict[str, str] | None = None, address: dict[str, str] | None = None) -> stripe.Customer:
        customer_data = {
            "email": email,
            "metadata": metadata or {},
            "preferred_locales": ["fr"],
        }

        if name:
            customer_data["name"] = name

        if address:
            customer_data["address"] = address

        return stripe.Customer.modify(customer_id, **customer_data)

    async def create_subscription(
        self, 
        customer_id: str, 
        price_id: str,
        quantity: int = 1,
        tax_rates: list | None = None,
        metadata: dict[str, str] | None = None,
        trial_period_days: int | None = None
    ) -> stripe.Subscription:
        subscription_data: dict[str, Any] = {
            "customer": customer_id,
            "items": [{"price": price_id, "quantity": quantity}],
            "payment_behavior": "default_incomplete",
            "payment_settings": {"save_default_payment_method": "on_subscription"},
            "expand": ["latest_invoice.payment_intent"],
            "metadata": metadata or {}
        }

        if tax_rates:
            subscription_data["default_tax_rates"] = tax_rates

        if trial_period_days:
            subscription_data["trial_period_days"] = trial_period_days

        return stripe.Subscription.create(**subscription_data)

    async def update_subscription(
        self, 
        subscription_id: str, 
        price_id: str | None = None,
        quantity: int | None = None,
        tax_rates: list | None = None,
        metadata: dict[str, str] | None = None
    ) -> stripe.Subscription:
        update_data = {}

        if price_id:
            subscription = stripe.Subscription.retrieve(subscription_id)
            item_data = {
                "id": subscription["items"]["data"][0]["id"],
                "price": price_id
            }

            if quantity is not None:
                item_data["quantity"] = quantity

            update_data["items"] = [item_data]

        if tax_rates is not None:
            update_data["default_tax_rates"] = tax_rates

        if metadata:
            update_data["metadata"] = metadata

        return stripe.Subscription.modify(subscription_id, **update_data)

    async def cancel_subscription(self, subscription_id: str, at_period_end: bool = True) -> stripe.Subscription:
        if at_period_end:
            return stripe.Subscription.modify(subscription_id, cancel_at_period_end=True)
        else:
            return stripe.Subscription.cancel(subscription_id)

    async def get_subscription(self, subscription_id: str) -> stripe.Subscription:
        return stripe.Subscription.retrieve(subscription_id)

    async def list_customer_subscriptions(self, customer_id: str) -> stripe.ListObject:
        return stripe.Subscription.list(customer=customer_id)

    async def create_billing_portal_session(self, customer_id: str, return_url: str) -> stripe.billing_portal.Session:
        return stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url
        )

    async def get_upcoming_invoice(self, customer_id: str):
        return stripe.Invoice.upcoming(customer=customer_id)

    async def list_customer_invoices(self, customer_id: str, limit: int = 10) -> stripe.ListObject:
        return stripe.Invoice.list(
            customer=customer_id,
            limit=limit,
            status='paid'
        )

    async def list_payment_methods(self, customer_id: str) -> stripe.ListObject:
        return stripe.PaymentMethod.list(
            customer=customer_id,
            type='card'
        )

    async def create_setup_intent(self, customer_id: str) -> stripe.SetupIntent:
        return stripe.SetupIntent.create(
            customer=customer_id,
            payment_method_types=['card'],
            usage='off_session',
            confirm=False
        )

    async def detach_payment_method(self, payment_method_id: str) -> stripe.PaymentMethod:
        return stripe.PaymentMethod.detach(payment_method_id)

    async def sync_workspace_plan_to_stripe(self, service_plan: ServicePlan) -> dict[str, str]:
        if not service_plan.name or not service_plan.type or not service_plan.period:
            raise ValueError("Le plan doit avoir un nom, un type et une période")

        if not service_plan.price or not service_plan.currency:
            raise ValueError("Le plan doit avoir un prix et une devise")

        # Create or update the Stripe product
        if service_plan.stripe_product_id:
            product = stripe.Product.modify(
                service_plan.stripe_product_id,
                name=service_plan.name,
                description=service_plan.description or "",
                metadata={
                    "workspace_plan_id": str(service_plan.id),
                    "type": service_plan.type.value,
                    "period": service_plan.period.value
                }
            )
        else:
            product = stripe.Product.create(
                name=service_plan.name,
                description=service_plan.description or "",
                metadata={
                    "workspace_plan_id": str(service_plan.id),
                    "type": service_plan.type.value,
                    "period": service_plan.period.value
                }
            )

        # Create tiered pricing structure - always create a new price
        # Create new price with tiered structure
        price = stripe.Price.create(
            product=product.id,
            currency=service_plan.currency.lower(),
            recurring={
                "interval": "month" if service_plan.period.value == "Mensuel" else "year"
            },
            billing_scheme="tiered",
            tiers_mode="volume",
            tiers=[
                {
                    "up_to": 1,
                    "unit_amount": int(service_plan.price * 100)  # Price for quantity 1
                },
                {
                    "up_to": "inf",
                    "unit_amount": int(service_plan.price * 100)  # Same price for quantity 2+
                }
            ],
            metadata={
                "workspace_plan_id": str(service_plan.id)
            }
        )

        # Set the new price as default for the product
        stripe.Product.modify(
            product.id,
            default_price=price.id
        )

        return {
            "product_id": product.id,
            "price_id": price.id
        }

    async def sync_tax_rate_to_stripe(self, tax: ServiceTax) -> str:
        if not tax.name or not tax.rate:
            raise ValueError("La taxe doit avoir un nom et un taux")

        if tax.stripe_id:
            return tax.stripe_id
        else:
            tax_rate_data = {
                "display_name": tax.name,
                "percentage": float(tax.rate),
                "inclusive": False,
                "metadata": {
                    "tax_id": str(tax.id)
                }
            }

            if tax.country_code:
                tax_rate_data["country"] = tax.country_code

            if tax.description:
                tax_rate_data["description"] = tax.description

            tax_rate = stripe.TaxRate.create(**tax_rate_data)

            return tax_rate.id


stripe_service = StripeService() 
