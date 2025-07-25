<template>
    <div>
        <div class="container mx-auto pt-6 px-5">
            <div class="mb-6 flex items-center justify-between">
                <div>
                    <h1 class="text-3xl font-bold mb-2">Pays</h1>
                    <p class="text-gray-600">Gestion des pays</p>
                </div>
                <Button @click="openCountryModal">
                    <Plus :size="16" class="mr-2" />
                    Ajouter un pays
                </Button>
            </div>

            <Card class="shadow-none py-5">
                <CardContent class="px-5 py-0">
                    <div class="rounded-md border">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Nom</TableHead>
                                    <TableHead>Code ISO</TableHead>
                                    <TableHead class="w-20"></TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                <TableRow v-if="loadingTable">
                                    <TableCell colspan="3" class="text-center py-8">
                                        <div class="flex items-center justify-center space-x-2">
                                            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-900"></div>
                                            <span>Chargement...</span>
                                        </div>
                                    </TableCell>
                                </TableRow>
                                <TableRow v-else-if="countries.length === 0">
                                    <TableCell colspan="3" class="text-center py-8 text-gray-500">
                                        Aucun pays trouvé
                                    </TableCell>
                                </TableRow>
                                <TableRow v-else v-for="country in countries" :key="country.id" class="hover:bg-gray-50">
                                    <TableCell>
                                        <span class="font-medium">{{ country.name }}</span>
                                    </TableCell>
                                    <TableCell>
                                        <span class="font-mono text-sm text-gray-600">{{ country.iso_code }}</span>
                                    </TableCell>
                                    <TableCell>
                                        <DropdownMenu>
                                            <DropdownMenuTrigger as-child>
                                                <Button variant="ghost" size="sm" class="h-8 w-8 p-0">
                                                    <MoreHorizontal weight="bold" class="h-4 w-4" />
                                                </Button>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent align="end">
                                                <DropdownMenuItem @click="editCountry(country)">
                                                    <Pencil class="mr-2 h-4 w-4" />
                                                    Modifier
                                                </DropdownMenuItem>
                                                <DropdownMenuSeparator />
                                                <DropdownMenuItem 
                                                    @click="confirmDelete(country)" 
                                                    class="text-red-600 focus:text-red-600"
                                                >
                                                    <Trash2 class="mr-2 h-4 w-4" />
                                                    Supprimer
                                                </DropdownMenuItem>
                                            </DropdownMenuContent>
                                        </DropdownMenu>
                                    </TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </div>

                    <div class="flex items-center justify-between mt-4">
                        <div class="text-sm text-gray-500">
                            Affichage de {{ ((page - 1) * itemsPerPage) + 1 }} à {{ Math.min(page * itemsPerPage, total) }} sur {{ total }} résultats
                        </div>
                        <div class="flex items-center space-x-2">
                            <Button 
                                variant="outline" 
                                size="sm" 
                                @click="previousPage" 
                                :disabled="page === 1"
                            >
                                Précédent
                            </Button>
                            <span class="text-sm text-gray-500">
                                Page {{ page }} sur {{ Math.ceil(total / itemsPerPage) }}
                            </span>
                            <Button 
                                variant="outline" 
                                size="sm" 
                                @click="nextPage" 
                                :disabled="page >= Math.ceil(total / itemsPerPage)"
                            >
                                Suivant
                            </Button>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>

        <CountryModal v-model:show="countryModal" :country="selectedCountry" @saved="onCountrySaved" @deleted="onCountryDeleted" />

        <AlertDialog v-model:open="deleteModal">
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>Confirmation de suppression</AlertDialogTitle>
                    <AlertDialogDescription>
                        Êtes-vous sûr de vouloir supprimer le pays "{{ selectedCountryForDelete?.name }}" ? 
                        Cette action est irréversible.
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel>Annuler</AlertDialogCancel>
                    <AlertDialogAction 
                        @click="deleteCountry" 
                        :disabled="deleting"
                        class="bg-red-600 hover:bg-red-700"
                    >
                        <span v-if="deleting" class="flex items-center">
                            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                            Suppression...
                        </span>
                        <span v-else>Supprimer</span>
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Trash2, Pencil } from 'lucide-vue-next'
import CountryModal from '@/admin/components/modals/CountryModal.vue'
import { useFetcher } from "@/common/composables/fetcher"
import { toast } from 'vue-sonner'
import { Card, CardContent } from '@/common/components/ui/card'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/common/components/ui/table'
import { Button } from '@/common/components/ui/button'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/common/components/ui/dropdown-menu'
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from '@/common/components/ui/alert-dialog'
import { MoreHorizontal } from 'lucide-vue-next'

const fetcher = useFetcher()

const loadingTable = ref(false)
const countries = ref([])
const total = ref(0)
const page = ref(1)
const itemsPerPage = ref(50)
const countryModal = ref(false)
const selectedCountry = ref(null)
const deleteModal = ref(false)
const selectedCountryForDelete = ref(null)
const deleting = ref(false)

const fetchCountries = async () => {
    loadingTable.value = true

    try {
        const params = {
            limit: itemsPerPage.value,
            offset: (page.value - 1) * itemsPerPage.value,
        }

        const { data } = await fetcher.get('/countries', { params })
        countries.value = data.items
        total.value = data.total
    } catch (error) {
        console.error('Erreur lors de la récupération des pays:', error)
        toast.error('Erreur lors du chargement des pays')
    } finally {
        loadingTable.value = false
    }
}

const openCountryModal = () => {
    selectedCountry.value = null
    countryModal.value = true
}

const editCountry = (country) => {
    selectedCountry.value = country
    countryModal.value = true
}

const confirmDelete = (country) => {
    selectedCountryForDelete.value = country
    deleteModal.value = true
}

const deleteCountry = async () => {
    if (!selectedCountryForDelete.value) {
        return
    }

    deleting.value = true

    try {
        await fetcher.delete(`/countries/${selectedCountryForDelete.value.id}`)
        toast.success(`Pays "${selectedCountryForDelete.value.name}" supprimé avec succès`)
        deleteModal.value = false
        fetchCountries()
    } catch (error) {
        console.error('Erreur:', error)
        toast.error('Erreur lors de la suppression')
    } finally {
        deleting.value = false
    }
}

const onCountrySaved = () => {
    fetchCountries()
    countryModal.value = false
}

const onCountryDeleted = () => {
    fetchCountries()
    countryModal.value = false
}

const previousPage = () => {
    if (page.value > 1) {
        page.value--
        fetchCountries()
    }
}

const nextPage = () => {
    if (page.value < Math.ceil(total.value / itemsPerPage.value)) {
        page.value++
        fetchCountries()
    }
}

onMounted(() => {
    fetchCountries()
})
</script>