<template>
  <div class="container mx-auto px-4 py-8 space-y-8">
    <!-- Hero Section -->
    <div class="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 rounded-lg p-8 shadow-2xl border border-slate-700/30 relative overflow-hidden">
      <!-- Background Pattern -->
      <div class="absolute inset-0 opacity-10">
        <div class="absolute inset-0" style="background-image: radial-gradient(circle at 1px 1px, rgb(255 255 255 / 0.1) 1px, transparent 0); background-size: 40px 40px;"></div>
      </div>
      
      <!-- Animated Gradient Border -->
      <div class="absolute inset-0 rounded-lg bg-gradient-to-r from-indigo-500/20 via-purple-500/20 to-pink-500/20 animate-gradient-x"></div>
      
      <!-- Content -->
      <div class="relative">
        <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-8">
          <div class="space-y-4">
            <div class="flex items-center space-x-3">
              <div class="w-12 h-12 bg-indigo-500/20 rounded-full flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <h1 class="text-4xl md:text-5xl font-bold text-white">{{ venueDetails.ground }}</h1>
            </div>
            <div class="flex flex-wrap items-center gap-4">
              <div class="flex items-center space-x-2 bg-slate-800/50 rounded-full px-4 py-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span class="text-slate-300">{{ venueDetails.city }}, {{ venueDetails.country }}</span>
              </div>
              <div class="flex items-center space-x-2 bg-slate-800/50 rounded-full px-4 py-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="text-slate-300">{{ venueDetails.timezone }}</span>
              </div>
              <div class="flex items-center space-x-2 bg-slate-800/50 rounded-full px-4 py-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span class="text-slate-300">Capacity: {{ venueDetails.capacity }}</span>
              </div>
            </div>
          </div>
          <div class="mt-4 md:mt-0">
            <div class="flex items-center space-x-2 bg-indigo-500/20 rounded-full px-6 py-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              <span class="text-indigo-400 font-medium">Est. {{ venueDetails.established }}</span>
            </div>
          </div>
        </div>

        <!-- Quick Stats Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-slate-800/50 rounded-lg p-4 transform hover:scale-105 transition-all duration-300 hover:bg-slate-800/70">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-indigo-500/20 rounded-full flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-slate-400">Total Matches</p>
                <p class="text-lg font-bold text-white">{{ venueStats.venueStats.find(s => s.key === 'Total Matches')?.value || '0' }}</p>
              </div>
            </div>
          </div>
          <div class="bg-slate-800/50 rounded-lg p-4 transform hover:scale-105 transition-all duration-300 hover:bg-slate-800/70">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-indigo-500/20 rounded-full flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-slate-400">Highest Score</p>
                <p class="text-lg font-bold text-white">{{ venueStats.venueStats.find(s => s.key === 'Highest Score')?.value || '0' }}</p>
              </div>
            </div>
          </div>
          <div class="bg-slate-800/50 rounded-lg p-4 transform hover:scale-105 transition-all duration-300 hover:bg-slate-800/70">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-indigo-500/20 rounded-full flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-slate-400">Average Score</p>
                <p class="text-lg font-bold text-white">{{ venueStats.venueStats.find(s => s.key === 'Average Score')?.value || '0' }}</p>
              </div>
            </div>
          </div>
          <div class="bg-slate-800/50 rounded-lg p-4 transform hover:scale-105 transition-all duration-300 hover:bg-slate-800/70">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-indigo-500/20 rounded-full flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p class="text-xs text-slate-400">Win Rate</p>
                <p class="text-lg font-bold text-white">{{ venueStats.venueStats.find(s => s.key === 'Win Rate')?.value || '0' }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Venue Profile -->
    <div class="bg-slate-800/60 rounded-lg p-6 mb-6 backdrop-blur-sm">
      <div class="flex items-center space-x-3 mb-4">
        <div class="w-10 h-10 bg-indigo-500/20 rounded-full flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-white">Venue Profile</h2>
      </div>
      <div class="prose prose-invert max-w-none" v-html="venueDetails.profile"></div>
    </div>

    <!-- Statistics Section -->
    <div class="bg-slate-800/60 rounded-lg p-6 mb-6 backdrop-blur-sm">
      <div class="flex items-center space-x-3 mb-4">
        <div class="w-10 h-10 bg-indigo-500/20 rounded-full flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-white">Venue Statistics</h2>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="stat in venueStats.venueStats" :key="stat.key" 
             class="bg-slate-700/40 rounded-lg p-4 transform hover:scale-105 transition-transform duration-300 hover:bg-slate-700/60">
          <p class="text-xs text-slate-400 mb-1">{{ stat.key }}</p>
          <p class="text-sm font-medium text-white whitespace-pre-line">{{ stat.value }}</p>
        </div>
      </div>
    </div>

    <!-- Upcoming Matches -->
    <div class="bg-slate-800/60 rounded-lg p-6 backdrop-blur-sm">
      <div class="flex items-center space-x-3 mb-4">
        <div class="w-10 h-10 bg-indigo-500/20 rounded-full flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-white">Upcoming Matches</h2>
      </div>
      <div v-for="series in venueMatches.matchDetails" :key="series.matchDetailsMap.seriesId" class="mb-6 last:mb-0">
        <div class="flex items-center space-x-2 mb-3">
          <div class="w-8 h-8 bg-indigo-500/20 rounded-full flex items-center justify-center">
            <span class="text-sm font-medium text-indigo-400">{{ series.matchDetailsMap.key.charAt(0) }}</span>
          </div>
          <h3 class="text-lg font-semibold text-slate-300">{{ series.matchDetailsMap.key }}</h3>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="match in series.matchDetailsMap.match" 
               :key="match.matchInfo.matchId" 
               class="bg-slate-700/40 rounded-lg p-4 transform hover:scale-105 transition-transform duration-300 hover:bg-slate-700/60">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center space-x-3">
                <img :src="getTeamImage(match.matchInfo.team1.imageId)" 
                     :alt="match.matchInfo.team1.teamName"
                     class="w-12 h-12 rounded-full border-2 border-slate-600" />
                <span class="text-sm font-medium text-white">{{ match.matchInfo.team1.teamSName }}</span>
              </div>
              <span class="text-sm font-medium text-indigo-400">VS</span>
              <div class="flex items-center space-x-3">
                <span class="text-sm font-medium text-white">{{ match.matchInfo.team2.teamSName }}</span>
                <img :src="getTeamImage(match.matchInfo.team2.imageId)" 
                     :alt="match.matchInfo.team2.teamName"
                     class="w-12 h-12 rounded-full border-2 border-slate-600" />
              </div>
            </div>
            <div class="text-center">
              <p class="text-sm text-slate-300">{{ formatDate(match.matchInfo.startDate) }}</p>
              <p class="text-xs text-slate-400">{{ match.matchInfo.status }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import venueDetails from '../sample-responses/venue-stats/venue-details.json'
import venueStats from '../sample-responses/venue-stats/venue-stats.json'
import venueMatches from '../sample-responses/venue-stats/venue-matches.json'

const props = defineProps({
  id: {
    type: String,
    required: true
  }
})

const formatDate = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(parseInt(timestamp))
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

const getTeamImage = (imageId) => {
  return 'http://static.cricbuzz.com/a/img/v1/i1/c' + imageId + '/i.jpg?p=thumb'
}

onMounted(() => {
  // In a real app, you would fetch venue data using the id prop
  // For now, we're using the sample data directly
})
</script>

<style scoped>
.prose {
  @apply text-slate-300;
}

.prose :deep(b) {
  @apply text-white font-semibold;
}

.prose :deep(p) {
  @apply mb-4;
}

.prose :deep(ul) {
  @apply list-disc list-inside mb-4;
}

.prose :deep(li) {
  @apply mb-2;
}

.backdrop-blur-sm {
  backdrop-filter: blur(8px);
}

@keyframes gradient-x {
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

.animate-gradient-x {
  animation: gradient-x 15s ease infinite;
  background-size: 200% 200%;
}
</style> 