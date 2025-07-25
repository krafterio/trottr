import { defineStore } from 'pinia'
import {useFetcher} from "@/common/composables/fetcher.js";

export const usePreferencesStore = defineStore('preferences', {
  state: () => ({
    preferences: {},
    loading: false
  }),

  actions: {
    async loadPreferences() {
      this.loading = true
      try {
        const fetcher = useFetcher({abortOnUnmounted: false})
        const response = await fetcher.get('/users/me/preferences')
        this.preferences = response.data.preferences
      } catch (error) {
        this.preferences = {}
      } finally {
        this.loading = false
      }
    },

    async updatePreference(key, value) {
      try {
        const update = { [key]: value }
        const fetcher = useFetcher({abortOnUnmounted: false})
        const response = await fetcher.patch('/users/me/preferences', update)
        this.preferences = response.data.preferences
      } catch (error) {
        this.preferences[key] = value
      }
    },

    async updatePreferences(newPreferences) {
      try {
        const fetcher = useFetcher({abortOnUnmounted: false})
        const response = await fetcher.put('/users/me/preferences', newPreferences)
        this.preferences = response.data.preferences
      } catch (error) {
      }
    },

    getPreference(key, defaultValue = null) {
      return this.preferences[key] ?? defaultValue
    }
  }
}) 