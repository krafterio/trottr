import { Signal, SignalHigh, SignalLow, SignalMedium } from 'lucide-vue-next'

export const useJob = () => {
    const priorityConfig = {
        low: {
            icon: SignalLow,
            color: 'text-gray-500',
            label: 'Faible',
            bgColor: 'bg-gray-500'
        },
        normal: {
            icon: SignalMedium,
            color: 'text-blue-500',
            label: 'Normale',
            bgColor: 'bg-blue-500'
        },
        high: {
            icon: SignalHigh,
            color: 'text-orange-500',
            label: 'Élevée',
            bgColor: 'bg-orange-500'
        },
        urgent: {
            icon: Signal,
            color: 'text-red-500',
            label: 'Urgente',
            bgColor: 'bg-red-500'
        }
    }

    const getPriorityConfig = (priority) => {
        return priorityConfig[priority] || priorityConfig.normal
    }

    const getPriorityOptions = () => {
        return Object.entries(priorityConfig).map(([value, config]) => ({
            value,
            label: config.label,
            icon: config.icon,
            color: config.color,
            bgColor: config.bgColor
        }))
    }

    return {
        priorityConfig,
        getPriorityConfig,
        getPriorityOptions
    }
} 