import { createRouter, createWebHistory } from 'vue-router'
import { bus } from "@/common/composables/bus";

const isPreviewMode = import.meta.env.VITE_MODE_PREVIEW === 'True';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL + 'admin'),
    routes: [
        {
            path: '/',
            redirect: '/home'
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('@/common/views/auth/LoginView.vue'),
            meta: {
                metaTitle: 'Connexion - Smashr',
                title: 'Connexion',
            },
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('@/common/views/auth/RegisterView.vue'),
            meta: {
                metaTitle: 'Inscription - Smashr',
                title: 'Inscription'
            }
        },
        {
            path: '/verify-code',
            name: 'verify-code',
            component: () => import('@/common/views/auth/VerifyCodeView.vue'),
            meta: {
                metaTitle: 'Vérification - Smashr',
                title: 'Vérification'
            }
        },
        {
            path: '/home',
            name: 'home',
            component: () => import('@/admin/views/HomeView.vue'),
        },
        {
            path: '/workspaces',
            name: 'workspaces',
            component: () => import('@/admin/views/WorkspacesView.vue'),
            meta: {
                metaTitle: 'Espaces de travail - Admin - Smashr',
                title: 'Espaces de travail',
            }
        },
        {
            path: '/workspaces/:id',
            name: 'workspace',
            component: () => import('@/admin/views/WorkspaceView.vue'),
            meta: {
                metaTitle: 'Détails de l\'espace de travail - Admin - Smashr',
                title: 'Détails de l\'espace de travail',
            }
        },
        {
            path: '/service-plans',
            name: 'service-plans',
            component: () => import('@/admin/views/ServicePlansView.vue'),
            meta: {
                metaTitle: 'Plans - Admin - Smashr',
                title: 'Plans',
            }
        },
        {
            path: '/service-credit-packs',
            name: 'service-credit-packs',
            component: () => import('@/admin/views/ServiceCreditPacksView.vue'),
            meta: {
                metaTitle: 'Packs d\'enrichissement - Admin - Smashr',
                title: 'Packs d\'enrichissement',
            }
        },
        {
            path: '/service-credit-coupons',
            name: 'service-credit-coupons',
            component: () => import('@/admin/views/ServiceCreditCouponsView.vue'),
            meta: {
                metaTitle: 'Coupons - Admin - Smashr',
                title: 'Coupons',
            }
        },
        {
            path: '/service-taxes',
            name: 'service-taxes',
            component: () => import('@/admin/views/ServiceTaxesView.vue'),
            meta: {
                metaTitle: 'Taxes des services - Admin - Smashr',
                title: 'Taxes des services',
            }
        },
        {
            path: '/countries',
            name: 'countries',
            component: () => import('@/admin/views/CountriesView.vue'),
            meta: {
                metaTitle: 'Pays - Admin - Smashr',
                title: 'Pays',
            }
        },
        {
            path: '/interaction-types',
            name: 'interaction-types',
            component: () => import('@/admin/views/InteractionTypesView.vue'),
            meta: {
                metaTitle: 'Types d\'interactions - Admin - Smashr',
                title: 'Types d\'interactions',
            }
        },
        ...(isPreviewMode ? [
            {
                path: '/user-invitations',
                name: 'user-invitations',
                component: () => import('@/admin/views/UserInvitationsView.vue'),
                meta: {
                    metaTitle: 'Invitations utilisateur - Admin - Smashr',
                    title: 'Invitations utilisateur',
                }
            }
        ] : []),
        {
            path: '/:pathMatch(.*)*',
            redirect: '/home',
        }
    ]
});

bus.addEventListener('auth:logout', async () => {
    router.push('/login').then();
})

export default router;
