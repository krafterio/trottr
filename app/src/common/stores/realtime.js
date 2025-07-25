import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useRealtimeStore = defineStore('realtime', () => {
  const pendingUpdates = ref(new Map())
  const handlers = ref(new Map())

  const registerHandler = (model, action, handler) => {
    const key = `${model}.${action}`
    if (!handlers.value.has(key)) {
      handlers.value.set(key, [])
    }
    handlers.value.get(key).push(handler)
  }

  const unregisterHandler = (model, action, handler) => {
    const key = `${model}.${action}`
    if (handlers.value.has(key)) {
      const handlerList = handlers.value.get(key)
      const index = handlerList.indexOf(handler)
      if (index > -1) {
        handlerList.splice(index, 1)
      }
    }
  }

  const handleModelUpdate = async (payload) => {
    const { model, action, ids, workspace_id, metadata } = payload
    const key = `${model}.${action}`

    console.log(`[Realtime] Received ${key} update:`, { ids, metadata })

    if (handlers.value.has(key)) {
      const handlerList = handlers.value.get(key)
      for (const handler of handlerList) {
        try {
          await handler({ ids, workspace_id, metadata })
        } catch (error) {
          console.error(`[Realtime] Error executing handler for ${key}:`, error)
        }
      }
    }

    if (handlers.value.has(`${model}.*`)) {
      const handlerList = handlers.value.get(`${model}.*`)
      for (const handler of handlerList) {
        try {
          await handler({ action, ids, workspace_id, metadata })
        } catch (error) {
          console.error(`[Realtime] Error executing wildcard handler for ${model}:`, error)
        }
      }
    }
  }

  const addPendingUpdate = (model, action, ids) => {
    const key = `${model}.${action}`
    if (!pendingUpdates.value.has(key)) {
      pendingUpdates.value.set(key, new Set())
    }
    ids.forEach(id => pendingUpdates.value.get(key).add(id))
  }

  const clearPendingUpdates = (model, action) => {
    const key = `${model}.${action}`
    pendingUpdates.value.delete(key)
  }

  const getPendingUpdates = (model, action = null) => {
    if (action) {
      const key = `${model}.${action}`
      return Array.from(pendingUpdates.value.get(key) || [])
    }
    
    const allUpdates = []
    for (const [key, ids] of pendingUpdates.value.entries()) {
      if (key.startsWith(`${model}.`)) {
        allUpdates.push(...Array.from(ids))
      }
    }
    return [...new Set(allUpdates)]
  }

  return {
    registerHandler,
    unregisterHandler,
    handleModelUpdate,
    addPendingUpdate,
    clearPendingUpdates,
    getPendingUpdates
  }
}) 
