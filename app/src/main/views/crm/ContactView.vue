<template>
    <div class="h-full flex flex-col bg-neutral-100">
        <div class="bg-white border-b">
            <div class="px-6 py-4 flex items-center justify-between">
                <div class="flex items-start space-x-2">
                    <Button variant="outline" @click="$router.go(-1)" class="h-9 w-9">
                        <ArrowLeft :size="20" />
                    </Button>
                    <template v-if="isDirty">
                        <Button @click="saveContact" variant="outline" :disabled="loading" class="w-9">
                            <Save class="h-4 w-4" />
                        </Button>
                        <Button variant="outline" @click="handleCancel" :disabled="loading" class="w-9">
                            <RotateCcw class="h-4 w-4" />
                        </Button>
                    </template>
                </div>
                <div class="flex items-center space-x-3">
                    <DropdownMenu>
                        <DropdownMenuTrigger as-child>
                            <Button variant="outline" class="h-9 w-9">
                                <MoreHorizontal :size="20" />
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                            <DropdownMenuItem @click="handleDelete">
                                <Trash class="h-4 w-4 text-destructive" />
                                Supprimer
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                    <Button variant="outline">
                        <MessageSquare class="h-4 w-4" />
                        Contacter
                    </Button>
                </div>
            </div>
        </div>

        <div class="flex-1 flex overflow-hidden lg:flex-row flex-col">
            <div class="w-full lg:w-1/4 xl:w-[500px] bg-white border-r overflow-y-auto">
                <div class="p-6">
                    <h2 class="text-lg font-semibold text-neutral-900 mb-4">Informations générales</h2>

                    <form @submit.prevent="saveContact" class="space-y-4">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Prénom</label>
                                <Input v-model="contactForm.first_name" class="mt-1" @input="checkDirty" />
                            </div>
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Nom</label>
                                <Input v-model="contactForm.last_name" class="mt-1" @input="checkDirty" />
                            </div>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Fonction</label>
                            <Input v-model="contactForm.function" class="mt-1" @input="checkDirty" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Entreprise</label>
                            <CompanySelect v-model="contactForm.company" class="mt-1"
                                @update:model-value="checkDirty" />
                        </div>

                        <Separator />

                        <h3 class="text-md font-medium text-neutral-700">Informations de contact</h3>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Email</label>
                            <Input v-model="contactForm.email" type="email" class="mt-1" @input="checkDirty" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Téléphone mobile</label>
                            <Input v-model="contactForm.mobile" class="mt-1" @input="checkDirty" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Téléphone fixe</label>
                            <Input v-model="contactForm.phone" class="mt-1" @input="checkDirty" />
                        </div>
                    </form>
                </div>
            </div>

            <div class="flex-1 overflow-y-auto p-6">
                <div class="bg-white mb-4 rounded-lg border">
                    <div class="p-6">
                        <div class="flex items-start justify-between">
                            <div class="flex items-start space-x-2">
                                <User class="h-8 w-8 text-neutral-400 mt-2 me-3" :stroke-width="1.2" />
                                <div class="flex flex-col">
                                    <h1 class="text-2xl font-semibold">{{ contact.full_name || `${contact.first_name}
                                        ${contact.last_name}`.trim() }}</h1>
                                    <p class="text-neutral-600" v-if="contact.function">{{ contact.function }}</p>
                                    <div class="flex items-center space-x-2 mt-1" v-if="contact.company">
                                        <Building class="h-4 w-4 text-neutral-500" />
                                        <router-link :to="`/company/${contact.company.id}`"
                                            class="text-neutral-600 hover:text-neutral-700 underline">
                                            {{ contact.company.name }}
                                        </router-link>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4 mb-4"
                    :class="{ 'grid-cols-3': workspaceStore.workspace?.use_subsites }">
                    <div class="bg-white p-4 rounded-lg border">
                        <div class="text-2xl font-semibold text-neutral-900">-</div>
                        <div class="text-sm text-neutral-600">Sites</div>
                    </div>
                    <div class="bg-white p-4 rounded-lg border">
                        <div class="text-2xl font-semibold text-neutral-900">-</div>
                        <div class="text-sm text-neutral-600">Interventions</div>
                    </div>
                    <div v-if="workspaceStore.workspace?.use_subsites" class="bg-white p-4 rounded-lg border">
                        <div class="text-2xl font-semibold text-neutral-900">-</div>
                        <div class="text-sm text-neutral-600">Lots</div>
                    </div>
                </div>

                <Tabs default-value="sites" class="mt-3">
                    <TabsList class="w-full mb-3 bg-neutral-200">
                        <TabsTrigger value="sites">Sites</TabsTrigger>
                        <TabsTrigger value="interventions">Interventions</TabsTrigger>
                        <TabsTrigger v-if="workspaceStore.workspace?.use_subsites" value="lots">Lots</TabsTrigger>
                    </TabsList>

                    <TabsContent value="sites" class="bg-white rounded-lg border">
                        <SitesTable :contact-id="contact.id" attachment-type="contact" />
                    </TabsContent>

                    <TabsContent value="interventions" class="bg-white rounded-lg border">
                        <div class="p-6">
                            <div class="text-center py-8">
                                <Wrench class="h-12 w-12 text-neutral-400 mx-auto mb-4" />
                                <h3 class="text-lg font-medium text-neutral-900 mb-2">Interventions</h3>
                                <p class="text-neutral-600 mb-4">Cette section permettra de consulter les interventions
                                    liées à
                                    ce contact.</p>
                                <p class="text-sm text-neutral-500">TODO: Implémenter la gestion des interventions</p>
                            </div>
                        </div>
                    </TabsContent>

                    <TabsContent v-if="workspaceStore.workspace?.use_subsites" value="lots"
                        class="bg-white rounded-lg border">
                        <div class="p-6">
                            <div class="text-center py-8">
                                <Package class="h-12 w-12 text-neutral-400 mx-auto mb-4" />
                                <h3 class="text-lg font-medium text-neutral-900 mb-2">Lots</h3>
                                <p class="text-neutral-600 mb-4">Cette section permettra de gérer les lots rattachés au
                                    contact.
                                </p>
                                <p class="text-sm text-neutral-500">TODO: Implémenter la gestion des lots</p>
                            </div>
                        </div>
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    </div>
</template>

