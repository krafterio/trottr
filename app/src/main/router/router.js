import { bus } from "@/common/composables/bus.js";
import { useAuthStore } from '@/common/stores/auth';
import { isValidFeaturesLevel } from "@/common/utils/features.js";
import { useWorkspaceStore } from "@/main/stores/workspace.js";
import { createRouter, createWebHistory } from 'vue-router';

const isPreviewMode = import.meta.env.VITE_MODE_PREVIEW === 'True';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/common/views/auth/LoginView.vue'),
      meta: {
        requiresGuest: true,
        metaTitle: 'Connexion - Trottr',
        title: 'Connexion'
      }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/common/views/auth/RegisterView.vue'),
      meta: {
        requiresGuest: true,
        metaTitle: 'Inscription - Trottr',
        title: 'Inscription'
      }
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('@/common/views/auth/ForgotPasswordView.vue'),
      meta: {
        requiresGuest: true,
        metaTitle: 'Mot de passe oublié - Trottr',
        title: 'Mot de passe oublié'
      }
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: () => import('@/common/views/auth/ResetPasswordView.vue'),
      meta: {
        requiresGuest: true,
        metaTitle: 'Réinitialiser le mot de passe - Trottr',
        title: 'Réinitialiser le mot de passe'
      }
    },
    {
      path: '/verify-code',
      name: 'verify-code',
      component: () => import('@/common/views/auth/VerifyCodeView.vue'),
      meta: {
        requiresGuest: true,
        metaTitle: 'Vérification - Trottr',
        title: 'Vérification'
      }
    },
    {
      path: '/',
      name: 'jobs',
      component: () => import('@/main/views/jobs/JobsView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Interventions'
      }
    },
    {
      path: '/jobs-proto',
      name: 'jobs-proto',
      component: () => import('@/main/views/jobs/proto/JobsView__Proto.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Interventions'
      }
    },
    {
      path: '/job-proto',
      name: 'job-proto',
      component: () => import('@/main/views/jobs/proto/JobView__Proto.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Intervention'
      }
    },
    {
      path: '/job-planner',
      name: 'job-planner',
      component: () => import('@/main/views/jobs/JobPlanner.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Planificateur d\'interventions'
      }
    },
    {
      path: '/job/:id',
      name: 'job',
      component: () => import('@/main/views/jobs/JobView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Détails de l\'intervention'
      }
    },
    {
      path: '/settings',
      component: () => import('@/main/views/settings/SettingsLayout.vue'),
      meta: {
        requiresAuth: true,
      },
      children: [
        {
          path: '',
          redirect: '/settings/general'
        },
        {
          path: 'general',
          name: 'settings-general',
          component: () => import('@/main/views/settings/pages/SettingsGeneral.vue'),
          meta: {
            metaTitle: 'Paramètres généraux'
          }
        },
        {
          path: 'jobs',
          name: 'settings-jobs',
          component: () => import('@/main/views/settings/pages/SettingsJob.vue'),
          meta: {
            metaTitle: 'Paramètres interventions'
          }
        },
        {
          path: 'crm',
          name: 'settings-crm',
          component: () => import('@/main/views/settings/pages/SettingsCrm.vue'),
          meta: {
            metaTitle: 'Paramètres CRM'
          }
        },
        {
          path: 'users',
          name: 'settings-users',
          component: () => import('@/main/views/settings/pages/SettingsUsers.vue'),
          meta: {
            metaTitle: 'Paramètres utilisateurs'
          }
        },
        {
          path: 'operators',
          name: 'settings-operators',
          component: () => import('@/main/views/settings/pages/SettingsOperators.vue'),
          meta: {
            metaTitle: 'Paramètres opérateurs'
          }
        },
        {
          path: 'billing',
          name: 'settings-billing',
          component: () => import('@/main/views/settings/pages/SettingsBilling.vue'),
          meta: {
            metaTitle: 'Paramètres facturation'
          }
        },
      ]
    },
    {
      path: '/planning',
      name: 'planning',
      component: () => import('@/main/views/planner/JobWeekPlanner.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Planning'
      }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/main/views/dashboard/DashboardView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Tableau de bord'
      }
    },
    {
      path: '/companies',
      name: 'companies',
      component: () => import('@/main/views/crm/CompaniesView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Entreprises'
      }
    },
    {
      path: '/company/:id',
      name: 'company',
      component: () => import('@/main/views/crm/CompanyView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Fiche entreprise'
      }
    },
    {
      path: '/contacts',
      name: 'contacts',
      component: () => import('@/main/views/crm/ContactsView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Contacts'
      }
    },
    {
      path: '/contact/:id',
      name: 'contact',
      component: () => import('@/main/views/crm/ContactView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Fiche contact'
      }
    },
    {
      path: '/sites',
      name: 'sites',
      component: () => import('@/main/views/crm/SitesView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Sites d\'intervention'
      }
    },
    {
      path: '/site/:id',
      name: 'site',
      component: () => import('@/main/views/crm/SiteView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Fiche site'
      }
    },
    {
      path: '/subsites',
      name: 'subsites',
      component: () => import('@/main/views/crm/SubsitesView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Lots'
      }
    },
    {
      path: '/subsite/:id',
      name: 'subsite',
      component: () => import('@/main/views/crm/SubsiteView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Fiche lot'
      }
    },
    {
      path: '/operateurs',
      name: 'operateurs',
      component: () => import('@/main/views/rh/OperatorsView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Techniciens'
      }
    },
    {
      path: '/absences',
      name: 'absences',
      component: () => import('@/main/views/rh/OperatorsAbsencesView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Absences / Congés'
      }
    },
    {
      path: '/operations',
      name: 'operations',
      component: () => import('@/main/views/gestion/OperationsView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Opérations'
      }
    },
    {
      path: '/diagnostics',
      name: 'diagnostics',
      component: () => import('@/main/views/gestion/JobsDiagnosticsView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Diagnostics'
      }
    },
    {
      path: '/produits',
      name: 'produits',
      component: () => import('@/main/views/gestion/ProductsView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Fiches produits'
      }
    },
    {
      path: '/stock',
      name: 'stock',
      component: () => import('@/main/views/gestion/StocksView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Stock pièces détachées'
      }
    },
    {
      path: '/workspace',
      name: 'workspace-home',
      redirect: '/',
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/home',
      redirect: '/',
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
      meta: {
        metaTitle: 'Page non trouvée - Trottr'
      }
    }
  ]
})

