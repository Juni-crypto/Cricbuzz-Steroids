<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-slate-900 to-gray-900 text-white p-4 md:p-8">
    <!-- Match Header with 3D effect -->
    <div class="relative bg-gradient-to-r from-indigo-600/20 to-purple-600/20 rounded-2xl p-8 mb-8 backdrop-blur-sm shadow-2xl overflow-hidden">
      <!-- Background pattern -->
      <div class="absolute inset-0 bg-grid-pattern opacity-5"></div>
      
      <!-- Team Selection -->
      <div class="flex flex-col md:flex-row justify-between items-center gap-6 relative z-10">
        <div class="flex flex-wrap gap-4">
          <button v-for="team in [match.matchInfo.team1, match.matchInfo.team2]"
                  :key="team.id"
                  @click="handleTeamChange(team)"
                  class="group relative px-8 py-4 rounded-xl transition-all duration-300"
                  :class="[
                    selectedTeam?.id === team.id
                      ? 'bg-indigo-500/30 text-white'
                      : 'hover:bg-slate-700/30 text-slate-300'
                  ]">
            <!-- Button glow effect -->
            <div class="absolute inset-0 rounded-xl bg-gradient-to-r from-indigo-500/20 to-purple-500/20 opacity-0 group-hover:opacity-100 transition-opacity"></div>
            
            <!-- Team flag/icon placeholder -->
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500/20 to-purple-500/20 mb-2 mx-auto flex items-center justify-center">
              <span class="text-lg font-bold">{{ team.name[0] }}</span>
            </div>
            
            <span class="relative z-10 block text-center font-medium">{{ team.name }}</span>
            
            <!-- Active indicator -->
            <div v-if="selectedTeam?.id === team.id" 
                 class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-12 h-1 bg-indigo-500 rounded-full"></div>
          </button>
        </div>

        <!-- Score Display with 3D card effect -->
        <div class="relative group bg-slate-800/40 rounded-2xl p-6 backdrop-blur-sm transition-transform hover:scale-105">
          <div class="absolute inset-0 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <div class="relative z-10">
            <div class="text-4xl font-bold bg-gradient-to-r from-white to-indigo-200 bg-clip-text text-transparent">
              {{ selectedTeam?.total }}/{{ selectedTeam?.wickets }}
            </div>
            <div class="mt-2 text-slate-300">
              <span class="text-indigo-400 font-medium">{{ selectedTeam?.overs }}</span> Overs
              <span class="mx-2">•</span>
              RR: <span class="text-indigo-400 font-medium">{{ selectedTeam?.runRate }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid with Glass Effect -->
    <div class="grid grid-cols-1 gap-8">
      <!-- Batting & Bowling Cards -->
      <div class="space-y-8">
        <div v-if="selectedTeam" class="bg-slate-800/30 backdrop-blur-sm rounded-2xl overflow-hidden shadow-xl border border-slate-700/30">
          <div class="p-6 bg-gradient-to-r from-slate-800/50 to-slate-700/50">
            <h3 class="text-xl font-semibold flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-400" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
              </svg>
              <span class="bg-gradient-to-r from-white to-indigo-200 bg-clip-text text-transparent">
                Batting
              </span>
            </h3>
          </div>
          
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-slate-700/50 bg-slate-800/30">
                  <th class="py-4 px-6 text-left text-sm font-medium text-slate-300">Batter</th>
                  <th class="py-4 px-6 text-center text-sm font-medium text-slate-300">R</th>
                  <th class="py-4 px-6 text-center text-sm font-medium text-slate-300">B</th>
                  <th class="py-4 px-6 text-center text-sm font-medium text-slate-300">4s</th>
                  <th class="py-4 px-6 text-center text-sm font-medium text-slate-300">6s</th>
                  <th class="py-4 px-6 text-center text-sm font-medium text-slate-300">SR</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-700/30">
                <tr v-for="batter in selectedTeam.battingCard"
                    :key="batter.id"
                    class="group hover:bg-slate-700/20 transition-all duration-300">
                  <td class="py-4 px-6">
                    <div class="flex flex-col">
                      <div class="font-medium text-white group-hover:text-indigo-400 transition-colors">
                        {{ batter.name }}
                      </div>
                      <div class="text-sm text-slate-400">{{ batter.dismissal }}</div>
                    </div>
                  </td>
                  <td class="py-4 px-6 text-center">
                    <div class="relative">
                      <span :class="{
                        'text-2xl font-bold bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent': batter.runs >= 100,
                        'text-xl font-bold text-indigo-400': batter.runs >= 50 && batter.runs < 100,
                        'text-white': batter.runs < 50
                      }">
                        {{ batter.runs }}
                      </span>
                      <!-- Achievement badge for century/fifty -->
                      <div v-if="batter.runs >= 50" 
                           class="absolute -top-1 -right-1 w-2 h-2 rounded-full"
                           :class="{
                             'bg-yellow-400 animate-ping': batter.runs >= 100,
                             'bg-indigo-400': batter.runs >= 50 && batter.runs < 100
                           }">
                      </div>
                    </div>
                  </td>
                  <td class="py-4 px-6 text-center text-slate-300">{{ batter.balls }}</td>
                  <td class="py-4 px-6 text-center">
                    <span class="text-green-400">{{ batter.fours }}</span>
                  </td>
                  <td class="py-4 px-6 text-center">
                    <span class="text-purple-400">{{ batter.sixes }}</span>
                  </td>
                  <td class="py-4 px-6 text-center">
                    <span :class="{
                      'text-green-400': batter.strikeRate >= 150,
                      'text-yellow-400': batter.strikeRate >= 100 && batter.strikeRate < 150,
                      'text-slate-300': batter.strikeRate < 100
                    }">
                      {{ batter.strikeRate }}
                    </span>
                  </td>
                </tr>
              </tbody>
              <tfoot>
                <tr class="border-t border-slate-700/50 bg-slate-800/40">
                  <td class="py-4 px-6 font-medium text-white">Extras</td>
                  <td class="py-4 px-6 text-center" colspan="5">
                    <span class="text-indigo-400 font-medium">{{ selectedTeam.extras.total }}</span>
                    <span class="text-slate-400 text-sm ml-2">
                      (b {{ selectedTeam.extras.byes }}, lb {{ selectedTeam.extras.legByes }}, 
                      w {{ selectedTeam.extras.wides }}, nb {{ selectedTeam.extras.noBalls }})
                    </span>
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>

        <div class="bg-slate-800/30 backdrop-blur-sm rounded-2xl overflow-hidden shadow-xl border border-slate-700/30">
          <div class="p-6 bg-gradient-to-r from-slate-800/50 to-slate-700/50">
            <h3 class="text-xl font-semibold flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-400" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"></path>
              </svg>
              <span class="bg-gradient-to-r from-white to-indigo-200 bg-clip-text text-transparent">
                Bowling
              </span>
            </h3>
          </div>
          
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-slate-700/50 bg-slate-800/30">
                  <th class="py-4 px-6 text-left text-sm font-medium text-slate-300">Bowler</th>
                  <th class="py-4 px-6 text-center text-sm font-medium text-slate-300">O</th>
                  <th class="py-4 px-6 text-center text-sm font-medium text-slate-300">M</th>
                  <th class="py-4 px-6 text-center text-sm font-medium text-slate-300">R</th>
                  <th class="py-4 px-6 text-center text-sm font-medium text-slate-300">W</th>
                  <th class="py-4 px-6 text-center text-sm font-medium text-slate-300">Econ</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-700/30">
                <tr v-for="bowler in selectedTeam.bowlingCard"
                    :key="bowler.id"
                    class="group hover:bg-slate-700/20 transition-all duration-300">
                  <td class="py-4 px-6 font-medium text-white group-hover:text-indigo-400 transition-colors">
                    {{ bowler.name }}
                  </td>
                  <td class="py-4 px-6 text-center text-slate-300">{{ bowler.overs }}</td>
                  <td class="py-4 px-6 text-center text-slate-300">{{ bowler.maidens }}</td>
                  <td class="py-4 px-6 text-center text-slate-300">{{ bowler.runs }}</td>
                  <td class="py-4 px-6 text-center">
                    <div class="relative">
                      <span :class="{
                        'text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent': bowler.wickets >= 5,
                        'text-xl font-bold text-green-400': bowler.wickets >= 3 && bowler.wickets < 5,
                        'text-white': bowler.wickets < 3
                      }">
                        {{ bowler.wickets }}
                      </span>
                      <!-- Achievement badge for 5-wicket haul -->
                      <div v-if="bowler.wickets >= 5" 
                           class="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-purple-400 animate-ping">
                      </div>
                    </div>
                  </td>
                  <td class="py-4 px-6 text-center">
                    <span :class="{
                      'text-green-400': bowler.economy <= 6,
                      'text-yellow-400': bowler.economy > 6 && bowler.economy <= 8,
                      'text-red-400': bowler.economy > 8
                    }">
                      {{ bowler.economy }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Partnerships Section -->
      <div class="space-y-8">
        <!-- Section Title -->
        <div class="flex items-center justify-between">
          <h2 class="text-2xl font-bold bg-gradient-to-r from-white to-indigo-200 bg-clip-text text-transparent">
            Match Progress
          </h2>
        </div>

        <!-- Partnerships -->
        <div class="bg-slate-800/30 backdrop-blur-sm rounded-2xl overflow-hidden shadow-xl border border-slate-700/30">
          <div class="p-6 bg-gradient-to-r from-slate-800/50 to-slate-700/50">
            <h3 class="text-xl font-semibold flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-400" viewBox="0 0 24 24" fill="currentColor">
                <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3z"></path>
              </svg>
              <span class="bg-gradient-to-r from-white to-indigo-200 bg-clip-text text-transparent">
                Partnerships
              </span>
            </h3>
          </div>
          
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="(partnership, index) in getPartnerships()"
                   :key="index"
                   class="group bg-slate-800/40 rounded-xl p-4 border border-indigo-500/20 hover:border-indigo-500/40 transition-all duration-300 hover:shadow-lg hover:shadow-indigo-500/10">
                <!-- Partnership Header -->
                <div class="flex items-center justify-between mb-3">
                  <span class="text-sm text-slate-400">Partnership #{{ index + 1 }}</span>
                  <span class="text-xs px-2 py-1 rounded-full bg-indigo-500/20 text-indigo-400">
                    {{ Math.round((partnership.totalRuns / selectedTeam.total) * 100) }}% of total
                  </span>
                </div>

                <!-- Partnership Score -->
                <div class="flex items-baseline gap-2 mb-3">
                  <span class="text-2xl font-bold text-indigo-400">{{ partnership.totalRuns }}</span>
                  <span class="text-sm text-slate-400">runs ({{ partnership.totalBalls }} balls)</span>
                  <span class="text-sm text-indigo-400 ml-auto">
                    RR: {{ ((partnership.totalRuns / partnership.totalBalls) * 6).toFixed(2) }}
                  </span>
                </div>

                <!-- Progress Bar -->
                <div class="h-1.5 w-full bg-slate-700/30 rounded-full overflow-hidden mb-4">
                  <div class="h-full bg-gradient-to-r from-indigo-500 to-purple-500"
                       :style="{ width: `${(partnership.totalRuns / selectedTeam.total * 100)}%` }">
                  </div>
                </div>

                <!-- Batsmen Details -->
                <div class="grid grid-cols-2 gap-3 bg-slate-900/20 rounded-lg p-3">
                  <!-- Batsman 1 -->
                  <div class="space-y-2">
                    <div class="text-sm font-medium text-white truncate">{{ partnership.bat1Name }}</div>
                    <div class="flex items-baseline gap-2">
                      <span class="text-lg font-bold text-indigo-400">{{ partnership.bat1Runs }}</span>
                      <span class="text-xs text-slate-400">({{ partnership.bat1Balls }})</span>
                    </div>
                    <div class="flex gap-2 text-xs">
                      <span class="px-1.5 py-0.5 rounded-full bg-green-500/20 text-green-400">
                        {{ partnership.bat1fours }}x4
                      </span>
                      <span class="px-1.5 py-0.5 rounded-full bg-purple-500/20 text-purple-400">
                        {{ partnership.bat1sixes }}x6
                      </span>
                    </div>
                  </div>
                  <!-- Batsman 2 -->
                  <div class="space-y-2">
                    <div class="text-sm font-medium text-white truncate">{{ partnership.bat2Name }}</div>
                    <div class="flex items-baseline gap-2">
                      <span class="text-lg font-bold text-indigo-400">{{ partnership.bat2Runs }}</span>
                      <span class="text-xs text-slate-400">({{ partnership.bat2Balls }})</span>
                    </div>
                    <div class="flex gap-2 text-xs">
                      <span class="px-1.5 py-0.5 rounded-full bg-green-500/20 text-green-400">
                        {{ partnership.bat2fours }}x4
                      </span>
                      <span class="px-1.5 py-0.5 rounded-full bg-purple-500/20 text-purple-400">
                        {{ partnership.bat2sixes }}x6
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Fall of Wickets -->
        <div class="bg-slate-800/30 backdrop-blur-sm rounded-2xl overflow-hidden shadow-xl border border-slate-700/30 mt-8">
          <div class="p-6 bg-gradient-to-r from-slate-800/50 to-slate-700/50">
            <h3 class="text-xl font-semibold flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-400" viewBox="0 0 24 24" fill="currentColor">
                <path d="M13 3h-2v10h2V3zm4.83 2.17l-1.42 1.42C17.99 7.86 19 9.81 19 12c0 3.87-3.13 7-7 7s-7-3.13-7-7c0-2.19 1.01-4.14 2.58-5.42L6.17 5.17C4.23 6.82 3 9.26 3 12c0 4.97 4.03 9 9 9s9-4.03 9-9c0-2.74-1.23-5.18-3.17-6.83z"></path>
              </svg>
              <span class="bg-gradient-to-r from-white to-indigo-200 bg-clip-text text-transparent">
                Fall of Wickets
              </span>
            </h3>
          </div>
          
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="wicket in selectedTeam.wicketsData"
                   :key="wicket.wktNbr"
                   class="group bg-slate-800/40 rounded-xl p-4 border border-red-500/20 hover:border-red-500/40 transition-all duration-300 hover:shadow-lg hover:shadow-red-500/10">
                <!-- Wicket Header -->
                <div class="flex items-center justify-between mb-4">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full bg-red-500/20 flex items-center justify-center border border-red-500/30">
                      <span class="text-lg font-bold text-red-400">{{ wicket.wktNbr }}</span>
                    </div>
                    <div class="text-lg font-medium text-white truncate">{{ wicket.batName }}</div>
                  </div>
                </div>

                <!-- Progress Bar -->
                <div class="h-1.5 w-full bg-slate-700/30 rounded-full overflow-hidden mb-4">
                  <div class="h-full bg-gradient-to-r from-red-500 to-pink-500"
                       :style="{ width: `${(wicket.wktRuns / selectedTeam.total * 100)}%` }">
                  </div>
                </div>

                <!-- Wicket Details -->
                <div class="grid grid-cols-2 gap-4 bg-slate-900/20 rounded-lg p-3">
                  <div>
                    <div class="text-sm text-slate-400">Team Score</div>
                    <div class="flex items-baseline gap-2">
                      <span class="text-lg font-bold text-red-400">{{ wicket.wktRuns }}</span>
                      <span class="text-xs px-2 py-1 rounded-full bg-red-500/20 text-red-400">
                        {{ Math.round((wicket.wktRuns / selectedTeam.total) * 100) }}%
                      </span>
                    </div>
                  </div>
                  <div>
                    <div class="text-sm text-slate-400">Over</div>
                    <div class="text-lg font-bold text-red-400">{{ wicket.wktOver }}</div>
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
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'

const props = defineProps({
  match: {
    type: Object,
    required: true
  }
})

// State
const selectedTeam = ref(null)

// Get partnerships data from scorecard
const getPartnerships = () => {
  if (!selectedTeam.value || !props.match?.scoreCard) return []

  const innings = props.match.scoreCard.find(inning => 
    inning.batTeamDetails.batTeamId === selectedTeam.value.id
  )

  if (!innings?.partnershipsData) return []

  return innings.partnershipsData.map(p => ({
    bat1Name: p.bat1Name,
    bat2Name: p.bat2Name,
    totalRuns: p.totalRuns || 0,
    totalBalls: p.totalBalls || 0,
    bat1Runs: p.bat1Runs || 0,
    bat1Balls: p.bat1balls || 0,
    bat1fours: p.bat1fours || 0,
    bat1sixes: p.bat1sixes || 0,
    bat2Runs: p.bat2Runs || 0,
    bat2Balls: p.bat2balls || 0,
    bat2fours: p.bat2fours || 0,
    bat2sixes: p.bat2sixes || 0
  })).filter(p => p.totalRuns > 0) // Only show partnerships that scored runs
}

// Initialize team data from scorecard
const initializeTeamData = (teamId) => {
  if (!teamId || !props.match?.scoreCard) return null

  const innings = props.match.scoreCard.find(inning => 
    inning.batTeamDetails.batTeamId === teamId
  )
  
  const team = teamId === props.match.matchInfo.team1.id 
    ? props.match.matchInfo.team1 
    : props.match.matchInfo.team2

  if (!innings) return {
    ...team,
    battingCard: [],
    extras: { total: 0, byes: 0, legByes: 0, wides: 0, noBalls: 0 },
    total: 0,
    wickets: 0,
    overs: 0,
    runRate: 0,
    bowlingCard: [],
    wicketsData: []
  }

  return {
    ...team,
    battingCard: innings.batTeamDetails.batsmenData.map(batter => ({
      id: batter.batId,
      name: batter.batName,
      dismissal: batter.outDesc || 'not out',
      runs: batter.runs || 0,
      balls: batter.balls || 0,
      fours: batter.fours || 0,
      sixes: batter.sixes || 0,
      strikeRate: batter.strikeRate || 0
    })),
    extras: innings.extrasData || { total: 0, byes: 0, legByes: 0, wides: 0, noBalls: 0 },
    total: innings.scoreDetails.runs || 0,
    wickets: innings.scoreDetails.wickets || 0,
    overs: innings.scoreDetails.overs || 0,
    runRate: innings.scoreDetails.runRate || 0,
    bowlingCard: innings.bowlTeamDetails.bowlersData.map(bowler => ({
      id: bowler.bowlerId,
      name: bowler.bowlName,
      overs: bowler.overs || 0,
      maidens: bowler.maidens || 0,
      runs: bowler.runs || 0,
      wickets: bowler.wickets || 0,
      economy: bowler.economy || 0,
      dots: bowler.dots || 0
    })),
    wicketsData: innings.wicketsData || []
  }
}

// Initialize selected team
selectedTeam.value = initializeTeamData(props.match.matchInfo.team1.id)

// Watch for team selection changes in the UI
const handleTeamChange = (team) => {
  if (!team?.id) return
  const newTeamData = initializeTeamData(team.id)
  if (newTeamData) {
    selectedTeam.value = newTeamData
  }
}

// Watch for match data changes
watch(() => props.match, () => {
  if (selectedTeam.value?.id) {
    selectedTeam.value = initializeTeamData(selectedTeam.value.id) || initializeTeamData(props.match.matchInfo.team1.id)
  } else {
    selectedTeam.value = initializeTeamData(props.match.matchInfo.team1.id)
  }
}, { deep: true })
</script>

<style scoped>
@import './styles.css';

/* Base transitions */
.v-enter-active,
.v-leave-active {
  transition: all 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Grid pattern background */
.bg-grid-pattern {
  background-image: radial-gradient(circle, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
}

/* Smooth transitions */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

/* Gradient text */
.gradient-text {
  @apply bg-gradient-to-r from-white to-indigo-200 bg-clip-text text-transparent;
}

/* Glass effect */
.glass-effect {
  @apply backdrop-blur-sm bg-slate-800/30 border border-slate-700/30;
}

/* Animations */
@keyframes glow {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

@keyframes progress {
  from { 
    width: 0;
    opacity: 0;
  }
  to { 
    width: 100%;
    opacity: 1;
  }
}

.animate-glow {
  animation: glow 2s ease-in-out infinite;
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

.progress-bar {
  animation: progress 2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
  }
  
  .partnership-grid {
    grid-template-columns: 1fr;
  }
}

/* Hover effects */
.hover-lift {
  transition: transform 0.2s ease;
}

.hover-lift:hover {
  transform: translateY(-2px);
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

/* Enhanced hover effects */
.hover-scale {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.hover-scale:hover {
  transform: scale(1.02);
}

/* Glow effects */
.glow {
  box-shadow: 0 0 15px rgba(99, 102, 241, 0.5);
}

.glow-red {
  box-shadow: 0 0 15px rgba(239, 68, 68, 0.5);
}

/* Card hover effects */
.group:hover {
  transform: translateY(-2px);
}
</style> 