import { onMounted, onBeforeUnmount } from 'vue'
import { usePresenceStore } from '@/common/stores/presence'

export function useViewPresence(pageName) {
  const presenceStore = usePresenceStore()
  let heartbeatInterval = null

  const startHeartbeat = () => {
    if (heartbeatInterval) {
      clearInterval(heartbeatInterval)
    }
    
    heartbeatInterval = setInterval(() => {
      presenceStore.sendHeartbeat()
    }, 30000)
  }

  const stopHeartbeat = () => {
    if (heartbeatInterval) {
      clearInterval(heartbeatInterval)
      heartbeatInterval = null
    }
  }

  onMounted(async () => {
    await presenceStore.enterView(pageName)
    startHeartbeat()
  })

  onBeforeUnmount(async () => {
    stopHeartbeat()
    await presenceStore.leaveView(pageName)
  })

  return {
    currentView: presenceStore.currentView,
    isViewTracked: presenceStore.isViewTracked
  }
} 
