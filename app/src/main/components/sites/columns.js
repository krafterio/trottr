import { useSite } from '@/common/composables/useSite'
import CellLink from '../CellLink.vue'

export const sitesColumns = [
    {
        key: 'name',
        label: 'Nom du site',
        hideable: false,
        component: CellLink,
        componentProps: (item) => ({
            href: `/site/${item.id}`,
            text: item.name,
            linkClass: 'font-medium text-sm text-neutral-900 hover:text-neutral-700 underline'
        })
    },
    {
        key: 'building_type',
        label: 'Type de bâtiment',
        type: 'badge',
        variant: 'outline',
        accessor: (site) => {
            const { getSiteBuildingTypeLabel } = useSite()
            return getSiteBuildingTypeLabel(site.building_type)
        }
    },
    {
        key: 'street',
        label: 'Adresse',
        classes: 'text-neutral-900'
    },
    {
        key: 'city',
        label: 'Ville',
        classes: 'text-neutral-900'
    },
    {
        key: 'zip',
        label: 'Code postal',
        classes: 'text-neutral-900'
    },
    {
        key: 'country',
        label: 'Pays',
        accessor: (site) => site.country?.name || '-',
        classes: 'text-neutral-900'
    },
    {
        key: 'company',
        label: 'Entreprise',
        component: CellLink,
        componentProps: (item) => {
            if (item.company) {
                return {
                    to: `/companies/${item.company.id}`,
                    text: item.company.name,
                    linkClass: 'text-sm text-neutral-900 hover:text-neutral-700 underline'
                }
            }
            return null
        },
        accessor: (site) => site.company?.name || '-',
        classes: 'text-neutral-500'
    }
]

export const sitesConfig = {
    title: 'Sites d\'intervention',
    subtitle: 'Gestion des sites d\'intervention',
    enableExport: true,
    enableCreate: true,
    enableSelection: true,
    createButtonText: 'Nouveau site',
    searchPlaceholder: 'Rechercher un site...',
    itemsLabel: 'sites'
}

const { getSiteBuildingTypeOptions } = useSite()

export const sitesFilters = [
    {
        key: 'building_type',
        label: 'Type de bâtiment',
        options: getSiteBuildingTypeOptions()
    }
] 