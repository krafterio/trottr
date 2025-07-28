export const companiesColumns = [
    {
        key: 'name',
        label: 'Entreprise',
        classes: 'font-medium text-neutral-900',
        hideable: false
    },
    {
        key: 'company_type',
        label: 'Type',
        type: 'badge',
        variant: 'outline'
    },
    {
        key: 'reference',
        label: 'Référence',
        classes: 'text-neutral-900'
    },
    {
        key: 'invoice_street',
        label: 'Adresse',
        classes: 'text-neutral-900'
    },
    {
        key: 'invoice_city',
        label: 'Ville',
        classes: 'text-neutral-900'
    },
    {
        key: 'phone',
        label: 'Téléphone',
        classes: 'text-neutral-900'
    },
    {
        key: 'email',
        label: 'Email',
        classes: 'text-neutral-900'
    },
    {
        key: 'siret',
        label: 'SIRET',
        classes: 'text-neutral-900'
    }
]

export const companiesConfig = {
    title: 'Entreprises',
    subtitle: 'Gestion des entreprises clientes',
    enableExport: true,
    enableCreate: true,
    enableSelection: true,
    createButtonText: 'Nouvelle entreprise',
    searchPlaceholder: 'Rechercher une entreprise...',
    itemsLabel: 'entreprises'
}

import { useCompany } from '@/common/composables/useCompany'

const { getCompanyTypeOptions } = useCompany()

export const companiesFilters = [
    {
        key: 'company_type',
        label: 'Type',
        options: getCompanyTypeOptions()
    }
]

export const companiesKpis = [
    {
        key: 'total',
        label: 'Total',
        value: 147,
        icon: 'Building'
    },
    {
        key: 'active',
        label: 'Actives',
        value: 132,
        icon: 'CheckCircle'
    },
    {
        key: 'pending',
        label: 'En attente',
        value: 12,
        icon: 'Clock'
    },
    {
        key: 'suspended',
        label: 'Suspendues',
        value: 3,
        icon: 'AlertTriangle'
    }
] 