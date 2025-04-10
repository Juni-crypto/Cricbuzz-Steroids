<template>
  <div class="min-h-screen flex flex-col">
    <!-- Main Content -->
    <div class="flex-1 container mx-auto px-4 py-8">
      <!-- Player Search Section -->
      <div class="relative mb-8">
        <div class="relative">
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="Search players..."
            class="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-indigo-500"
            @input="handleSearch"
          />
          <div class="absolute right-3 top-1/2 -translate-y-1/2">
            <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        <!-- Search Results Dropdown -->
        <div v-if="searchQuery && searchResults.length > 0" 
             class="absolute z-50 w-full mt-2 bg-slate-800 border border-slate-700 rounded-lg shadow-lg max-h-[400px] overflow-y-auto">
          <div class="divide-y divide-slate-700">
            <div v-for="player in searchResults" 
                 :key="player.id"
                 class="p-4 hover:bg-slate-700 cursor-pointer transition-colors"
                 @click="selectPlayer(player)">
              <div class="flex items-center space-x-4">
                <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${player.faceImageId}/i.jpg?p=thumb`"
                     :alt="player.name"
                     class="w-12 h-12 rounded-full border-2 border-indigo-500/50">
                <div>
                  <h3 class="font-medium text-white">{{ player.name }}</h3>
                  <p class="text-sm text-slate-400">{{ player.teamName }}</p>
                  <p v-if="player.dob" class="text-xs text-slate-500">Born: {{ formatDate(player.dob) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Trending Players Section -->
      <div v-if="!searchQuery && trendingPlayers.length > 0" class="mb-8">
        <h2 class="text-xl font-bold text-white mb-4">Trending Players</h2>
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <div v-for="player in trendingPlayers" 
               :key="player.id"
               class="bg-slate-800 rounded-lg p-4 hover:bg-slate-700 transition-colors cursor-pointer"
               @click="selectPlayer(player)">
            <div class="flex items-center space-x-4">
              <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${player.faceImageId}/i.jpg?p=thumb`"
                   :alt="player.name"
                   class="w-16 h-16 rounded-full border-2 border-indigo-500/50">
              <div>
                <h3 class="font-medium text-white">{{ player.name }}</h3>
                <p class="text-sm text-slate-400">{{ player.teamName }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Selected Player Details -->
      <div v-if="selectedPlayer" class="bg-slate-800 rounded-lg p-6">
        <div class="flex items-start space-x-6">
          <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${selectedPlayer.faceImageId}/i.jpg?p=medium`"
               :alt="selectedPlayer.name"
               class="w-32 h-32 rounded-lg object-cover">
          <div class="flex-1">
            <h1 class="text-3xl font-bold text-white mb-2">{{ selectedPlayer.name }}</h1>
            <div class="flex items-center space-x-4 text-slate-400">
              <span>{{ selectedPlayer.teamName }}</span>
              <span v-if="selectedPlayer.dob">• Born: {{ formatDate(selectedPlayer.dob) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
  
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Sample data from the JSON files
const trendingPlayers = ref([
  {
    id: "42828",
    name: "Conrad Greenshields",
    teamName: "Portugal",
    faceImageId: 182026
  },
  {
    id: "9406",
    name: "Nicholas Pooran",
    teamName: "West Indies",
    faceImageId: 244722
  },
  {
    id: "10636",
    name: "Rajat Patidar",
    teamName: "India",
    faceImageId: 234983
  },
  {
    id: "25210",
    name: "Kuruge Abeyrathna",
    teamName: "Norway",
    faceImageId: 182026
  },
  {
    id: "10808",
    name: "Mohammed Siraj",
    teamName: "India",
    faceImageId: 591952
  },
  {
    id: "11540",
    name: "Jofra Archer",
    teamName: "England",
    faceImageId: 617429
  },
  {
    id: "8733",
    name: "KL Rahul",
    teamName: "India",
    faceImageId: 616523
  },
  {
    id: "9551",
    name: "Michael Bracewell",
    teamName: "New Zealand",
    faceImageId: 616430
  }
])

// Search functionality
const searchQuery = ref('')
const searchResults = ref([])
const selectedPlayer = ref(null)

// Sample search response data
const searchResponse = {
  player: [
    {
      id: "9161",
      name: "Chamani Seneviratna",
      teamName: "Sri Lanka",
      faceImageId: 151508,
      dob: "1978-11-14"
    },
    {
      id: "1413",
      name: "Virat Kohli",
      teamName: "India",
      faceImageId: 616517,
      dob: "1988-11-05"
    },
    {
      id: "10213",
      name: "Virat Singh",
      teamName: "India",
      faceImageId: 182026,
      dob: "1997-12-08"
    }
  ],
  category: "Virat"
}

// Simple search function
const handleSearch = () => {
  if (!searchQuery.value) {
    searchResults.value = []
    return
  }
  
  // Simulate API call with sample data
  searchResults.value = searchResponse.player
}

const selectPlayer = (player) => {
  // Navigate to the player details page
  router.push({
    name: 'player-details',
    params: { id: player.id }
  })
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Smooth transitions */
.transition-colors {
  transition-property: background-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* Hover effects */
.hover\:bg-slate-700:hover {
  background-color: rgb(51 65 85);
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(99, 102, 241, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(99, 102, 241, 0.5);
}
</style> 