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
        metaTitle: 'Connexion - Smashr',
        title: 'Connexion'
      }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/common/views/auth/RegisterView.vue'),
      meta: {
        requiresGuest: true,
        metaTitle: 'Inscription - Smashr',
        title: 'Inscription'
      }
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('@/common/views/auth/ForgotPasswordView.vue'),
      meta: {
        requiresGuest: true,
        metaTitle: 'Mot de passe oublié - Smashr',
        title: 'Mot de passe oublié'
      }
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: () => import('@/common/views/auth/ResetPasswordView.vue'),
      meta: {
        requiresGuest: true,
        metaTitle: 'Réinitialiser le mot de passe - Smashr',
        title: 'Réinitialiser le mot de passe'
      }
    },
    {
      path: '/verify-code',
      name: 'verify-code',
      component: () => import('@/common/views/auth/VerifyCodeView.vue'),
      meta: {
        requiresGuest: true,
        metaTitle: 'Vérification - Smashr',
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
      name: 'settings',
      component: () => import('@/main/views/settings/SettingsView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Paramètres'
      }
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
      path: '/techniciens',
      name: 'techniciens',
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
        metaTitle: 'Page non trouvée - Smashr'
      }
    }
  ]
})

router.afterEach((to) => {
  const defaultTitle = 'Smashr'
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
      // Rediriger vers jobs et ouvrir la modal des licences
      if (to.name !== 'jobs') {
        bus.trigger('open-workspace-manager-modal', { tab: 'licenses' })
        next({ name: 'jobs' })
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
