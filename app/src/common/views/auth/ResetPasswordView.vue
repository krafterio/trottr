<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gray-50">
    <div class="max-w-md w-full">
      <div class="flex flex-col gap-6">
        <Alert v-if="success" class="border-green-200 bg-green-50 text-green-800">
          <AlertDescription>
            {{ success }}
          </AlertDescription>
        </Alert>

        <Alert v-if="error" variant="destructive">
          <AlertDescription>
            {{ error }}
          </AlertDescription>
        </Alert>

        <Card>
          <CardHeader class="text-center">
            <div class="flex justify-center mb-4">
              <img src="@/common/assets/img/logo.svg" alt="Trottr" class="w-24 h-8" />
            </div>
            <CardTitle class="text-2xl">
              Nouveau mot de passe
            </CardTitle>
            <CardDescription>
              Saisissez votre nouveau mot de passe
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form @submit.prevent="handleResetPassword">
              <div class="grid gap-6">
                <div class="grid gap-6">
                  <!-- Nouveau mot de passe -->
                  <div class="grid gap-2">
                    <Label for="password">Nouveau mot de passe</Label>
                    <Input 
                      id="password" 
                      v-model="form.password" 
                      type="password" 
                      placeholder="••••••••••••" 
                      required 
                      :disabled="loading"
                      autofocus
                      :class="passwordError ? 'border-red-500' : ''"
                    />
                    <p v-if="passwordError" class="text-sm text-red-500">{{ passwordError }}</p>
                  </div>

                  <!-- Confirmer mot de passe -->
                  <div class="grid gap-2">
                    <Label for="confirmPassword">Confirmer le nouveau mot de passe</Label>
                    <Input 
                      id="confirmPassword" 
                      v-model="form.confirmPassword" 
                      type="password" 
                      placeholder="••••••••••••" 
                      required 
                      :disabled="loading"
                      :class="confirmPasswordError ? 'border-red-500' : ''"
                      @keyup.enter="handleResetPassword"
                    />
                    <p v-if="confirmPasswordError" class="text-sm text-red-500">{{ confirmPasswordError }}</p>
                  </div>

                  <!-- Bouton réinitialisation -->
                  <Button type="submit" class="w-full" :disabled="success || !isFormValid || loading">
                    {{ loading ? 'Réinitialisation...' : 'Réinitialiser le mot de passe' }}
                  </Button>
                </div>

                <!-- Navigation -->
                <div class="text-center text-sm">
                  <router-link to="/login" class="underline underline-offset-4 text-primary hover:text-primary/80">
                    Retour à la connexion
                  </router-link>
                </div>
              </div>
            </form>
          </CardContent>
        </Card>

        <!-- Conditions d'utilisation -->
        <div
          class="text-balance text-center text-xs text-muted-foreground [&_a]:underline [&_a]:underline-offset-4 [&_a]:hover:text-primary">
          En continuant, vous acceptez nos <a href="#">Conditions d'utilisation</a>
          et notre <a href="#">Politique de confidentialité</a>.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/common/stores/auth'
import { Button } from '@/common/components/ui/button'
import { Input } from '@/common/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/common/components/ui/card'
import { Label } from '@/common/components/ui/label'
import { Alert, AlertDescription } from '@/common/components/ui/alert'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const form = ref({
    password: '',
    confirmPassword: '',
})

const error = ref('')
const success = ref('')
const loading = ref(false)
const passwordError = ref('')
const confirmPasswordError = ref('')
const token = ref('')

const isFormValid = computed(() => {
    return token.value
        && form.value.password
        && form.value.password.length >= 6
        && form.value.confirmPassword
        && form.value.password === form.value.confirmPassword
})

onMounted(() => {
    token.value = route.query.token || ''

    if (!token.value) {
        error.value = 'Token de réinitialisation manquant'
    }
})

const resetError = () => {
    error.value = ''
    passwordError.value = ''
    confirmPasswordError.value = ''
}

const validateForm = () => {
    resetError()

    let isValid = true

    if (!form.value.password) {
        passwordError.value = 'Le mot de passe est requis'
        isValid = false
    } else if (form.value.password.length < 6) {
        passwordError.value = 'Le mot de passe doit contenir au moins 6 caractères'
        isValid = false
    }

    if (!form.value.confirmPassword) {
        confirmPasswordError.value = 'La confirmation du mot de passe est requise'
        isValid = false
    } else if (form.value.password !== form.value.confirmPassword) {
        confirmPasswordError.value = 'Les mots de passe ne correspondent pas'
        isValid = false
    }

    return isValid
}

const handleResetPassword = async () => {
    if (!validateForm() || !token.value) {
        return
    }

    try {
        loading.value = true

        await authStore.confirmPasswordReset({
            token: token.value,
            new_password: form.value.password,
        })

        success.value = 'Votre mot de passe a été réinitialisé avec succès. Vous pouvez maintenant vous connecter.'

        setTimeout(() => {
            router.push('/login').then()
        }, 2000)
    } catch (err) {
        error.value = err.response?.data?.detail || 'Une erreur est survenue'
    } finally {
        loading.value = false
    }
}
</script> 
