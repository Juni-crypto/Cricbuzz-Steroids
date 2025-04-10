import { defineStore } from 'pinia'

// Import mock data
import liveMatches from '../../sample-responses/live.json'
import recentMatches from '../../sample-responses/recent.json'
import upcomingMatches from '../../sample-responses/upcoming.json'

export const useCricketStore = defineStore('cricket', {
  state: () => ({
    liveMatches: [],
    recentMatches: [],
    upcomingMatches: [],
    selectedMatch: null,
    loading: false,
    error: null
  }),

  getters: {
    getLiveMatches: (state) => state.liveMatches,
    getRecentMatches: (state) => state.recentMatches,
    getUpcomingMatches: (state) => state.upcomingMatches,
    isLoading: (state) => state.loading,
    hasError: (state) => state.error !== null
  },

  actions: {
    async fetchLiveMatches() {
      try {
        this.loading = true
        // In a real app, this would be an API call
        this.liveMatches = liveMatches.typeMatches
        this.loading = false
      } catch (error) {
        this.error = error.message
        this.loading = false
      }
    },

    async fetchRecentMatches() {
      try {
        this.loading = true
        this.recentMatches = recentMatches.typeMatches
        this.loading = false
      } catch (error) {
        this.error = error.message
        this.loading = false
      }
    },

    async fetchUpcomingMatches() {
      try {
        this.loading = true
        this.upcomingMatches = upcomingMatches.typeMatches
        this.loading = false
      } catch (error) {
        this.error = error.message
        this.loading = false
      }
    },

    setSelectedMatch(match) {
      this.selectedMatch = match
    },

    clearError() {
      this.error = null
    }
  }
}) 