<script setup>
import CompanySelect from '@/common/components/form/company-select/CompanySelect.vue'
import { Button } from '@/common/components/ui/button'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/common/components/ui/dropdown-menu'
import Input from '@/common/components/ui/input/Input.vue'
import { Separator } from '@/common/components/ui/separator'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/common/components/ui/tabs'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import SitesTable from '@/main/components/sites/SitesTable.vue'

import { useWorkspaceStore } from '@/main/stores/workspace'
import {
    ArrowLeft,
    Building,
    MessageSquare,
    MoreHorizontal,
    Package,
    RotateCcw,
    Save,
    Trash,
    User,
    Wrench
} from 'lucide-vue-next'
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const workspaceStore = useWorkspaceStore()

const route = useRoute()
const router = useRouter()
const fetcher = useFetcher()

const contactId = route.params.id
const contact = ref({})
const loading = ref(false)
const error = ref(null)
const isDirty = ref(false)
const originalForm = ref({})

useBus(bus, 'confirm-delete-contact:confirmed', () => {
    deleteContact()
})

const contactForm = reactive({
    first_name: '',
    last_name: '',
    function: '',
    company: null,
    email: '',
    mobile: '',
    phone: ''
})

const checkDirty = () => {
    isDirty.value = JSON.stringify(contactForm) !== JSON.stringify(originalForm.value)
}

const resetForm = (data) => {
    Object.assign(contactForm, {
        first_name: data.first_name || '',
        last_name: data.last_name || '',
        function: data.function || '',
        company: data.company?.id || null,
        email: data.email || '',
        mobile: data.mobile || '',
        phone: data.phone || ''
    })
    originalForm.value = JSON.parse(JSON.stringify(contactForm))
    isDirty.value = false
}

const handleCancel = () => {
    resetForm(contact.value)
}

const handleDelete = () => {
    if (!contactId || !contact.value.id) return

    bus.trigger('confirm-delete', {
        title: 'Supprimer le contact',
        message: 'Êtes-vous sûr de vouloir supprimer ce contact ?',
        itemName: contact.value.full_name || `${contact.value.first_name} ${contact.value.last_name}`.trim() || 'Contact sans nom',
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-contact:confirmed'
    })
}

const deleteContact = async () => {
    try {
        await fetcher.delete(`/contacts/${contactId}`)
        toast.success('Contact supprimé avec succès')
        bus.trigger('confirm-delete-dialog:close')
        router.push('/contacts')
    } catch (err) {
        console.error('Erreur lors de la suppression:', err)
        toast.error('Erreur lors de la suppression')
        bus.trigger('confirm-delete-dialog:close')
    }
}

const fetchContact = async () => {
    if (!contactId) return

    loading.value = true
    error.value = null

    try {
        const response = await fetcher.get(`/contacts/${contactId}`)
        contact.value = response.data
        resetForm(contact.value)
    } catch (err) {
        console.error('Erreur lors du chargement du contact:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const saveContact = async () => {
    if (!contactId) return

    loading.value = true
    error.value = null

    try {
        const submitData = { ...contactForm }

        if (typeof submitData.company === 'object' && submitData.company?.id) {
            submitData.company = submitData.company.id
        }

        const response = await fetcher.put(`/contacts/${contactId}`, submitData)
        contact.value = response.data
        resetForm(contact.value)
        toast.success('Contact sauvegardé avec succès')
    } catch (err) {
        console.error('Erreur lors de la sauvegarde:', err)
        error.value = err
        toast.error('Erreur lors de la sauvegarde')
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchContact()
})
</script>