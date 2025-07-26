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
      path: '/home',
      name: 'home',
      component: () => import('@/main/views/HomeView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Accueil'
      }
    },
    {
      path: '/job-planner',
      name: 'job-planner',
      component: () => import('@/main/views/JobPlanner.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Planificateur d\'interventions'
      }
    },
    {
      path: '/job/:id',
      name: 'job',
      component: () => import('@/main/views/JobView.vue'),
      meta: {
        requiresAuth: true,
        metaTitle: 'Détails de l\'intervention'
      }
    },
    {
      path: '/workspace',
      name: 'workspace-home',
      redirect: '/home',
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/',
      name: 'root',
      redirect: (to) => {
        const authStore = useAuthStore()
        return authStore.isAuthenticated ? { name: 'home' } : { name: 'login' }
      },
      meta: {
        metaTitle: 'Smashr'
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

  if (to.name === 'home' && isAuthenticated) {
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
      // Rediriger vers home et ouvrir la modal des licences
      if (to.name !== 'home') {
        bus.trigger('open-workspace-manager-modal', { tab: 'licenses' })
        next({ name: 'home' })
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
