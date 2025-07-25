<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gray-50">
    <div class="max-w-md w-full">
      <div class="flex flex-col gap-6">
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
              Code de vérification
            </CardTitle>
            <CardDescription class="space-y-2">
              <p>
                Un code de vérification a été envoyé à <strong>{{ email }}</strong>.
                Entrez ce code à 6 chiffres ci-dessous pour accéder à votre compte.
              </p>
              <p class="text-xs text-muted-foreground">
                Pensez à vérifier vos courriers indésirables si vous ne voyez pas l'email.
              </p>
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form @submit.prevent="handleVerify">
              <div class="grid gap-6">
                <div class="grid gap-6">
                  <!-- PIN Input -->
                  <div class="flex justify-center">
                    <PinInput id="pin-input" v-model="pinValue" placeholder="○" class="gap-2" :length="6"
                      @complete="handlePinComplete" @update:model-value="handlePinUpdate">
                      <PinInputGroup class="gap-2">
                        <PinInputSlot v-for="(id, index) in 6" :key="id" :index="index"
                          class="w-12 h-12 text-center border rounded-md text-lg font-semibold" />
                      </PinInputGroup>
                    </PinInput>
                  </div>

                  <!-- Bouton vérification -->
                  <Button type="submit" class="w-full" :disabled="loading || !isCodeComplete">
                    {{ loading ? 'Vérification...' : 'Vérifier le code' }}
                  </Button>
                </div>

                <!-- Boutons Gmail/Outlook -->
                <div class="flex justify-center gap-4">
                  <Button variant="outline" size="sm" @click="openGmail" class="gap-2">
                    <Mail class="w-4 h-4" />
                    Gmail
                  </Button>
                  <Button variant="outline" size="sm" @click="openOutlook" class="gap-2">
                    <Mail class="w-4 h-4" />
                    Outlook
                  </Button>
                </div>

                <!-- Séparateur -->
                <div class="relative">
                  <div class="absolute inset-0 flex items-center">
                    <span class="w-full border-t" />
                  </div>
                  <div class="relative flex justify-center text-xs uppercase">
                    <span class="bg-background px-2 text-muted-foreground">
                      Problème ?
                    </span>
                  </div>
                </div>

                <!-- Renvoyer le code -->
                <div class="text-center space-y-3">
                  <p class="text-sm text-muted-foreground">Vous ne trouvez pas votre code ?</p>
                  <Button variant="outline" size="sm" @click="resendCode" :disabled="resendLoading">
                    {{ resendLoading ? 'Envoi...' : 'Demander un nouveau code' }}
                  </Button>
                </div>
              </div>
            </form>
          </CardContent>
        </Card>

        <!-- Sécurité info -->
        <div class="text-center space-y-2">
          <div class="flex items-center justify-center gap-2 text-sm text-muted-foreground">
            <Shield class="w-4 h-4" />
            <span>Sécurité renforcée</span>
          </div>
          <p class="text-xs text-muted-foreground">
            Votre compte est protégé par une authentification à deux facteurs
          </p>
        </div>

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
import { PinInput, PinInputGroup, PinInputSlot } from '@/common/components/ui/pin-input'
import { useFetcher } from '@/common/composables/fetcher'
import { useAuthStore } from '@/common/stores/auth'
import { Mail, Shield } from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const fetcher = useFetcher()

const email = ref(route.query.email || '')
const pinValue = ref('')
const pinCode = ref('')
const error = ref('')
const loading = ref(false)
const resendLoading = ref(false)

const isCodeComplete = computed(() => {
  return pinCode.value.length === 6
})

const handlePinUpdate = (value) => {
  pinValue.value = value
  if (Array.isArray(value)) {
    pinCode.value = value.join('')
  } else {
    pinCode.value = value || ''
  }
  error.value = ''
}

const handlePinComplete = (value) => {
  handlePinUpdate(value)
}

const handleVerify = async () => {
  if (!isCodeComplete.value) return

  try {
    loading.value = true
    error.value = ''

    await authStore.verifyLoginCode(email.value, pinCode.value)

    if (route.query.redirect) {
      router.push(route.query.redirect.toString())
    } else {
      router.push('/')
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Code de vérification invalide'
    pinValue.value = ''
    pinCode.value = ''
  } finally {
    loading.value = false
  }
}

const resendCode = async () => {
  try {
    resendLoading.value = true
    await fetcher.post('/auth/resend-login-code', {
      email: email.value
    })
    error.value = ''
  } catch (err) {
    error.value = err.response?.data?.detail || 'Erreur lors du renvoi du code'
  } finally {
    resendLoading.value = false
  }
}

const openGmail = () => {
  window.open('https://mail.google.com', '_blank')
}

const openOutlook = () => {
  window.open('https://outlook.live.com', '_blank')
}

onMounted(() => {
  if (!email.value) {
    router.push('/login')
    return
  }
})
</script>

<style scoped>
.code-input :deep(.v-field__input) {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  padding: 0;
}

.code-input :deep(.v-field) {
  font-size: 24px;
  line-height: 60px;
}
</style>