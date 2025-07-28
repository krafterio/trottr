<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between mb-0">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Contacts</h1>
                    <p class="text-neutral-600">Gestion des contacts</p>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline">
                        <Download class="h-4 w-4" />
                        Exporter
                    </Button>
                    <Button @click="handleCreate">
                        <Plus class="h-4 w-4" />
                        Nouveau contact
                    </Button>
                </div>
            </div>
        </div>

        <div class="flex-1 flex overflow-hidden">
            <div :class="[
                'bg-neutral-50 border-r overflow-y-auto',
                showFilters ? 'w-64 p-4' : 'w-16 p-2 pt-4 cursor-pointer hover:bg-neutral-100'
            ]" @click="!showFilters && toggleFilters()">

                <div v-if="showFilters" class="flex items-center justify-between mb-4">
                    <h3 class="font-semibold text-neutral-900">Filtres</h3>
                    <Button variant="ghost" size="sm" class="h-6 w-6 p-0 cursor-pointer" @click.stop="toggleFilters">
                        <PanelLeftClose class="h-4 w-4" />
                    </Button>
                </div>

                <div v-else class="flex flex-col items-center mb-4">
                    <Button variant="ghost" size="sm" class="h-6 w-6 p-0 mb-2 cursor-pointer"
                        @click.stop="toggleFilters">
                        <PanelLeftOpen class="h-4 w-4" />
                    </Button>
                    <h3 class="font-semibold text-neutral-900 transform -rotate-90 origin-center mt-4">
                        Filtres
                    </h3>
                </div>

                <div v-show="showFilters" class="space-y-6">
                    <Button variant="outline" size="sm" class="w-full" @click="resetFilters">
                        <RotateCcw class="h-4 w-4 mr-2" />
                        Réinitialiser
                    </Button>
                </div>
            </div>

            <div class="flex-1 overflow-y-auto pb-16">
                <div class="px-6 py-4 border-b">
                    <div class="flex items-center justify-between">
                        <div class="relative">
                            <Search
                                class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-neutral-400" />
                            <Input type="text" placeholder="Rechercher un contact..." class="h-9 pl-10 pr-4 py-2 w-64"
                                v-model="searchQuery" @input="handleSearch" />
                        </div>
                        <span class="text-sm text-muted-foreground">{{ totalItems }} contacts</span>
                    </div>
                </div>

                <div v-if="loading" class="flex-1 flex items-center justify-center py-12">
                    <div class="text-center">
                        <div
                            class="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full mx-auto mb-4">
                        </div>
                        <p class="text-neutral-600">Chargement...</p>
                    </div>
                </div>

                <div v-else-if="contacts.length === 0" class="flex-1 flex items-center justify-center py-12">
                    <div class="text-center py-8">
                        <div
                            class="w-16 h-16 mx-auto mb-4 bg-neutral-100 rounded-full flex items-center justify-center">
                            <Users class="w-8 h-8 text-neutral-400" :stroke-width="1.2" />
                        </div>
                        <h3 class="text-lg font-semibold text-neutral-900 mb-2">Créez votre premier contact
                        </h3>
                        <p class="text-neutral-600 mb-6 max-w-md mx-auto">
                            Les contacts sont essentiels pour gérer vos relations clients.
                            Ajoutez vos premiers contacts pour organiser votre réseau professionnel.
                        </p>
                        <Button @click="handleCreate" class="inline-flex items-center">
                            <Plus class="w-4 h-4 mr-2" />
                            Ajouter un contact
                        </Button>
                    </div>
                </div>

                <div v-else>
                    <Table>
                        <TableHeader>
                            <TableRow class="bg-neutral-50 border-b uppercase tracking-wider text-xs text-neutral-500">
                                <TableHead class="ps-3 w-8">
                                    <Checkbox v-model="selectAll" @update:model-value="toggleSelectAll" />
                                </TableHead>
                                <TableHead>Nom / Prénom</TableHead>
                                <TableHead>Société</TableHead>
                                <TableHead>Fonction</TableHead>
                                <TableHead>Email</TableHead>
                                <TableHead>Mobile</TableHead>
                                <TableHead>Téléphone</TableHead>
                                <TableHead class="w-10"></TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            <TableRow v-for="contact in contacts" :key="contact.id" class="hover:bg-neutral-50">
                                <TableCell @click.stop class="ps-3">
                                    <Checkbox :checked="selectedContacts.includes(contact.id)"
                                        @update:checked="toggleContactSelection(contact.id)" />
                                </TableCell>
                                <TableCell class="font-medium text-neutral-900">
                                    <router-link :to="`/contact/${contact.id}`"
                                        class="text-neutral-900 hover:text-neutral-700 underline">
                                        {{ contact.full_name || `${contact.first_name} ${contact.last_name}`.trim() }}
                                    </router-link>
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    <router-link v-if="contact.company" :to="`/company/${contact.company.id}`"
                                        class="text-neutral-900 hover:text-neutral-700 underline">
                                        {{ contact.company.name }}
                                    </router-link>
                                    <span v-else class="text-neutral-500">-</span>
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ contact.function || '-' }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ contact.email || '-' }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ contact.mobile || '-' }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ contact.phone || '-' }}
                                </TableCell>
                                <TableCell @click.stop>
                                    <DropdownMenu>
                                        <DropdownMenuTrigger as-child>
                                            <Button variant="ghost" size="sm" class="h-8 w-8 p-0">
                                                <MoreVertical class="h-4 w-4" />
                                            </Button>
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent align="end">
                                            <DropdownMenuItem @click="handleView(contact)">
                                                <Eye class="mr-2 h-4 w-4" />
                                                Voir
                                            </DropdownMenuItem>
                                            <DropdownMenuItem @click="handleDelete(contact)" class="text-red-600">
                                                <Trash class="mr-2 h-4 w-4" />
                                                Supprimer
                                            </DropdownMenuItem>
                                        </DropdownMenuContent>
                                    </DropdownMenu>
                                </TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </div>

            </div>
        </div>

        <TablePagination :current-page="currentPage" :total-pages="totalPages" :total-items="totalItems"
            :items-per-page="itemsPerPage"
            :position-classes="showFilters ? 'bottom-0 left-80 right-0' : 'bottom-0 left-32 right-0'"
            @page-change="handlePageChange" @items-per-page-change="handleItemsPerPageChange" />
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { Checkbox } from '@/common/components/ui/checkbox'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/common/components/ui/dropdown-menu'
import { Input } from '@/common/components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/common/components/ui/table'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import TablePagination from '@/main/components/TablePagination.vue'
import { usePreferencesStore } from '@/main/stores/preferences'
import { debounce } from 'lodash'
import { Download, Eye, MoreVertical, PanelLeftClose, PanelLeftOpen, Plus, RotateCcw, Search, Trash, Users } from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const router = useRouter()
const fetcher = useFetcher()
const preferencesStore = usePreferencesStore()

