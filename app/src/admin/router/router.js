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
                metaTitle: 'Connexion - Trottr',
                title: 'Connexion',
            },
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('@/common/views/auth/RegisterView.vue'),
            meta: {
                metaTitle: 'Inscription - Trottr',
                title: 'Inscription'
            }
        },
        {
            path: '/verify-code',
            name: 'verify-code',
            component: () => import('@/common/views/auth/VerifyCodeView.vue'),
            meta: {
                metaTitle: 'Vérification - Trottr',
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
                metaTitle: 'Espaces de travail - Admin - Trottr',
                title: 'Espaces de travail',
            }
        },
        {
            path: '/service-plans',
            name: 'service-plans',
            component: () => import('@/admin/views/ServicePlansView.vue'),
            meta: {
                metaTitle: 'Plans - Admin - Trottr',
                title: 'Plans',
            }
        },
        {
            path: '/service-taxes',
            name: 'service-taxes',
            component: () => import('@/admin/views/ServiceTaxesView.vue'),
            meta: {
                metaTitle: 'Taxes des services - Admin - Trottr',
                title: 'Taxes des services',
            }
        },
        {
            path: '/countries',
            name: 'countries',
            component: () => import('@/admin/views/CountriesView.vue'),
            meta: {
                metaTitle: 'Pays - Admin - Trottr',
                title: 'Pays',
            }
        },
        ...(isPreviewMode ? [
            {
                path: '/user-invitations',
                name: 'user-invitations',
                component: () => import('@/admin/views/UserInvitationsView.vue'),
                meta: {
                    metaTitle: 'Invitations utilisateur - Admin - Trottr',
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
