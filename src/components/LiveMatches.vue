<template>
  <div class="p-6">
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center p-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-400"></div>
    </div>

    <template v-else>
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold bg-gradient-to-r from-primary-400 to-accent-400 bg-clip-text text-transparent animate-gradient">
          Live Matches
        </h1>
        <p class="text-gray-400 mt-2">Real-time cricket matches from around the world</p>
      </div>

      <!-- Match Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="(match, index) in matches" :key="index" 
          class="group relative overflow-hidden rounded-xl backdrop-blur-sm bg-dark-800/40 border border-dark-600 transition-all duration-300 hover:shadow-lg hover:shadow-primary-500/10 hover:border-primary-500/50">
          
          <!-- Glow Effect -->
          <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <div class="absolute inset-0 bg-gradient-to-r from-primary-500/20 to-accent-500/20 blur-xl"></div>
          </div>

          <!-- Content -->
          <div class="relative p-6">
            <!-- Match Status -->
            <div class="flex items-center justify-between mb-4">
              <span class="px-3 py-1 rounded-full text-xs font-medium" 
                :class="match.isLive ? 'bg-accent-500/20 text-accent-400 animate-pulse' : 'bg-dark-600 text-gray-400'">
                {{ match.isLive ? 'LIVE' : match.status }}
              </span>
              <span class="text-sm text-gray-400">{{ match.time }}</span>
            </div>

            <!-- Teams -->
            <div class="space-y-4">
              <div v-for="team in match.teams" :key="team.name" class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                  <div class="w-8 h-8 rounded-full overflow-hidden border border-dark-600">
                    <img :src="team.flag" :alt="team.name" class="w-full h-full object-cover" />
                  </div>
                  <span class="font-medium text-gray-200">{{ team.name }}</span>
                </div>
                <span class="font-semibold text-gray-200">{{ team.score }}</span>
              </div>
            </div>

            <!-- Match Info -->
            <div class="mt-4 pt-4 border-t border-dark-600">
              <div class="flex items-center justify-between text-sm text-gray-400">
                <span>{{ match.tournament }}</span>
                <span>{{ match.venue }}</span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="mt-4 flex space-x-2">
              <button class="flex-1 px-4 py-2 rounded-lg bg-primary-500/10 text-primary-400 hover:bg-primary-500/20 transition-colors duration-300">
                View Details
              </button>
              <button class="px-4 py-2 rounded-lg bg-dark-600 text-gray-300 hover:bg-dark-500 transition-colors duration-300">
                <span class="material-icons-outlined text-sm">notifications</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- No Matches State -->
      <div v-if="matches.length === 0" class="text-center py-12">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-dark-700 mb-4">
          <span class="material-icons-outlined text-3xl text-gray-400">sports_cricket</span>
        </div>
        <h3 class="text-xl font-medium text-gray-300 mb-2">No Live Matches</h3>
        <p class="text-gray-400">Check back later for live cricket action</p>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const loading = ref(true)
const matches = ref([
  {
    id: 1,
    isLive: true,
    status: 'LIVE',
    time: 'Day 1 - Session 2',
    tournament: 'Test Series 2024',
    venue: 'MCG, Melbourne',
    teams: [
      {
        name: 'India',
        score: '245/4',
        flag: 'https://flagcdn.com/in.svg'
      },
      {
        name: 'Australia',
        score: '',
        flag: 'https://flagcdn.com/au.svg'
      }
    ]
  },
  {
    id: 2,
    isLive: true,
    status: 'LIVE',
    time: '18.2 Overs',
    tournament: 'T20I Tri-Series',
    venue: 'Lord\'s, London',
    teams: [
      {
        name: 'England',
        score: '156/3',
        flag: 'https://flagcdn.com/gb-eng.svg'
      },
      {
        name: 'New Zealand',
        score: '',
        flag: 'https://flagcdn.com/nz.svg'
      }
    ]
  },
  {
    id: 3,
    isLive: false,
    status: 'Starting in 1h',
    time: '14:30 GMT',
    tournament: 'ODI Series',
    venue: 'Wanderers, Johannesburg',
    teams: [
      {
        name: 'South Africa',
        score: '',
        flag: 'https://flagcdn.com/za.svg'
      },
      {
        name: 'Pakistan',
        score: '',
        flag: 'https://flagcdn.com/pk.svg'
      }
    ]
  }
])

// Simulate loading
setTimeout(() => {
  loading.value = false
}, 1500)
</script> 