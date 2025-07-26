<template>
    <div class="max-w-5xl space-y-8">
        <div>
            <h2 class="text-lg font-semibold text-neutral-900">Votre entreprise</h2>
            <p class="text-neutral-600">Informations sur votre entreprise.</p>
        </div>

        <div class="space-y-6">

            <div class="space-y-6">
                <div class="space-y-2">
                    <Label for="company-name">Raison sociale</Label>
                    <Input id="company-name" v-model="companyName" placeholder="Nom de votre entreprise" />
                </div>

                <div class="space-y-2">
                    <Label for="street">Rue</Label>
                    <Input id="street" v-model="street" placeholder="123 rue de la République" />
                </div>

                <div class="space-y-2">
                    <Label for="street2">Rue 2 (optionnel)</Label>
                    <Input id="street2" v-model="street2" placeholder="Appartement, étage, etc." />
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <Label for="postal-code">Code postal</Label>
                        <Input id="postal-code" v-model="postalCode" placeholder="75001" />
                    </div>
                    <div class="space-y-2">
                        <Label for="city">Ville</Label>
                        <Input id="city" v-model="city" placeholder="Paris" />
                    </div>
                </div>

                <div class="space-y-2">
                    <Label for="country">Pays</Label>
                    <Select>
                        <SelectTrigger class="w-full">
                            <SelectValue placeholder="Sélectionner un pays" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="fr">France</SelectItem>
                            <SelectItem value="be">Belgique</SelectItem>
                            <SelectItem value="ch">Suisse</SelectItem>
                            <SelectItem value="ca">Canada</SelectItem>
                        </SelectContent>
                    </Select>
                </div>
            </div>

            <Separator />

            <!-- Section Informations légales -->
            <div>
                <h2 class="text-lg font-semibold text-neutral-900">Informations légales</h2>
                <p class="text-neutral-600">Informations légales et fiscales de votre entreprise.</p>
            </div>

            <div class="space-y-6">
                <div class="space-y-2">
                    <Label for="siren">Numéro de SIREN</Label>
                    <Input id="siren" v-model="sirenNumber" placeholder="123 456 789" />
                    <p class="text-sm text-neutral-500">
                        Numéro d'identification unique de votre entreprise (9 chiffres).
                    </p>
                </div>

                <div class="space-y-2">
                    <Label for="tva">Numéro de TVA</Label>
                    <Input id="tva" v-model="tvaNumber" placeholder="FR 12 345678901" />
                    <p class="text-sm text-neutral-500">
                        Numéro de TVA intracommunautaire (optionnel).
                    </p>
                </div>
            </div>

            <Separator />

            <div class="flex justify-end">
                <Button @click="updateProfile">
                    Mettre à jour le profil
                </Button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { Input } from '@/common/components/ui/input'
import { Label } from '@/common/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { Separator } from '@/common/components/ui/separator'
import { ref } from 'vue'

const username = ref('shadcn')
const bio = ref('Je suis propriétaire d\'un ordinateur.')
const website = ref('')

// Informations entreprise
const companyName = ref('')
const street = ref('')
const street2 = ref('')
const postalCode = ref('')
const city = ref('')

// Informations légales
const sirenNumber = ref('')
const tvaNumber = ref('')

const updateProfile = () => {
    console.log('Profil mis à jour')
}
</script>