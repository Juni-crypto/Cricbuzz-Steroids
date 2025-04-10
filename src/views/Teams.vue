<!-- Teams.vue -->
<template>
  <div class="p-6 h-screen flex flex-col">
    <!-- Header Section with Enhanced Design -->
    <div class="mb-8 relative">
      <div class="absolute inset-0 bg-gradient-to-r from-primary-500/10 to-accent-500/10 rounded-2xl"></div>
      <div class="relative p-8">
        <h1 class="text-4xl font-bold bg-gradient-to-r from-primary-400 via-accent-400 to-primary-400 bg-clip-text text-transparent animate-gradient">
          Cricket Teams
        </h1>
        <p class="text-gray-400 mt-3 text-lg">Explore teams from different categories</p>
      </div>
    </div>

    <!-- Category Tabs with Enhanced Design -->
    <div class="mb-6">
      <div class="flex space-x-4 overflow-x-auto pb-2 hide-scrollbar">
        <button
          v-for="category in categories"
          :key="category.id"
          @click="selectedCategory = category.id"
          class="group relative px-6 py-3 rounded-xl text-sm font-medium transition-all duration-300 whitespace-nowrap"
          :class="[
            selectedCategory === category.id
              ? 'bg-primary-500/20 text-primary-400'
              : 'text-gray-400 hover:text-primary-400'
          ]"
        >
          <!-- Background Effect -->
          <div class="absolute inset-0 rounded-xl bg-gradient-to-r from-primary-500/0 via-primary-500/10 to-accent-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          
          <!-- Content -->
          <div class="relative flex items-center space-x-3">
            <span class="material-icons-outlined text-xl">{{ category.icon }}</span>
            <span>{{ category.name }}</span>
          </div>
          
          <!-- Active Indicator -->
          <div v-if="selectedCategory === category.id" 
               class="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-primary-500 to-accent-500 rounded-full"></div>
        </button>
      </div>
    </div>

    <!-- Search Bar with Enhanced Design -->
    <div class="relative mb-6">
      <div class="absolute inset-0 bg-gradient-to-r from-primary-500/5 to-accent-500/5 rounded-xl blur-xl"></div>
      <div class="relative">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search teams..."
          class="w-full px-6 py-4 pl-14 bg-dark-700/50 border border-dark-600 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:border-primary-500 backdrop-blur-sm"
        >
        <span class="material-icons-outlined absolute left-5 top-1/2 transform -translate-y-1/2 text-gray-400">
          search
        </span>
      </div>
    </div>

    <!-- Teams Grid with Enhanced Design and Scroll -->
    <div class="relative flex-1 overflow-hidden">
      <div class="h-full overflow-y-auto custom-scrollbar">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 p-4">
          <div
            v-for="(team, index) in filteredTeams"
            :key="team.teamId"
            @click="navigateToTeam(team)"
            class="group relative bg-dark-700/50 rounded-2xl border border-dark-600 overflow-hidden transition-all duration-500 hover:border-primary-500/50 hover:shadow-xl hover:shadow-primary-500/10 cursor-pointer"
            :class="{ 'animate-fade-in': index < 12 }"
          >
            <!-- Background Effects -->
            <div class="absolute inset-0 bg-gradient-to-br from-dark-800/80 to-dark-900/80 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            <div class="absolute inset-0 bg-gradient-to-br from-primary-500/5 to-accent-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
            
            <!-- Team Content -->
            <div class="relative p-6">
              <!-- Team Flag with Enhanced Design -->
              <div class="relative w-24 h-24 mx-auto mb-4">
                <!-- Glow Effect -->
                <div class="absolute inset-0 bg-primary-500/20 rounded-full blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <!-- Flag Container -->
                <div class="relative w-full h-full rounded-full overflow-hidden border-4 border-dark-600 group-hover:border-primary-500/50 transition-colors duration-500">
                  <img
                    :src="`https://static.cricbuzz.com/a/img/v1/i1/c${team.imageId}/i.jpg?p=thumb`"
                    :alt="team.teamName"
                    class="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-500"
                  >
                </div>
              </div>
              
              <!-- Team Info with Enhanced Design -->
              <div class="text-center">
                <h3 class="text-xl font-bold text-white mb-2 group-hover:text-primary-400 transition-colors duration-300">
                  {{ team.teamName }}
                </h3>
                <p class="text-sm text-gray-400 mb-3">{{ team.teamSName }}</p>
                <p v-if="team.countryName" 
                   class="inline-block px-3 py-1 rounded-full text-xs font-medium bg-primary-500/10 text-primary-400 border border-primary-500/20">
                  {{ team.countryName }}
                </p>
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
import { useRouter } from 'vue-router'

// Import JSON data
import leagueTeams from '../sample-responses/team-details-league.json'
import localTeams from '../sample-responses/team-details-local.json'
import womenTeams from '../sample-responses/team-details-women.json'
import internationalTeams from '../sample-responses/team-details-int.json'

const router = useRouter()

// Sample data - In real app, this would come from API
const teamsData = {
  league: leagueTeams.list,
  local: localTeams.list,
  women: womenTeams.list,
  international: internationalTeams.list
}

const categories = [
  { id: 'league', name: 'League Teams', icon: 'emoji_events' },
  { id: 'local', name: 'Local Teams', icon: 'location_city' },
  { id: 'women', name: 'Women Teams', icon: 'female' },
  { id: 'international', name: 'International', icon: 'public' }
]

const selectedCategory = ref('league')
const searchQuery = ref('')

const filteredTeams = computed(() => {
  const teams = teamsData[selectedCategory.value] || []
  return teams.filter(team => {
    if (!team.teamId) return false // Filter out category headers
    const searchLower = searchQuery.value.toLowerCase()
    return (
      team.teamName.toLowerCase().includes(searchLower) ||
      team.teamSName.toLowerCase().includes(searchLower) ||
      (team.countryName && team.countryName.toLowerCase().includes(searchLower))
    )
  })
})

const navigateToTeam = (team) => {
  router.push({
    name: 'team-details',
    params: { teamId: team.teamId },
    state: { team }
  })
}
</script>

<style scoped>
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: theme('colors.dark.600') theme('colors.dark.800');
}

.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: theme('colors.dark.800');
  border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: theme('colors.dark.600');
  border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: theme('colors.dark.500');
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Gradient text animation */
.animate-gradient {
  background-size: 200% 200%;
  animation: gradient 8s ease infinite;
}

@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
</style> 