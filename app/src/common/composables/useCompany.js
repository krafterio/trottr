import { computed } from 'vue'

export function useCompany() {
  const staffRanges = computed(() => [
    {
      value: '1-10',
      label: '1-10',
      color: '#10b981'
    },
    {
      value: '10-50',
      label: '10-50',
      color: '#3b82f6'
    },
    {
      value: '50-200',
      label: '50-200',
      color: '#8b5cf6'
    },
    {
      value: '200-500',
      label: '200-500',
      color: '#f97316'
    },
    {
      value: '500-1K',
      label: '500-1000',
      color: '#ef4444'
    },
    {
      value: '1K-5K',
      label: '1000-5000',
      color: '#ec4899'
    },
    {
      value: '5K-10K',
      label: '5000-10000',
      color: '#6366f1'
    },
    {
      value: '> 10K',
      label: '> 10000',
      color: '#6b7280'
    }
  ])

  const getStaffRangeLabel = (value) => {
    const range = staffRanges.value.find(r => r.value === value)
    return range?.label || value
  }

  const getStaffRangeColor = (value) => {
    const range = staffRanges.value.find(r => r.value === value)
    return range?.color || 'gray'
  }

  return {
    staffRanges,
    getStaffRangeLabel,
    getStaffRangeColor
  }
} 