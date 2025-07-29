<template>
	<div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gray-50">
		<div class="max-w-md w-full">
			<div class="flex flex-col gap-6">
				<Card class="pt-0">
					<CardHeader class="text-center">
						<div
							class="flex justify-center mb-4 -mt-8 transition-all duration-500 [transform-style:preserve-3d] hover:[transform:rotateY(180deg)]">
							<img src="/favicon.svg" alt="Smashr" class="rounded-full w-16 h-16" />
						</div>
						<CardTitle class="text-2xl">
							{{ isPreviewMode && !showRegisterForm ? 'Rejoindre Smashr' : 'Créer un compte' }}
						</CardTitle>
						<CardDescription>
							{{ isPreviewMode && !showRegisterForm ? 'Choisissez votre méthode d\'inscription' :
								'Utilisez le formulaire ci-dessous pour créer votre compte' }}
						</CardDescription>
					</CardHeader>
					<CardContent>
						<Alert v-if="error" variant="destructive" class="mb-4">
							<AlertDescription>
								{{ error }}
							</AlertDescription>
						</Alert>


						<!-- Mode choix d'inscription (preview mode) -->
						<div v-if="isPreviewMode && !showRegisterForm" class="flex flex-col gap-4">
							<Button @click="showAccessForm" class="w-full h-16 p-4 justify-start" variant="default">
								<div class="flex items-center gap-3">
									<UserRoundCheck class="!w-8 !h-8" stroke-width="1.2" />
									<div class="text-left">
										<div class="font-bold">J'ai un code d'invitation</div>
										<div class="text-xs opacity-80">Créer mon compte avec un code</div>
									</div>
								</div>
							</Button>

							<Button @click="showRequestForm" variant="outline" class="w-full h-16 p-4 justify-start">
								<div class="flex items-center gap-3">
									<ClipboardList class="!w-8 !h-8" stroke-width="1.2" />
									<div class="text-left">
										<div class="font-bold">Demander l'accès</div>
										<div class="text-xs opacity-80">Soumettre une demande d'inscription</div>
									</div>
								</div>
							</Button>

							<div class="text-center text-sm mt-4">
								Déjà un compte ?
								<router-link to="/login"
									class="underline underline-offset-4 text-primary hover:text-primary/80">
									Se connecter
								</router-link>
							</div>
						</div>

						<!-- Formulaire d'inscription -->
						<form v-else @submit.prevent="handleRegister">
							<div class="grid gap-6">
								<div class="grid gap-6">
									<!-- Code d'invitation (conditionnel) -->
									<div v-if="showInvitationCode" class="grid gap-2">
										<Label for="invitationCode">Code d'invitation</Label>
										<Input id="invitationCode" v-model="form.invitationCode" type="text"
											placeholder="Votre code d'invitation" required @input="resetError" autofocus
											:class="invitationCodeError ? 'border-red-500' : ''" />
										<p v-if="invitationCodeError" class="text-sm text-red-500">{{
											invitationCodeError }}</p>
									</div>

									<!-- Email -->
									<div class="grid gap-2">
										<Label for="email">Email</Label>
										<Input id="email" v-model="form.email" type="email"
											placeholder="Votre adresse email" required @input="resetError"
											:autofocus="!showInvitationCode" :readonly="isWorkspaceInvitation"
											:class="emailError ? 'border-red-500' : ''" />
										<p v-if="emailError" class="text-sm text-red-500">{{ emailError }}</p>
									</div>

									<!-- Mot de passe -->
									<div class="grid gap-2">
										<Label for="password">Mot de passe</Label>
										<Input id="password" v-model="form.password" type="password" required
											placeholder="Mot de passe" @input="resetError"
											:class="passwordError ? 'border-red-500' : ''" />
										<p v-if="passwordError" class="text-sm text-red-500">{{ passwordError }}</p>
									</div>

									<!-- Confirmation mot de passe -->
									<div class="grid gap-2">
										<Label for="confirmPassword">Confirmer le mot de passe</Label>
										<Input id="confirmPassword" v-model="form.confirmPassword" type="password"
											required placeholder="Confirmer le mot de passe" @input="resetError"
											@keyup.enter="handleRegister"
											:class="confirmPasswordError ? 'border-red-500' : ''" />
										<p v-if="confirmPasswordError" class="text-sm text-red-500">{{
											confirmPasswordError }}</p>
									</div>

									<!-- Bouton inscription -->
									<Button type="submit" class="w-full" :disabled="loading">
										{{ loading ? 'Création...' : 'Créer mon compte' }}
									</Button>
								</div>

								<!-- Lien vers connexion -->
								<div class="text-center text-sm">
									Déjà un compte ?
									<router-link to="/login"
										class="underline underline-offset-4 text-primary hover:text-primary/80">
										Se connecter
									</router-link>
								</div>
							</div>
						</form>
					</CardContent>
				</Card>

				<!-- Conditions d'utilisation -->
				<div
					class="text-balance text-center text-xs text-muted-foreground [&_a]:underline [&_a]:underline-offset-4 [&_a]:hover:text-primary">
					En continuant, vous acceptez les
					<a href="https://smashr.ai/conditions-utilisation" target="_blank">
						conditions générales d'utilisation
					</a>.
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
import { useFetcher } from '@/common/composables/fetcher'
import { usePreview } from '@/common/composables/preview'
import useRecaptcha from '@/common/composables/useRecaptcha'
import { useAuthStore } from '@/common/stores/auth'
import { ClipboardList, UserRoundCheck } from 'lucide-vue-next'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const { getToken } = useRecaptcha()
const { isPreviewMode } = usePreview()
const fetcher = useFetcher()