router.afterEach((to) => {
  const defaultTitle = 'Trottr'
  document.title = to.meta.metaTitle || defaultTitle
  bus.trigger('record-context', { type: null, id: null })
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated

  if ((to.meta.requiresGuest || !isValidFeaturesLevel(to.meta.featuresLevel)) && isAuthenticated) {
    // Permettre l'accès au register avec un token d'invitation workspace
    if (to.name === 'register' && to.query.token) {
      next()
      return
    }
    next({ name: 'home' })
    return
  }

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  if (to.name === 'jobs' && isAuthenticated) {
    // redirect to module
  }

  next()
})

router.beforeEach(async (to, from, next) => {
  const workspaceStore = useWorkspaceStore()
  const authStore = useAuthStore()

  if (authStore.isAuthenticated) {
    await workspaceStore.fetchWorkspace()
  }

  if (authStore.isAuthenticated && to.meta.requiresPlan && !workspaceStore.hasPlan(to.meta.requiresPlan)) {
    next({ name: 'home' })
    return
  }

  next()
})

router.beforeEach(async (to, from, next) => {
  const workspaceStore = useWorkspaceStore()
  const authStore = useAuthStore()

  if (authStore.isAuthenticated) {
    const isAuthRoute = to.meta.requiresGuest || !to.meta.requiresAuth

    if (!workspaceStore.isValid && !isAuthRoute) {
      // Rediriger vers settings billing
      if (to.name !== 'settings-billing' && to.name !== 'settings-users') {
        next({ name: 'settings-billing' })
        return
      }
    }
  }

  next()
})

bus.addEventListener('auth:logout', async () => {
  router.push('/login').then();
})

bus.addEventListener('workspace:invalid-license', async () => {
  bus.trigger('open-workspace-manager-modal', { tab: 'licenses' })
})

export default router 
