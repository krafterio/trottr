<template>
    <div class="p-6">
        <div v-if="loading" class="text-center py-8">
            <div class="animate-spin w-8 h-8 border-2 border-neutral-300 border-t-neutral-900 rounded-full mx-auto">
            </div>
            <p class="text-neutral-600 mt-4">Chargement des contacts...</p>
        </div>

        <div v-else-if="contacts.length === 0" class="text-center py-8">
            <Users class="h-12 w-12 text-neutral-400 mx-auto mb-4" />
            <h3 class="text-lg font-medium text-neutral-900 mb-2">Aucun contact</h3>
            <p class="text-neutral-600 mb-4">Cette entreprise n'a pas encore de contacts associés.</p>
            <Button @click="handleCreateContact" class="inline-flex items-center">
                <Plus class="w-4 h-4" />
                Ajouter un contact
            </Button>
        </div>

        <div v-else class="space-y-4">
            <div class="flex items-center justify-between">
                <h3 class="text-lg font-medium text-neutral-900">Contacts ({{ contacts.length }})</h3>
                <Button @click="handleCreateContact" size="sm" class="inline-flex items-center">
                    <Plus class="w-4 h-4" />
                    Ajouter un contact
                </Button>
            </div>

            <div class="border rounded-lg overflow-hidden">
                <table class="w-full">
                    <thead class="bg-neutral-50 border-b">
                        <tr>
                            <th
                                class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                Nom / Prénom
                            </th>
                            <th
                                class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                Fonction
                            </th>
                            <th
                                class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                Email
                            </th>
                            <th
                                class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                Téléphone
                            </th>
                            <th
                                class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-neutral-200">
                        <tr v-for="contact in contacts" :key="contact.id" class="hover:bg-neutral-50">
                            <td class="px-4 py-3">
                                <div class="text-sm font-medium text-neutral-900">
                                    {{ contact.full_name || `${contact.first_name} ${contact.last_name}`.trim() }}
                                </div>
                            </td>
                            <td class="px-4 py-3">
                                <div class="text-sm text-neutral-900">{{ contact.function || '-' }}</div>
                            </td>
                            <td class="px-4 py-3">
                                <div class="text-sm text-neutral-900">{{ contact.email || '-' }}</div>
                            </td>
                            <td class="px-4 py-3">
                                <div class="text-sm text-neutral-900">{{ contact.mobile || contact.phone || '-' }}</div>
                                <div v-if="contact.mobile && contact.phone" class="text-sm text-neutral-500">{{
                                    contact.phone }}</div>
                            </td>
                            <td class="px-4 py-3">
                                <div class="flex items-center space-x-2">
                                    <Button variant="ghost" size="sm" @click="viewContact(contact)">
                                        <Eye class="w-4 h-4" />
                                    </Button>
                                    <Button variant="ghost" size="sm" @click="editContact(contact)">
                                        <Edit class="w-4 h-4" />
                                    </Button>
                                    <Button variant="ghost" size="sm" @click="deleteContact(contact)">
                                        <Trash class="w-4 h-4 text-destructive" />
                                    </Button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { Edit, Eye, Plus, Trash, Users } from 'lucide-vue-next'
import { onMounted, ref, watch } from 'vue'
import { toast } from 'vue-sonner'

const props = defineProps({
    companyId: {
        type: Number,
        required: true
    }
})

const fetcher = useFetcher()

const contacts = ref([])
const loading = ref(false)
const selectedContactForDelete = ref(null)

const fetchContacts = async () => {
    if (!props.companyId) return

    loading.value = true
    try {
        const response = await fetcher.get('/contacts', {
            params: {
                company: props.companyId,
                per_page: 100
            }
        })
        contacts.value = response.data.items || []
    } catch (error) {
        console.error('Erreur lors du chargement des contacts:', error)
        toast.error('Erreur lors du chargement des contacts')
    } finally {
        loading.value = false
    }
}

const handleCreateContact = () => {
    bus.trigger('open-contact-dialog', { company_id: props.companyId })
}

const viewContact = (contact) => {
    console.log('View contact:', contact)
}

const editContact = (contact) => {
    bus.trigger('open-contact-dialog', contact)
}

const deleteContact = (contact) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer le contact',
        message: 'Êtes-vous sûr de vouloir supprimer ce contact ?',
        itemName: contact.full_name || `${contact.first_name} ${contact.last_name}`.trim(),
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-contact:confirmed'
    })

    selectedContactForDelete.value = contact
}

const performDeleteContact = async () => {
    if (!selectedContactForDelete.value) return

    try {
        await fetcher.delete(`/contacts/${selectedContactForDelete.value.id}`)
        toast.success('Contact supprimé avec succès')
        fetchContacts()

        bus.trigger('contact:deleted', {
            contactId: selectedContactForDelete.value.id,
            contactName: selectedContactForDelete.value.full_name || `${selectedContactForDelete.value.first_name} ${selectedContactForDelete.value.last_name}`.trim()
        })

        selectedContactForDelete.value = null
        bus.trigger('confirm-delete-dialog:close')
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression')
        bus.trigger('confirm-delete-dialog:close')
    }
}

useBus(bus, 'confirm-delete-contact:confirmed', () => {
    performDeleteContact()
})

useBus(bus, 'contact-saved', () => {
    fetchContacts()
})

useBus(bus, 'contact-created-stay', () => {
    fetchContacts()
})

watch(() => props.companyId, (newId) => {
    if (newId) {
        fetchContacts()
    }
}, { immediate: true })

onMounted(() => {
    fetchContacts()
})
</script>