<template>
  <div class="p-6">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent animate-gradient">
        Cricket Matches
      </h1>
      <p class="text-gray-400 mt-2">View live, upcoming and recent cricket matches</p>
    </div>

    <!-- Match Type Tabs -->
    <div class="mb-8">
      <div class="flex space-x-4 overflow-x-auto pb-2">
        <button 
          v-for="type in matchTypes" 
          :key="type"
          @click="selectedType = type"
          class="px-6 py-2 rounded-full text-sm font-medium transition-all duration-300 whitespace-nowrap"
          :class="selectedType === type ? 'bg-primary-500 text-white shadow-lg shadow-primary-500/20' : 'bg-dark-700 text-gray-400 hover:bg-dark-600'">
          {{ type }}
        </button>
      </div>
    </div>

    <!-- Filter Section -->
    <div class="mb-8 p-4 rounded-lg backdrop-blur-sm bg-dark-800/40 border border-dark-600">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-400">Format</label>
          <select v-model="selectedFormat" class="w-full rounded-lg bg-dark-700 border-dark-600 text-gray-200 focus:border-primary-500 focus:ring-primary-500">
            <option value="all">All Formats</option>
            <option v-for="format in uniqueFormats" :key="format" :value="format">{{ format }}</option>
          </select>
        </div>

        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-400">Series</label>
          <select v-model="selectedSeries" class="w-full rounded-lg bg-dark-700 border-dark-600 text-gray-200 focus:border-primary-500 focus:ring-primary-500">
            <option value="all">All Series</option>
            <option v-for="series in uniqueSeries" :key="series" :value="series">{{ series }}</option>
          </select>
        </div>

        <div class="flex items-end">
          <button @click="applyFilters" class="w-full px-4 py-2 rounded-lg bg-primary-500 text-white hover:bg-primary-600 transition-colors duration-300">
            Apply Filters
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="!groupedMatches.length" class="flex flex-col items-center justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500 mb-4"></div>
      <p class="text-gray-400">Loading matches...</p>
    </div>

    <!-- Matches Grid -->
    <div v-else class="space-y-6">
      <div v-for="(day, index) in groupedMatches" :key="index" class="space-y-4">
        <h3 class="text-lg font-semibold text-gray-300">{{ day.date }}</h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="match in day.matches" :key="match.matchInfo.matchId" 
            class="group relative overflow-hidden rounded-lg backdrop-blur-sm bg-dark-800/40 border border-dark-600 p-4 hover:border-primary-500/50 transition-all duration-300 cursor-pointer"
            @click="showMatchDetails(match)">
            
            <!-- Glow Effect -->
            <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <div class="absolute inset-0 bg-gradient-to-r from-primary-500/10 to-accent-500/10 blur-xl"></div>
            </div>

            <!-- Content -->
            <div class="relative">
              <div class="flex justify-between items-center mb-3">
                <span class="text-sm font-medium text-primary-400">{{ match.matchInfo.matchFormat }}</span>
                <span class="text-sm text-gray-400">{{ formatDate(match.matchInfo.startDate) }}</span>
              </div>

              <div class="space-y-3">
                <div v-for="team in [match.matchInfo.team1, match.matchInfo.team2]" :key="team.teamId" 
                  class="flex items-center justify-between">
                  <div class="flex items-center space-x-3">
                    <div class="w-6 h-6 rounded-full overflow-hidden border border-dark-600">
                      <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${team.imageId}/i.jpg?p=de`" 
                        :alt="team.teamName" 
                        class="w-full h-full object-cover"
                        >
                    </div>
                    <span class="text-gray-200">{{ team.teamName }}</span>
                  </div>
                  <span class="text-gray-200">{{ getTeamScore(match, team.teamId) }}</span>
                </div>
              </div>

              <div class="mt-3 pt-3 border-t border-dark-600">
                <div class="flex items-center justify-between text-sm">
                  <span class="text-gray-400">{{ match.matchInfo.venueInfo.ground }}</span>
                  <span class="px-2 py-1 rounded-full text-xs" 
                    :class="getStatusClass(match.matchInfo.state)">
                    {{ match.matchInfo.state }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Match Details Modal -->
    <div v-if="selectedMatch" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-dark-800 rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-start mb-4">
          <h2 class="text-xl font-bold text-white">Match Details</h2>
          <button @click="selectedMatch = null" class="text-gray-400 hover:text-white">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="space-y-4">
          <div class="flex justify-between items-center">
            <div class="flex items-center space-x-3">
              <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${selectedMatch.matchInfo.team1.imageId}/i.jpg?p=de`" 
                :alt="selectedMatch.matchInfo.team1.teamName" 
                class="w-8 h-8"
                @error="e => e.target.src = 'https://via.placeholder.com/32'">
              <span class="text-white">{{ selectedMatch.matchInfo.team1.teamName }}</span>
            </div>
            <span class="text-2xl font-bold text-white">VS</span>
            <div class="flex items-center space-x-3">
              <span class="text-white">{{ selectedMatch.matchInfo.team2.teamName }}</span>
              <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${selectedMatch.matchInfo.team2.imageId}/i.jpg?p=de`" 
                :alt="selectedMatch.matchInfo.team2.teamName" 
                class="w-8 h-8"
                @error="e => e.target.src = 'https://via.placeholder.com/32'">
            </div>
          </div>

          <div class="bg-dark-700 rounded-lg p-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <h3 class="text-sm font-medium text-gray-400">Format</h3>
                <p class="text-white">{{ selectedMatch.matchInfo.matchFormat }}</p>
              </div>
              <div>
                <h3 class="text-sm font-medium text-gray-400">Venue</h3>
                <p class="text-white">{{ selectedMatch.matchInfo.venueInfo.ground }}</p>
              </div>
              <div>
                <h3 class="text-sm font-medium text-gray-400">Date</h3>
                <p class="text-white">{{ formatDate(selectedMatch.matchInfo.startDate) }}</p>
              </div>
              <div>
                <h3 class="text-sm font-medium text-gray-400">Status</h3>
                <p class="text-white">{{ selectedMatch.matchInfo.status }}</p>
              </div>
            </div>
          </div>

          <div v-if="selectedMatch.matchScore" class="space-y-4">
            <div class="bg-dark-700 rounded-lg p-4">
              <h3 class="text-lg font-semibold text-white mb-2">Scorecard</h3>
              <div class="space-y-4">
                <div v-for="(team, index) in [selectedMatch.matchInfo.team1, selectedMatch.matchInfo.team2]" :key="team.teamId">
                  <div class="flex justify-between items-center mb-2">
                    <span class="text-white font-medium">{{ team.teamName }}</span>
                    <span class="text-primary-400">{{ getTeamScore(selectedMatch, team.teamId) }}</span>
                  </div>
                  <div class="grid grid-cols-2 gap-2 text-sm">
                    <div v-for="(innings, key) in getTeamInnings(selectedMatch, team.teamId)" :key="key">
                      <span class="text-gray-400">{{ key }}:</span>
                      <span class="text-white">{{ innings.runs }}/{{ innings.wickets }} ({{ innings.overs }})</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import liveMatches from '../sample-responses/live.json'
import upcomingMatches from '../sample-responses/upcoming.json'
import recentMatches from '../sample-responses/recent.json'

const matchTypes = ['Live', 'Upcoming', 'Recent']
const selectedType = ref('Live')
const selectedFormat = ref('all')
const selectedSeries = ref('all')
const selectedMatch = ref(null)

// Get all unique formats
const uniqueFormats = computed(() => {
  const allMatches = [...liveMatches.typeMatches, ...upcomingMatches.typeMatches, ...recentMatches.typeMatches]
  const formats = new Set()
  allMatches.forEach(typeMatch => {
    typeMatch.seriesMatches.forEach(seriesMatch => {
      seriesMatch.seriesAdWrapper.matches.forEach(match => {
        formats.add(match.matchInfo.matchFormat)
      })
    })
  })
  return Array.from(formats)
})

// Get all unique series names
const uniqueSeries = computed(() => {
  const allMatches = [...liveMatches.typeMatches, ...upcomingMatches.typeMatches, ...recentMatches.typeMatches]
  const series = new Set()
  allMatches.forEach(typeMatch => {
    typeMatch.seriesMatches.forEach(seriesMatch => {
      series.add(seriesMatch.seriesAdWrapper.seriesName)
    })
  })
  return Array.from(series)
})

// Get matches based on selected type
const currentMatches = computed(() => {
  let matches
  switch (selectedType.value) {
    case 'Live':
      matches = liveMatches
      break
    case 'Upcoming':
      matches = upcomingMatches
      break
    case 'Recent':
      matches = recentMatches
      break
    default:
      matches = liveMatches
  }
  return matches.typeMatches
})

// Group matches by date
const groupedMatches = computed(() => {
  const matches = currentMatches.value.flatMap(typeMatch => 
    typeMatch.seriesMatches.flatMap(seriesMatch => 
      seriesMatch.seriesAdWrapper.matches
    )
  )

  // Filter matches based on selected filters
  const filteredMatches = matches.filter(match => {
    if (selectedFormat.value !== 'all' && match.matchInfo.matchFormat !== selectedFormat.value) return false
    if (selectedSeries.value !== 'all' && match.matchInfo.seriesName !== selectedSeries.value) return false
    return true
  })

  // Sort matches by date
  filteredMatches.sort((a, b) => {
    return parseInt(a.matchInfo.startDate) - parseInt(b.matchInfo.startDate)
  })

  // Group by date
  const groups = {}
  filteredMatches.forEach(match => {
    const date = new Date(parseInt(match.matchInfo.startDate))
    const dateStr = date.toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
    if (!groups[dateStr]) {
      groups[dateStr] = []
    }
    groups[dateStr].push(match)
  })

  return Object.entries(groups).map(([date, matches]) => ({
    date,
    matches
  }))
})

// Helper functions
const formatDate = (timestamp) => {
  return new Date(parseInt(timestamp)).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getTeamScore = (match, teamId) => {
  if (!match.matchScore) return ''
  const teamScore = teamId === match.matchInfo.team1.teamId ? match.matchScore.team1Score : match.matchScore.team2Score
  if (!teamScore) return ''
  const innings = Object.values(teamScore)[0]
  return `${innings.runs}/${innings.wickets}`
}

const getTeamInnings = (match, teamId) => {
  if (!match.matchScore) return {}
  const teamScore = teamId === match.matchInfo.team1.teamId ? match.matchScore.team1Score : match.matchScore.team2Score
  return teamScore || {}
}

const getStatusClass = (state) => {
  switch (state.toLowerCase()) {
    case 'complete':
      return 'bg-accent-500/20 text-accent-400'
    case 'live':
      return 'bg-primary-500/20 text-primary-400'
    case 'upcoming':
      return 'bg-blue-500/20 text-blue-400'
    case 'preview':
      return 'bg-purple-500/20 text-purple-400'
    default:
      return 'bg-gray-500/20 text-gray-400'
  }
}

const showMatchDetails = (match) => {
  selectedMatch.value = match
}

const applyFilters = () => {
  // Filters are already applied through computed properties
  console.log('Filters applied')
}
</script>

<style scoped>
.animate-gradient {
  background-size: 200% 200%;
  animation: gradient 8s ease infinite;
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style> 