const form = ref({
	email: '',
	password: '',
	confirmPassword: '',
	invitationCode: ''
})

const error = ref('')
const loading = ref(false)
const emailError = ref('')
const passwordError = ref('')
const confirmPasswordError = ref('')
const invitationCodeError = ref('')
const showRegisterForm = ref(!isPreviewMode)
const showInvitationCode = ref(false)
const workspaceInvitationToken = ref('')
const isWorkspaceInvitation = ref(false)
const workspaceInvitationInfo = ref(null)

const resetError = () => {
	error.value = ''
	emailError.value = ''
	passwordError.value = ''
	confirmPasswordError.value = ''
	invitationCodeError.value = ''
}

const showAccessForm = () => {
	showRegisterForm.value = true
	showInvitationCode.value = true
}

const showRequestForm = () => {
	router.push('/register/request-access')
}

const checkWorkspaceInvitation = async (token) => {
	try {
		const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/workspace-invitation/${token}`)
		const data = await response.json()

		if (response.ok && data) {
			workspaceInvitationToken.value = token
			isWorkspaceInvitation.value = true
			workspaceInvitationInfo.value = data
			form.value.email = data.email
			showRegisterForm.value = true
			showInvitationCode.value = false
		} else {
			error.value = 'Lien d\'invitation invalide ou expiré'
		}
	} catch (error) {
		error.value = 'Lien d\'invitation invalide ou expiré'
	}
}

onMounted(async () => {
	if (route.params.invitationCode) {
		form.value.invitationCode = route.params.invitationCode
		showRegisterForm.value = true
		showInvitationCode.value = true
	}

	if (route.query.token) {
		await checkWorkspaceInvitation(route.query.token)
	}
})

const validateForm = () => {
	resetError()
	let isValid = true

	if (showInvitationCode.value && !form.value.invitationCode) {
		invitationCodeError.value = 'Le code d\'invitation est requis'
		isValid = false
	}

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

const handleRegister = async () => {
	if (!validateForm()) return

	try {
		loading.value = true

		const recaptchaToken = await getToken('register')

		const registerData = {
			email: form.value.email,
			password: form.value.password,
			recaptcha_token: recaptchaToken,
		}

		if (form.value.invitationCode) {
			registerData.invitation_code = form.value.invitationCode
		}

		if (isWorkspaceInvitation.value && workspaceInvitationToken.value) {
			registerData.workspace_invitation_token = workspaceInvitationToken.value
		}

		await authStore.register(registerData)

		router.push({
			path: '/verify-code',
			query: { email: form.value.email }
		})
	} catch (err) {
		const errorDetail = err.response?.data?.detail || err.data?.detail || 'Une erreur est survenue lors de l\'inscription'

		// Messages d'erreur plus conviviaux
		if (errorDetail === 'Email already registered') {
			error.value = 'Cette adresse email est déjà utilisée. Essayez de vous connecter ou utilisez une autre adresse.'
		} else if (errorDetail === 'Code d\'invitation requis en mode preview') {
			error.value = 'Un code d\'invitation est requis pour créer un compte.'
		} else if (errorDetail === 'Code d\'invitation invalide ou email incorrect') {
			error.value = 'Le code d\'invitation est invalide ou ne correspond pas à votre adresse email.'
		} else if (errorDetail === 'Invitation workspace invalide ou expirée') {
			error.value = 'Cette invitation a expiré ou n\'est plus valide.'
		} else {
			error.value = errorDetail
		}
	} finally {
		loading.value = false
	}
}
</script>
