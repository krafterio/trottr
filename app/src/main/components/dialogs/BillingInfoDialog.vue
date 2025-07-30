<template>
    <Dialog v-model:open="open">
        <DialogContent class="sm:max-w-md">
            <DialogHeader>
                <DialogTitle>Informations de facturation</DialogTitle>
                <DialogDescription>
                    Modifiez les informations de facturation de votre workspace
                </DialogDescription>
            </DialogHeader>
            
            <form @submit.prevent="updateBillingInfo" class="space-y-4">
                <div class="space-y-4">
                    <div>
                        <Label for="name">Nom de l'entreprise</Label>
                        <Input
                            id="name"
                            v-model="form.name"
                            placeholder="Nom de votre entreprise"
                        />
                    </div>
                    
                    <div>
                        <Label for="street">Adresse</Label>
                        <Input
                            id="street"
                            v-model="form.street"
                            placeholder="Adresse"
                        />
                    </div>
                    
                    <div>
                        <Label for="street2">Complément d'adresse</Label>
                        <Input
                            id="street2"
                            v-model="form.street2"
                            placeholder="Complément d'adresse (optionnel)"
                        />
                    </div>
                    
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <Label for="zip">Code postal</Label>
                            <Input
                                id="zip"
                                v-model="form.zip"
                                placeholder="Code postal"
                            />
                        </div>
                        <div>
                            <Label for="city">Ville</Label>
                            <Input
                                id="city"
                                v-model="form.city"
                                placeholder="Ville"
                            />
                        </div>
                    </div>
                    
                    <div>
                        <Label for="country">Pays</Label>
                        <CountrySelect
                            v-model="form.country"
                            placeholder="Sélectionner un pays"
                        />
                    </div>
                    
                    <div>
                        <Label for="siren">SIREN</Label>
                        <Input
                            id="siren"
                            v-model="form.siren"
                            placeholder="Numéro SIREN"
                        />
                    </div>
                    
                    <div>
                        <Label for="vat">Numéro TVA</Label>
                        <Input
                            id="vat"
                            v-model="form.vat"
                            placeholder="Numéro de TVA"
                        />
                    </div>
                </div>
                
                <DialogFooter>
                    <Button 
                        type="button" 
                        variant="outline" 
                        @click="open = false"
                        :disabled="loading"
                    >
                        Annuler
                    </Button>
                    <Button 
                        type="submit" 
                        :disabled="loading"
                    >
                        {{ loading ? 'Sauvegarde...' : 'Sauvegarder' }}
                    </Button>
                </DialogFooter>
            </form>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Button } from '@/common/components/ui/button'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { Input } from '@/common/components/ui/input'
import { Label } from '@/common/components/ui/label'
import { useFetcher } from '@/common/composables/fetcher'
import CountrySelect from '@/common/components/form/country-select/CountrySelect.vue'

const fetcher = useFetcher()
const open = defineModel('open', { default: false })

const loading = ref(false)
const form = ref({
    name: '',
    street: '',
    street2: '',
    zip: '',
    city: '',
    country: null,
    siren: '',
    vat: ''
})

const fetchWorkspace = async () => {
    try {
        const response = await fetcher.get('/workspace')
        const workspace = response.data

        form.value = {
            name: workspace.name || '',
            street: workspace.street || '',
            street2: workspace.street2 || '',
            zip: workspace.zip || '',
            city: workspace.city || '',
            country: workspace.country?.id || null,
            siren: workspace.siren || '',
            vat: workspace.vat || ''
        }
    } catch (err) {
        console.error('Erreur lors de la récupération du workspace:', err)
    }
}

watch(open, (isOpen) => {
    if (isOpen) {
        fetchWorkspace()
    }
})

const updateBillingInfo = async () => {
    try {
        loading.value = true
        const value = {...form.value}
        value.country_id = value.country?.id || value.country || null
        
        await fetcher.patch('/workspace', value)
        
        open.value = false
    } catch (err) {
        console.error('Erreur lors de la mise à jour:', err)
    } finally {
        loading.value = false
    }
}
</script> 
