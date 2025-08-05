import { toast } from 'vue-sonner'
import { useFetcher } from './fetcher'

export function useUnavailability() {
    const fetcher = useFetcher()

    const getUnavailabilityTypeLabel = (type) => {
        const labels = {
            disease: 'Maladie',
            training: 'Formation',
            paid_leave: 'Congés payés',
            other: 'Autre'
        }
        return labels[type] || type
    }

    const getUnavailabilityTypeOptions = () => {
        return [
            { value: 'disease', label: 'Maladie' },
            { value: 'training', label: 'Formation' },
            { value: 'paid_leave', label: 'Congés payés' },
            { value: 'other', label: 'Autre' }
        ]
    }

    const getUnavailabilityTypeColor = (type) => {
        const colors = {
            disease: 'bg-red-100 text-red-800',
            training: 'bg-blue-100 text-blue-800',
            paid_leave: 'bg-green-100 text-green-800',
            other: 'bg-neutral-100 text-neutral-800'
        }
        return colors[type] || 'bg-neutral-100 text-neutral-800'
    }

    const fetchUnavailabilities = async (params = {}) => {
        try {
            const response = await fetcher.get('/unavailabilities', { params })
            return response.data
        } catch (error) {
            console.error('Erreur lors du chargement des indisponibilités:', error)
            toast.error('Erreur lors du chargement des indisponibilités')
            throw error
        }
    }

    const fetchUnavailability = async (id) => {
        try {
            const response = await fetcher.get(`/unavailabilities/${id}`)
            return response.data
        } catch (error) {
            console.error('Erreur lors du chargement de l\'indisponibilité:', error)
            toast.error('Erreur lors du chargement de l\'indisponibilité')
            throw error
        }
    }

    const createUnavailability = async (data) => {
        try {
            const response = await fetcher.post('/unavailabilities', data)
            toast.success('Indisponibilité créée avec succès')
            return response.data
        } catch (error) {
            console.error('Erreur lors de la création de l\'indisponibilité:', error)
            toast.error('Erreur lors de la création de l\'indisponibilité')
            throw error
        }
    }

    const updateUnavailability = async (id, data) => {
        try {
            const response = await fetcher.put(`/unavailabilities/${id}`, data)
            toast.success('Indisponibilité mise à jour avec succès')
            return response.data
        } catch (error) {
            console.error('Erreur lors de la mise à jour de l\'indisponibilité:', error)
            toast.error('Erreur lors de la mise à jour de l\'indisponibilité')
            throw error
        }
    }

    const deleteUnavailability = async (id) => {
        try {
            await fetcher.delete(`/unavailabilities/${id}`)
            toast.success('Indisponibilité supprimée avec succès')
        } catch (error) {
            console.error('Erreur lors de la suppression de l\'indisponibilité:', error)
            toast.error('Erreur lors de la suppression de l\'indisponibilité')
            throw error
        }
    }

    return {
        getUnavailabilityTypeLabel,
        getUnavailabilityTypeOptions,
        getUnavailabilityTypeColor,
        fetchUnavailabilities,
        fetchUnavailability,
        createUnavailability,
        updateUnavailability,
        deleteUnavailability
    }
} 