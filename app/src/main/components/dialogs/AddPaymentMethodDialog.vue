<template>
    <Dialog v-model:open="isOpen">
        <DialogContent class="sm:max-w-[425px]">
            <DialogHeader>
                <DialogTitle>Ajouter un moyen de paiement</DialogTitle>
                <DialogDescription>
                    Ajoutez une nouvelle carte bancaire pour vos paiements
                </DialogDescription>
            </DialogHeader>

            <div v-if="loading" class="flex items-center justify-center py-8">
                <div class="text-center">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
                    <p class="text-sm text-neutral-600 mt-2">Initialisation...</p>
                </div>
            </div>

            <div v-else-if="error" class="text-center py-8">
                <p class="text-red-600 text-sm">{{ error }}</p>
                <Button @click="initStripe" variant="outline" size="sm" class="mt-4">
                    Réessayer
                </Button>
            </div>

            <div v-else class="space-y-4">
                <div>
                    <Label for="cardholder-name">Nom du titulaire</Label>
                    <Input 
                        id="cardholder-name"
                        v-model="cardholderName"
                        placeholder="Nom complet"
                        class="mt-1"
                    />
                </div>

                <div>
                    <Label>Informations de la carte</Label>
                    <div 
                        ref="cardElementRef" 
                        class="mt-1 p-3 border border-neutral-200 rounded-md min-h-[40px] bg-white"
                    ></div>
                </div>

                <div v-if="cardError" class="text-red-600 text-sm">
                    {{ cardError }}
                </div>
            </div>

            <DialogFooter>
                <Button 
                    @click="close" 
                    variant="outline"
                    :disabled="processing"
                >
                    Annuler
                </Button>
                <Button 
                    @click="addPaymentMethod" 
                    :disabled="!stripeReady || processing || !cardholderName.trim()"
                    class="relative"
                >
                    <span v-if="processing" class="flex items-center">
                        <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Ajout en cours...
                    </span>
                    <span v-else>Ajouter la carte</span>
                </Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { Button } from '@/common/components/ui/button'
import { Input } from '@/common/components/ui/input'
import { Label } from '@/common/components/ui/label'
import { ref, nextTick, watch } from 'vue'
import { useFetcher } from '@/common/composables/fetcher'

const props = defineProps({
    open: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:open', 'payment-method-added'])

const fetcher = useFetcher()

const isOpen = ref(false)
const loading = ref(false)
const error = ref(null)
const processing = ref(false)
const stripeReady = ref(false)
const cardholderName = ref('')
const cardError = ref(null)
const clientSecret = ref('')

let stripe = null
let elements = null
let cardElement = null
const cardElementRef = ref(null)

// Fonction pour charger Stripe.js dynamiquement
const loadStripe = () => {
    return new Promise((resolve, reject) => {
        if (window.Stripe) {
            resolve(window.Stripe)
            return
        }

        const script = document.createElement('script')
        script.src = 'https://js.stripe.com/v3/'
        script.onload = () => {
            if (window.Stripe) {
                resolve(window.Stripe)
            } else {
                reject(new Error('Stripe failed to load'))
            }
        }
        script.onerror = () => reject(new Error('Failed to load Stripe script'))
        document.head.appendChild(script)
    })
}

const initStripe = async () => {
    try {
        loading.value = true
        error.value = null

        // Charger Stripe.js dynamiquement
        const StripeConstructor = await loadStripe()

        // Créer un setup intent
        const response = await fetcher.post('/workspace/subscription/setup-intent', {})
        const { client_secret, publishable_key } = response.data
        
        // Stocker le client_secret pour l'utiliser plus tard
        clientSecret.value = client_secret

        if (!publishable_key) {
            error.value = "Configuration Stripe manquante"
            return
        }

        stripe = StripeConstructor(publishable_key)
        
        // Debug pour vérifier la clé
        console.log('Stripe key:', publishable_key)
        
        elements = stripe.elements({
            clientSecret: client_secret
        })

        cardElement = elements.create('card', {
            style: {
                base: {
                    fontSize: '16px',
                    color: '#424770',
                    '::placeholder': {
                        color: '#aab7c4',
                    },
                },
            },
        })

        // Marquer comme non-loading pour rendre l'élément DOM
        loading.value = false
        
        // Attendre que l'élément soit rendu dans le DOM
        await nextTick()
        await new Promise(resolve => setTimeout(resolve, 200))
        
        console.log('cardElementRef.value:', cardElementRef.value)
        
        if (cardElementRef.value) {
            console.log('Montage du cardElement...')
            
            // Vérifier que l'élément est bien visible
            const rect = cardElementRef.value.getBoundingClientRect()
            console.log('Element dimensions:', rect)
            
            if (rect.width === 0 || rect.height === 0) {
                console.warn('Element not visible yet, waiting...')
                await new Promise(resolve => setTimeout(resolve, 300))
            }
            
            cardElement.mount(cardElementRef.value)
            
            cardElement.on('change', ({error}) => {
                cardError.value = error ? error.message : null
            })
            
            cardElement.on('ready', () => {
                console.log('Card element is ready')
                stripeReady.value = true
            })
            
            cardElement.on('focus', () => {
                console.log('Card element focused')
            })

        } else {
            console.error('cardElementRef.value is still null after waiting')
            error.value = "Erreur de montage du composant de carte"
        }

    } catch (err) {
        console.error('Erreur initialisation Stripe:', err)
        error.value = "Erreur lors de l'initialisation du paiement"
    } finally {
        // Ne pas remettre loading à false ici car on l'a déjà fait plus haut
        // loading.value = false
    }
}

const addPaymentMethod = async () => {
    if (!stripe || !cardElement || !cardholderName.value.trim()) return

    try {
        processing.value = true
        cardError.value = null

        const { error, setupIntent } = await stripe.confirmCardSetup(
            clientSecret.value,  // Le client_secret qu'on a stocké
            {
                payment_method: {
                    card: cardElement,
                    billing_details: {
                        name: cardholderName.value.trim(),
                    },
                }
            }
        )

        if (error) {
            cardError.value = error.message
        } else if (setupIntent && setupIntent.status === 'succeeded') {
            emit('payment-method-added')
            close()
        }

    } catch (err) {
        console.error('Erreur ajout moyen de paiement:', err)
        cardError.value = "Une erreur est survenue lors de l'ajout de la carte"
    } finally {
        processing.value = false
    }
}

const close = () => {
    emit('update:open', false)
}

const reset = () => {
    cardholderName.value = ''
    cardError.value = null
    processing.value = false
    stripeReady.value = false
    clientSecret.value = ''
    
    if (cardElement) {
        cardElement.destroy()
        cardElement = null
    }
    if (elements) {
        elements = null
    }
    stripe = null
}

watch(() => props.open, async (newValue) => {
    isOpen.value = newValue
    
    if (newValue) {
        // Attendre que la modal soit complètement rendue
        await nextTick()
        await new Promise(resolve => setTimeout(resolve, 150))
        initStripe()
    } else {
        reset()
    }
})

watch(isOpen, (newValue) => {
    if (!newValue) {
        close()
    }
})
</script> 
