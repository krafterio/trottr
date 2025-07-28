
export function useCompany() {
  const companyTypes = {
    'client_final': 'Client final',
    'regie_gestionnaire': 'Régie / Gestionnaire',
    'donneur_ordre': 'Donneur d\'ordre',
    'sous_traitant': 'Sous-traitant',
    'fournisseur': 'Fournisseur',
    'autre': 'Autre'
  }

  const getCompanyTypeLabel = (type) => {
    return companyTypes[type] || type
  }

  const getCompanyTypeOptions = () => {
    return Object.entries(companyTypes).map(([value, label]) => ({
      value,
      label
    }))
  }

  return {
    companyTypes,
    getCompanyTypeLabel,
    getCompanyTypeOptions
  }
} 