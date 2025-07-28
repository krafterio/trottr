export const sitesColumns = [
    {
        key: 'name',
        label: 'Nom du site',
        classes: 'font-medium text-neutral-900',
        hideable: false
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
        accessor: (site) => site.company?.name || '-',
        classes: 'text-neutral-900'
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

import { useSite } from '@/common/composables/useSite'

const { getSiteBuildingTypeOptions } = useSite()

export const sitesFilters = [
    {
        key: 'building_type',
        label: 'Type de bâtiment',
        options: getSiteBuildingTypeOptions()
    }
] 