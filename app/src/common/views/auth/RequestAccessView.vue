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
							Demander l'accès
						</CardTitle>
						<CardDescription>
							Remplissez le formulaire ci-dessous pour demander l'accès à Trottr
						</CardDescription>
					</CardHeader>
					<CardContent>
						<form @submit.prevent="handleSubmit">
							<div class="grid gap-6">
								<div class="grid gap-6">
									<!-- Nom complet -->
									<div class="grid gap-2">
										<Label for="name">Nom complet</Label>
										<Input id="name" v-model="form.name" type="text" placeholder="Votre nom complet"
											required @input="resetError" autofocus
											:class="nameError ? 'border-red-500' : ''" />
										<p v-if="nameError" class="text-sm text-red-500">{{ nameError }}</p>
									</div>

									<!-- Email -->
									<div class="grid gap-2">
										<Label for="email">Email</Label>
										<Input id="email" v-model="form.email" type="email"
											placeholder="votre@email.com" required @input="resetError"
											:class="emailError ? 'border-red-500' : ''" />
										<p v-if="emailError" class="text-sm text-red-500">{{ emailError }}</p>
									</div>

									<!-- Société -->
									<div class="grid gap-2">
										<Label for="company">Société (optionnel)</Label>
										<Input id="company" v-model="form.company" type="text"
											placeholder="Nom de votre société" @input="resetError" />
									</div>

									<!-- Effectif -->
									<div class="grid gap-2">
										<Label for="staffRange">Effectif de l'entreprise (optionnel)</Label>
										<Select v-model="form.staffRange">
											<SelectTrigger class="w-full">
												<SelectValue placeholder="Sélectionnez l'effectif" />
											</SelectTrigger>
											<SelectContent>
												<SelectItem v-for="option in staffRangeOptions" :key="option.value"
													:value="option.value">
													{{ option.title }}
												</SelectItem>
											</SelectContent>
										</Select>
									</div>

									<!-- Message de validation -->
									<div v-if="!isFormValid && !loading && !success && hasAttemptedSubmit" class="text-sm text-red-500">
										Veuillez remplir les champs requis pour envoyer votre demande.
									</div>

									<!-- Bouton envoi -->
									<Button type="submit" class="w-full" :disabled="!isFormValid || loading">
										{{ loading ? 'Envoi...' : success ? 'Demande envoyée' : 'Envoyer ma demande' }}
									</Button>
								</div>

								<!-- Navigation -->
								<div class="text-center text-sm space-y-2">
									<div>
										<router-link to="/register"
											class="underline underline-offset-4 text-primary hover:text-primary/80">
											← Retour aux options d'inscription
										</router-link>
									</div>
									<div>
										Déjà un compte ?
										<router-link to="/login"
											class="underline underline-offset-4 text-primary hover:text-primary/80">
											Se connecter
										</router-link>
									</div>
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useFetcher } from '@/common/composables/fetcher'
import { Button } from '@/common/components/ui/button'
import { Input } from '@/common/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/common/components/ui/card'
import { Label } from '@/common/components/ui/label'
import { Alert, AlertDescription } from '@/common/components/ui/alert'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'

const router = useRouter()
const fetcher = useFetcher()

const form = ref({
	name: '',
	email: '',
	company: '',
	staffRange: null
})

const error = ref('')
const success = ref('')
const loading = ref(false)
const nameError = ref('')
const emailError = ref('')
const hasAttemptedSubmit = ref(false)

const staffRangeOptions = [
	{ title: '1-10 employés', value: '1-10' },
	{ title: '10-50 employés', value: '10-50' },
	{ title: '50-200 employés', value: '50-200' },
	{ title: '200-500 employés', value: '200-500' },
	{ title: '500-1K employés', value: '500-1K' },
	{ title: '1K-5K employés', value: '1K-5K' },
	{ title: '5K-10K employés', value: '5K-10K' },
	{ title: '> 10K employés', value: '> 10K' }
]

const isFormValid = computed(() => {
	return form.value.name && form.value.email && form.value.email.includes('@') && !loading.value && !success.value
})

const resetError = () => {
	error.value = ''
	nameError.value = ''
	emailError.value = ''
}

const validateForm = () => {
	resetError()
	let isValid = true

	if (!form.value.name.trim()) {
		nameError.value = 'Le nom est requis'
		isValid = false
	}

	if (!form.value.email) {
		emailError.value = 'L\'email est requis'
		isValid = false
	} else if (!form.value.email.includes('@')) {
		emailError.value = 'L\'email n\'est pas valide'
		isValid = false
	}

	return isValid
}

const handleSubmit = async () => {
  hasAttemptedSubmit.value = true
  
  if (!validateForm()) return

  try {
		loading.value = true

		await fetcher.post('/invitations/request-access', {
			name: form.value.name,
			email: form.value.email,
			company: form.value.company || null,
			staff_range: form.value.staffRange || null
		})

		success.value = 'Votre demande d\'accès a été soumise avec succès. Nous vous contacterons prochainement.'

		setTimeout(() => {
			router.push('/login')
		}, 3000)

	} catch (err) {
		error.value = err.response?.data?.detail || 'Une erreur est survenue lors de l\'envoi de votre demande'
	} finally {
		loading.value = false
	}
}
</script>