const contacts = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const itemsPerPage = ref(50)
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const selectedContacts = ref([])
const selectedContactForDelete = ref(null)

const showFilters = computed({
    get() {
        return preferencesStore.getPreference('display_filters', true)
    },
    set(value) {
        preferencesStore.updatePreference('display_filters', value)
        toast.success('Préférences mises à jour')
    }
})

const selectAll = computed({
    get() {
        return contacts.value.length > 0 && selectedContacts.value.length === contacts.value.length
    },
    set(value) {
        if (value) {
            selectedContacts.value = contacts.value.map(c => c.id)
        } else {
            selectedContacts.value = []
        }
    }
})

const toggleFilters = () => {
    showFilters.value = !showFilters.value
}

const resetFilters = () => {
    fetchContacts()
}

const fetchContacts = async () => {
    loading.value = true
    error.value = null

    try {
        const params = {
            page: currentPage.value,
            per_page: itemsPerPage.value
        }

        const response = await fetcher.get('/contacts', { params })
        contacts.value = response.data.items || []
        totalItems.value = response.data.total || 0
        totalPages.value = response.data.total_pages || 1
        currentPage.value = response.data.page || 1
    } catch (err) {
        console.error('Erreur lors du chargement des contacts:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const searchContacts = async (query) => {
    if (!query || query.trim().length < 2) {
        currentPage.value = 1
        fetchContacts()
        return
    }

    loading.value = true
    error.value = null

    try {
        const params = {
            q: query.trim(),
            page: currentPage.value,
            per_page: itemsPerPage.value
        }

        const response = await fetcher.get('/contacts/quick_search', { params })
        contacts.value = response.data.items || []
        totalItems.value = response.data.total || 0
        totalPages.value = response.data.total_pages || 1
        currentPage.value = response.data.page || 1
    } catch (err) {
        console.error('Erreur lors de la recherche:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const debouncedSearchContacts = debounce(searchContacts, 300)

const handleCreate = () => {
    bus.trigger('open-contact-dialog')
}

const handleRowClick = (contact) => {
    router.push(`/contact/${contact.id}`)
}

const handleView = (contact) => {
    router.push(`/contact/${contact.id}`)
}

const handleSearch = () => {
    debouncedSearchContacts(searchQuery.value)
}

const handlePageChange = (page) => {
    currentPage.value = page
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchContacts(searchQuery.value)
    } else {
        fetchContacts()
    }
}

const handleItemsPerPageChange = (itemsCount) => {
    itemsPerPage.value = parseInt(itemsCount)
    currentPage.value = 1
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchContacts(searchQuery.value)
    } else {
        fetchContacts()
    }
}

const toggleSelectAll = () => {
    selectAll.value = !selectAll.value
}

const toggleContactSelection = (contactId) => {
    const index = selectedContacts.value.indexOf(contactId)
    if (index > -1) {
        selectedContacts.value.splice(index, 1)
    } else {
        selectedContacts.value.push(contactId)
    }
}

const handleDelete = (contact) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer le contact',
        message: 'Êtes-vous sûr de vouloir supprimer ce contact ?',
        itemName: contact.full_name || `${contact.first_name} ${contact.last_name}`.trim(),
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-contact:confirmed'
    })

    selectedContactForDelete.value = contact
}

const deleteContact = async () => {
    if (!selectedContactForDelete.value) return

    try {
        await fetcher.delete(`/contacts/${selectedContactForDelete.value.id}`)
        toast.success('Contact supprimé avec succès')
        bus.trigger('confirm-delete-dialog:close')
        refreshList()
        selectedContactForDelete.value = null
    } catch (err) {
        console.error('Erreur lors de la suppression:', err)
        toast.error('Erreur lors de la suppression')
        bus.trigger('confirm-delete-dialog:close')
    }
}

const refreshList = () => {
    selectedContacts.value = []
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchContacts(searchQuery.value)
    } else {
        fetchContacts()
    }
}

useBus(bus, 'contact-saved', () => {
    refreshList()
})

useBus(bus, 'contact-created-stay', () => {
    refreshList()
})

useBus(bus, 'confirm-delete-contact:confirmed', () => {
    deleteContact()
})

onMounted(() => {
    fetchContacts()
})
</script>