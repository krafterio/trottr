<template>
	<div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gray-50">
		<div class="max-w-md w-full">
			<div class="flex flex-col gap-6">
				<Alert v-if="route.query.account_created_success" class="border-green-200 bg-green-50 text-green-800">
					<AlertDescription>
						Votre compte a été créé avec succès. Vous pouvez vous connecter.
					</AlertDescription>
				</Alert>

				<Card class="pt-0">
					<CardHeader class="text-center">
						<div class="flex justify-center mb-4 -mt-8">
							<img src="/favicon.svg" alt="Smashr" class="rounded-full w-16 h-16" />
						</div>
						<CardTitle class="text-2xl">
							Bienvenue sur Trottr
						</CardTitle>
						<CardDescription>
							Connectez-vous à votre compte
						</CardDescription>
					</CardHeader>
					<CardContent>
						<Alert v-if="error" variant="default" class="mb-4 border-0 bg-red-50">
							<AlertDescription class="text-red-800 flex items-center gap-2">
								<TriangleAlert class="h-4 w-4" />
								{{ error }}
							</AlertDescription>
						</Alert>
						<form @submit.prevent="handleLogin">
							<div class="grid gap-6">
								<div class="grid gap-6">
									<div class="grid gap-2">
										<Label for="email">Email</Label>
										<Input id="email" v-model="form.email" type="email"
											placeholder="alexander@supertramp.com" required @input="resetError"
											autofocus :class="emailError ? 'border-red-500' : ''" />
										<p v-if="emailError" class="text-sm text-red-500">{{ emailError }}</p>
									</div>
									<div class="grid gap-2">
										<div class="flex items-center">
											<Label for="password">Mot de passe</Label>
											<router-link to="/forgot-password"
												class="ml-auto text-sm underline-offset-4 hover:underline text-primary">
												Mot de passe oublié ?
											</router-link>
										</div>
										<Input id="password" v-model="form.password" type="password" required
											placeholder="••••••••••••" @input="resetError"
											:class="passwordError ? 'border-red-500' : ''" />
										<p v-if="passwordError" class="text-sm text-red-500">{{ passwordError }}</p>
									</div>
									<Button type="submit" class="w-full" :disabled="loading">
										{{ loading ? 'Connexion...' : 'Se connecter' }}
									</Button>
								</div>
								<div class="text-center text-sm">
									Vous n'avez pas encore de compte ?
									<router-link to="/register"
										class="underline underline-offset-4 text-primary hover:text-primary/80">
										Inscription
									</router-link>
								</div>
							</div>
						</form>
					</CardContent>
				</Card>
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
import { TriangleAlert } from 'lucide-vue-next'
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const { getToken } = useRecaptcha()

const form = ref({
	email: '',
	password: ''
})

const error = ref('')
const loading = ref(false)
const emailError = ref('')
const passwordError = ref('')
const rememberMe = ref(false)

const resetError = () => {
	error.value = ''
	emailError.value = ''
	passwordError.value = ''
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

	if (!form.value.password) {
		passwordError.value = 'Le mot de passe est requis'
		isValid = false
	}

	return isValid
}

const handleLogin = async () => {
	if (!validateForm() || loading.value) {
		return;
	}

	try {
		loading.value = true

		const recaptchaToken = await getToken('login')

		await authStore.login({
			...form.value,
			recaptcha_token: recaptchaToken,
		})

		router.push({
			path: '/verify-code',
			query: {
				email: form.value.email,
				redirect: route.query.redirect
			}
		})
	} catch (err) {
		error.value = authStore.error || 'Email ou mot de passe incorrect'
	} finally {
		loading.value = false
	}
}
</script>
