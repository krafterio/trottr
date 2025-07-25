import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useWebSocket } from '@/common/composables/websocket'

export const usePresenceStore = defineStore('presence', () => {
  const currentView = ref('')
  const isViewTracked = ref(false)
  const onlineUsers = ref([])
  const { sendMessage, on } = useWebSocket()

  const unsubscribeOnlineUsers = on('online_users_update', (data) => {
    if (data && data.users) {
      onlineUsers.value = data.users
    }
  })

  const enterView = async (view) => {
    if (currentView.value) {
      await leaveView(currentView.value)
    }

    currentView.value = view
    isViewTracked.value = true

    try {
      await sendMessage('view_enter', { view: view })
      console.log(`[Presence] Entered view: ${view}`)
    } catch (error) {
      console.error(`[Presence] Error entering view ${view}:`, error)
    }
  }

  const leaveView = async (view) => {
    if (!isViewTracked.value || currentView.value !== view) {
      return
    }

    try {
      await sendMessage('view_leave', { view: view })
      console.log(`[Presence] Left view: ${view}`)
    } catch (error) {
      console.error(`[Presence] Error leaving view ${view}:`, error)
    }

    if (currentView.value === view) {
      currentView.value = ''
      isViewTracked.value = false
    }
  }

  const sendHeartbeat = async () => {
    if (!isViewTracked.value) {
      return
    }

    try {
      await sendMessage('heartbeat', { 
        page: currentView.value,
        timestamp: Date.now()
      })
    } catch (error) {
      console.error('[Presence] Error sending heartbeat:', error)
    }
  }

  const cleanup = async () => {
    if (currentView.value && isViewTracked.value) {
      await leaveView(currentView.value)
    }

    if (unsubscribeOnlineUsers) {
      unsubscribeOnlineUsers()
    }
  }

  return {
    currentView: computed(() => currentView.value),
    isViewTracked: computed(() => isViewTracked.value),
    onlineUsers: computed(() => onlineUsers.value),
    enterView: enterView,
    leaveView: leaveView,
    sendHeartbeat,
    cleanup
  }
})
