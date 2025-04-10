<template>
  <div class="space-y-8 relative">
    <!-- Team Selection Tabs -->
    <div class="flex space-x-4 border-b border-slate-700">
      <button v-for="team in [
        { id: 'team1', name: match.squad.team1.team.teamName, imageId: match.squad.team1.team.imageId },
        { id: 'team2', name: match.squad.team2.team.teamName, imageId: match.squad.team2.team.imageId }
      ]"
              :key="team.id"
              @click="selectedTeamId = team.id"
              class="flex items-center px-4 py-2 -mb-px font-medium transition-colors space-x-2"
              :class="[
                selectedTeamId === team.id
                  ? 'text-indigo-400 border-b-2 border-indigo-400'
                  : 'text-slate-400 hover:text-slate-300'
              ]">
        <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${team.imageId}/i.jpg?p=thumb`" 
             :alt="team.name" 
             class="w-6 h-6 rounded-full">
        <span>{{ team.name }}</span>
      </button>
    </div>

    <!-- Playing XI / Bench Tabs -->
    <div class="flex space-x-4 border-b border-slate-700">
      <button v-for="section in ['playing XI', 'substitutes', 'bench', 'support staff']"
              :key="section"
              @click="selectedSection = section"
              class="px-4 py-2 -mb-px font-medium transition-colors"
              :class="[
                selectedSection === section
                  ? 'text-indigo-400 border-b-2 border-indigo-400'
                  : 'text-slate-400 hover:text-slate-300'
              ]">
        {{ section.charAt(0).toUpperCase() + section.slice(1) }}
      </button>
    </div>

    <!-- Team Info -->
    <div class="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
      <div class="flex items-center space-x-4">
        <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${currentTeam.team.imageId}/i.jpg?p=thumb`" 
             :alt="currentTeam.team.teamName" 
             class="w-16 h-16 rounded-full">
        <div>
          <h3 class="text-xl font-bold">{{ currentTeam.team.teamName }}</h3>
          <p class="text-sm text-slate-400">{{ currentPlayers.length }} {{ selectedSection }} members</p>
        </div>
      </div>
    </div>

    <!-- Player Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="player in currentPlayers"
           :key="player.id"
           class="stat-card hover:border-indigo-500/50 transition-colors cursor-pointer"
           @click="selectedPlayer = player">
        <div class="flex items-start space-x-4">
          <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${player.faceImageId || 182026}/i.jpg?p=thumb`" 
               :alt="player.name" 
               class="w-16 h-16 rounded-full object-cover">
          <div class="flex-1">
        <div class="flex items-start justify-between">
          <div>
                <h4 class="text-lg font-semibold flex items-center">
                  {{ player.name }}
                  <span v-if="player.captain" class="ml-1 text-yellow-400 text-sm">©</span>
                  <span v-if="player.keeper" class="ml-1 text-indigo-400 text-sm">†</span>
                </h4>
            <p class="text-sm text-slate-400">{{ player.role }}</p>
          </div>
          <span class="px-2 py-1 text-xs rounded-full"
                :class="[
                      player.isOverseas
                        ? 'bg-indigo-400/10 text-indigo-400'
                        : (player.inMatchChange ? 'bg-yellow-400/10 text-yellow-400' : 'bg-slate-400/10 text-slate-400')
                    ]">
                {{ player.isOverseas ? 'Overseas' : (player.inMatchChange ? player.inMatchChange : 'Local') }}
          </span>
        </div>
            <div class="mt-3 grid grid-cols-2 gap-2">
          <div>
                <p class="text-xs text-slate-400">Batting</p>
                <p class="text-sm font-medium">{{ formatStyle(player.battingStyle) }}</p>
          </div>
          <div>
                <p class="text-xs text-slate-400">Bowling</p>
                <p class="text-sm font-medium">{{ player.bowlingStyle ? formatBowlingStyle(player.bowlingStyle) : 'N/A' }}</p>
              </div>
          </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Player Details Modal -->
    <div v-if="selectedPlayer"
         class="modal-backdrop"
         @click.self="selectedPlayer = null">
      <div class="modal-container">
        <div class="bg-slate-800 rounded-lg p-6 max-w-2xl w-full space-y-6">
        <!-- Header -->
          <div class="flex items-start space-x-6">
            <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${selectedPlayer.faceImageId || 182026}/i.jpg?p=medium`" 
                 :alt="selectedPlayer.name" 
                 class="w-24 h-24 rounded-lg object-cover">
            <div class="flex-1">
        <div class="flex items-start justify-between">
          <div>
                  <h3 class="text-2xl font-bold flex items-center">
                    {{ selectedPlayer.name }}
                    <span v-if="selectedPlayer.captain" class="ml-2 px-2 py-0.5 bg-yellow-400/10 text-yellow-400 text-xs rounded-full">Captain</span>
                    <span v-if="selectedPlayer.keeper" class="ml-2 px-2 py-0.5 bg-indigo-400/10 text-indigo-400 text-xs rounded-full">Keeper</span>
                  </h3>
                  <p class="text-slate-400">{{ selectedPlayer.fullName }}</p>
                  <div class="flex items-center mt-1">
                    <span class="text-xs px-2 py-0.5 rounded-full bg-slate-700 text-slate-300">{{ selectedPlayer.role }}</span>
                    <span v-if="selectedPlayer.isOverseas" class="ml-2 text-xs px-2 py-0.5 rounded-full bg-indigo-400/10 text-indigo-400">Overseas</span>
                  </div>
          </div>
          <button @click="selectedPlayer = null"
                  class="text-slate-400 hover:text-slate-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
              </div>
            </div>
        </div>

          <!-- Player Info -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="stat-card">
              <p class="text-sm text-slate-400">Player ID</p>
              <p class="text-lg font-semibold">{{ selectedPlayer.id }}</p>
          </div>
          <div class="stat-card">
              <p class="text-sm text-slate-400">Team</p>
              <p class="text-lg font-semibold">{{ selectedPlayer.teamName }}</p>
          </div>
          <div class="stat-card">
              <p class="text-sm text-slate-400">Playing Status</p>
              <p class="text-lg font-semibold">{{ getPlayerStatus(selectedPlayer) }}</p>
          </div>
          <div class="stat-card">
              <p class="text-sm text-slate-400">Match Change</p>
              <p class="text-lg font-semibold">{{ selectedPlayer.inMatchChange || 'None' }}</p>
          </div>
        </div>

          <!-- Batting & Bowling -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="stat-card">
              <h4 class="text-lg font-semibold mb-4">Batting Details</h4>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span class="text-slate-400">Style</span>
                  <span>{{ formatStyle(selectedPlayer.battingStyle) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-400">Preferred Position</span>
                  <span>{{ determinePosition(selectedPlayer) }}</span>
                </div>
              </div>
          </div>
          <div class="stat-card">
              <h4 class="text-lg font-semibold mb-4">Bowling Details</h4>
              <div class="space-y-2">
                <div class="flex justify-between">
                  <span class="text-slate-400">Style</span>
                  <span>{{ selectedPlayer.bowlingStyle || 'N/A' }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-slate-400">Type</span>
                  <span>{{ determineBowlingType(selectedPlayer.bowlingStyle) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Team Role -->
          <div class="stat-card">
            <h4 class="text-lg font-semibold mb-4">Team Role</h4>
            <p class="text-base leading-relaxed text-slate-300">
              {{ getPlayerDescription(selectedPlayer) }}
            </p>
          </div>
          
          <!-- Get More Details Button -->
          <div class="flex justify-center mt-6">
            <button @click="getMorePlayerDetails" 
                    class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-medium transition-colors flex items-center space-x-2">
              <span>Get More Details</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'

const props = defineProps({
  match: {
    type: Object,
    required: true
  }
})

const selectedTeamId = ref('team1')
const selectedSection = ref('playing XI')
const selectedPlayer = ref(null)

const currentTeam = computed(() => {
  if (!props.match.squad) return { team: { teamId: 0, teamName: '', imageId: 0 } }
  return props.match.squad[selectedTeamId.value] || { team: { teamId: 0, teamName: '', imageId: 0 } }
})

const currentPlayers = computed(() => {
  if (!props.match.squad) return []
  
  const team = props.match.squad[selectedTeamId.value]
  if (!team || !team.players || !team.players[selectedSection.value]) {
    return []
  }
  
  return team.players[selectedSection.value]
})

// Helper functions
const formatStyle = (style) => {
  if (!style) return 'N/A'
  return style === 'LEFT' ? 'Left Handed' : 'Right Handed'
}

const formatBowlingStyle = (style) => {
  if (!style) return 'N/A'
  if (style.length > 15) {
    return style.split(' ').slice(-2).join(' ')
  }
  return style
}

const determinePosition = (player) => {
  if (!player) return 'N/A'
  
  if (player.role.includes('WK')) {
    return 'Wicketkeeper-Batsman'
  } else if (player.role.includes('Batting Allrounder')) {
    return 'Top/Middle Order'
  } else if (player.role.includes('Bowling Allrounder')) {
    return 'Middle/Lower Order'
  } else if (player.role === 'Batter') {
    return 'Specialist Batsman'
  } else if (player.role === 'Bowler') {
    return 'Tail'
  }
  
  return 'Flexible'
}

const determineBowlingType = (style) => {
  if (!style) return 'N/A'
  
  if (style.includes('fast')) {
    return 'Pace Bowler'
  } else if (style.includes('medium')) {
    return 'Medium Pacer'
  } else if (style.includes('leg break')) {
    return 'Leg Spinner'
  } else if (style.includes('off break')) {
    return 'Off Spinner'
  } else if (style.includes('orthodox')) {
    return 'Orthodox Spinner'
  }
  
  return 'All-Rounder'
}

const getPlayerStatus = (player) => {
  if (player.substitute) {
    return player.splSubstitute ? 'Impact Sub' : 'Substitute'
  } else if (player.captain) {
    return 'Playing (Captain)'
  } else if (player.keeper) {
    return 'Playing (Keeper)'
  } else if (selectedSection.value === 'playing XI') {
    return 'Playing XI'
  } else if (selectedSection.value === 'substitutes') {
    return 'Substitute'
  } else if (selectedSection.value === 'bench') {
    return 'Bench'
  } else if (selectedSection.value === 'support staff') {
    return 'Support Staff'
  }
  
  return 'Squad Member'
}

const getPlayerDescription = (player) => {
  let description = `${player.fullName} is a ${player.battingStyle === 'LEFT' ? 'left-handed' : 'right-handed'} `
  
  if (player.role.includes('WK')) {
    description += 'wicketkeeper-batsman '
  } else if (player.role === 'Batter') {
    description += 'specialist batsman '
  } else if (player.role === 'Bowling Allrounder') {
    description += 'bowling all-rounder '
  } else if (player.role === 'Batting Allrounder') {
    description += 'batting all-rounder '
  } else if (player.role === 'Bowler') {
    description += `${player.bowlingStyle?.toLowerCase() || ''} bowler `
  }
  
  description += `playing for ${player.teamName}. `
  
  if (player.captain) {
    description += 'Currently captaining the side. '
  }
  
  if (player.keeper) {
    description += 'Primary wicketkeeper in the team. '
  }
  
  if (player.isOverseas) {
    description += 'Overseas player in the squad. '
  }
  
  if (player.inMatchChange) {
    description += `In-match change status: ${player.inMatchChange}. `
  }
  
  return description
}

const getMorePlayerDetails = () => {
  // This function would typically fetch more detailed player information from an API
  // For now, we'll just show an alert
  alert(`Fetching more details for ${selectedPlayer.value.fullName}`)
  
  // In a real application, this might open a new page or fetch additional data
  // window.open(`https://www.cricbuzz.com/profiles/${selectedPlayer.value.id}/${selectedPlayer.value.fullName.replace(/\s+/g, '-').toLowerCase()}`, '_blank')
}

// Reset player selection when changing teams or sections
watch([selectedTeamId, selectedSection], () => {
  selectedPlayer.value = null
})

// Watch for player selection and scroll to modal when opened
watch(selectedPlayer, (player) => {
  if (player) {
    // Use nextTick to ensure the modal is rendered before scrolling
    nextTick(() => {
      const modalContainer = document.querySelector('.modal-container')
      if (modalContainer) {
        modalContainer.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    })
  }
})
</script>

<style scoped>
@import './styles.css';

.stat-card {
  @apply bg-slate-800/50 rounded-lg p-4 border border-slate-700;
}

.modal-backdrop {
  @apply fixed inset-0 bg-slate-900/75 z-50;
  /* This keeps the modal within the component */
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
}

.modal-container {
  @apply flex items-center justify-center p-4;
  height: 100%;
  overflow-y: auto;
}
</style> 