export function useSite() {
    const buildingTypes = {
        'residence_collective': 'Résidence collective',
        'maison_individuelle': 'Maison individuelle',
        'batiment_tertiaire': 'Bâtiment tertiaire',
        'local_commercial': 'Local commercial',
        'autre': 'Autre'
    }

    const getSiteBuildingTypeLabel = (type) => {
        return buildingTypes[type] || type
    }

    const getSiteBuildingTypeOptions = () => {
        return Object.entries(buildingTypes).map(([value, label]) => ({
            value,
            label
        }))
    }

    return {
        buildingTypes,
        getSiteBuildingTypeLabel,
        getSiteBuildingTypeOptions
    }
} 