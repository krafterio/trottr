<script setup>
import { Button } from '@/common/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from 'lucide-vue-next'

const props = defineProps({
    currentPage: {
        type: Number,
        default: 1
    },
    totalPages: {
        type: Number,
        default: 1
    },
    totalItems: {
        type: Number,
        default: 0
    },
    itemsPerPage: {
        type: Number,
        default: 10
    },
    positionClasses: {
        type: String,
        default: 'bottom-0 left-80 right-0'
    }
})

const emit = defineEmits(['page-change', 'items-per-page-change'])

const goToPage = (page) => {
    if (page >= 1 && page <= props.totalPages) {
        emit('page-change', page)
    }
}

const changeItemsPerPage = (value) => {
    emit('items-per-page-change', parseInt(value))
}

const startItem = (props.currentPage - 1) * props.itemsPerPage + 1
const endItem = Math.min(props.currentPage * props.itemsPerPage, props.totalItems)
</script>

<template>
    <div :class="['fixed z-50 bg-white border-t border-gray-200 px-6 py-3', positionClasses]">
        <div class="flex items-center justify-between">
            <!-- Informations sur les éléments -->
            <div class="flex items-center space-x-6">
                <div class="text-sm text-gray-700">
                    Affichage de {{ startItem }} à {{ endItem }} sur {{ totalItems }} résultats
                </div>

                <!-- Sélecteur d'éléments par page -->
                <div class="flex items-center space-x-2">
                    <span class="text-sm text-gray-700">Afficher</span>
                    <Select :model-value="itemsPerPage.toString()" @update:model-value="changeItemsPerPage">
                        <SelectTrigger class="w-20 h-8">
                            <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="10">10</SelectItem>
                            <SelectItem value="25">25</SelectItem>
                            <SelectItem value="50">50</SelectItem>
                            <SelectItem value="100">100</SelectItem>
                        </SelectContent>
                    </Select>
                    <span class="text-sm text-gray-700">par page</span>
                </div>
            </div>

            <!-- Contrôles de pagination -->
            <div class="flex items-center space-x-2">
                <!-- Première page -->
                <Button variant="outline" size="sm" :disabled="currentPage === 1" @click="goToPage(1)"
                    class="h-8 w-8 p-0">
                    <ChevronsLeft class="h-4 w-4" />
                </Button>

                <!-- Page précédente -->
                <Button variant="outline" size="sm" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)"
                    class="h-8 w-8 p-0">
                    <ChevronLeft class="h-4 w-4" />
                </Button>

                <!-- Numéros de pages -->
                <div class="flex items-center space-x-1">
                    <template v-for="page in Math.min(5, totalPages)" :key="page">
                        <Button variant="outline" size="sm" :class="[
                            'h-8 w-8 p-0',
                            currentPage === page ? 'bg-primary text-white border-primary' : ''
                        ]" @click="goToPage(page)">
                            {{ page }}
                        </Button>
                    </template>

                    <span v-if="totalPages > 5" class="text-sm text-gray-500 px-2">
                        ...
                    </span>

                    <Button v-if="totalPages > 5 && currentPage < totalPages - 2" variant="outline" size="sm"
                        class="h-8 w-8 p-0" @click="goToPage(totalPages)">
                        {{ totalPages }}
                    </Button>
                </div>

                <!-- Page suivante -->
                <Button variant="outline" size="sm" :disabled="currentPage === totalPages"
                    @click="goToPage(currentPage + 1)" class="h-8 w-8 p-0">
                    <ChevronRight class="h-4 w-4" />
                </Button>

                <!-- Dernière page -->
                <Button variant="outline" size="sm" :disabled="currentPage === totalPages" @click="goToPage(totalPages)"
                    class="h-8 w-8 p-0">
                    <ChevronsRight class="h-4 w-4" />
                </Button>
            </div>
        </div>
    </div>
</template>