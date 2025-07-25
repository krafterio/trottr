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

        <Card class="pt-0">
          <CardHeader class="text-center">
            <div class="flex justify-center mb-4 -mt-8">
              <img src="/favicon.svg" alt="Smashr" class="rounded-full w-16 h-16" />
            </div>
            <CardTitle class="text-2xl">
              Mot de passe oublié
            </CardTitle>
            <CardDescription>
              Saisissez votre adresse email pour recevoir un lien de réinitialisation
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form @submit.prevent="handleForgotPassword">
              <div class="grid gap-6">
                <div class="grid gap-6">
                  <!-- Email -->
                  <div class="grid gap-2">
                    <Label for="email">Adresse email</Label>
                    <Input id="email" v-model="form.email" type="email" placeholder="stanley@gmail.com" required
                      :disabled="loading" autofocus :class="emailError ? 'border-red-500' : ''"
                      @keyup.enter="handleForgotPassword" />
                    <p v-if="emailError" class="text-sm text-red-500">{{ emailError }}</p>
                  </div>

                  <!-- Bouton envoi -->
                  <Button type="submit" class="w-full" :disabled="loading">
                    {{ loading ? 'Envoi...' : 'Envoyer le lien de réinitialisation' }}
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
import { Alert, AlertDescription } from '@/common/components/ui/alert'
import { Button } from '@/common/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/common/components/ui/card'
import { Input } from '@/common/components/ui/input'
import { Label } from '@/common/components/ui/label'
import useRecaptcha from '@/common/composables/useRecaptcha'
import { useAuthStore } from '@/common/stores/auth'
import { ref } from 'vue'

const authStore = useAuthStore()
const { getToken } = useRecaptcha()

const form = ref({
  email: '',
})

const error = ref('')
const success = ref('')
const loading = ref(false)
const emailError = ref('')

const resetError = () => {
  error.value = ''
  emailError.value = ''
  success.value = ''
}

const validateForm = () => {
  resetError()

  let isValid = true

  if (!form.value.email) {
    emailError.value = 'L\'email est requis'
    isValid = false
  } else if (!form.value.email.includes('@')) {
    emailError.value = 'L\'email n\'est pas valide'
    isValid = false
  }

  return isValid
}

const handleForgotPassword = async () => {
  if (!validateForm()) {
    return
  }

  try {
    loading.value = true

    const recaptchaToken = await getToken('password_reset')

    await authStore.requestPasswordReset({
      email: form.value.email,
      recaptcha_token: recaptchaToken,
    })

    success.value = 'Si cette adresse email existe dans notre système, un lien de réinitialisation a été envoyé.'
    form.value.email = ''
  } catch (err) {
    error.value = err.response?.data?.detail || 'Une erreur est survenue'
  } finally {
    loading.value = false
  }
}
</script>
