<!-- MatchDetails.vue -->
<template>
  <div class="container mx-auto px-4 py-8 space-y-8">
    <!-- Match Header with Enhanced Details -->
    <div class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-lg p-6 shadow-xl border border-slate-700/30">
      <!-- Series Info Banner -->
      <div class="mb-6 flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-white">{{ match.matchInfo.series.name }}</h1>
          <p class="text-slate-400 text-sm">{{ match.matchInfo.matchDescription }}</p>
        </div>
        <div class="px-3 py-1 bg-indigo-600/20 rounded-full text-xs font-medium text-indigo-400">
          {{ match.matchInfo.series.seriesType }}
        </div>
      </div>

      <!-- Match Result Banner -->
      <div v-if="match.matchInfo.state.toLowerCase() === 'complete'" 
           class="mb-6 p-4 bg-gradient-to-r from-indigo-900/30 to-slate-800/50 rounded-lg flex flex-col md:flex-row items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-indigo-500/20 rounded-full flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-slate-400 text-sm">Match Result</p>
            <p class="text-xl font-bold text-white">
              {{ getWinningTeamName() }} won by 
              {{ match.matchInfo.result.winningMargin }} 
              {{ match.matchInfo.result.winByRuns ? 'runs' : 'wickets' }}
            </p>
          </div>
        </div>
        
        <div v-if="match.matchInfo.playersOfTheMatch && match.matchInfo.playersOfTheMatch.length" 
             class="mt-4 md:mt-0 flex items-center space-x-3">
          <div>
            <p class="text-slate-400 text-sm text-right">Player of the Match</p>
            <p class="text-lg font-bold text-white text-right">{{ match.matchInfo.playersOfTheMatch[0].fullName }}</p>
          </div>
          <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${match.matchInfo.playersOfTheMatch[0].faceImageId}/i.jpg?p=thumb`" 
               :alt="match.matchInfo.playersOfTheMatch[0].name"
               class="w-12 h-12 rounded-full border-2 border-indigo-500/30">
        </div>
      </div>

      <!-- Teams -->
      <div class="flex flex-col md:flex-row items-center justify-between gap-6 mb-6">
        <div class="flex items-center gap-4">
          <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${match.squad.team1.team.imageId}/i.jpg?p=thumb`" 
               :alt="match.matchInfo.team1.name" 
               class="w-16 h-16 rounded-full shadow-lg border-2 border-slate-700">
          <div class="text-center md:text-left">
            <h3 class="text-xl font-bold text-white">{{ match.matchInfo.team1.name }}</h3>
            <p class="text-slate-400">{{ getTeamScore(match.matchInfo.team1.id) }}</p>
          </div>
        </div>
        
        <div class="flex flex-col items-center gap-2">
          <span class="text-sm font-medium px-4 py-1.5 rounded-full shadow-md"
                :class="match.matchInfo.state.toLowerCase() === 'complete' ? 'bg-slate-700 text-slate-300' : 'bg-red-500/20 text-red-400 animate-pulse'">
            {{ match.matchInfo.state.toLowerCase() === 'complete' ? match.matchInfo.shortStatus : match.matchInfo.status }}
          </span>
        </div>
        
        <div class="flex items-center gap-4">
          <div class="text-center md:text-right">
            <h3 class="text-xl font-bold text-white">{{ match.matchInfo.team2.name }}</h3>
            <p class="text-slate-400">{{ getTeamScore(match.matchInfo.team2.id) }}</p>
          </div>
          <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${match.squad.team2.team.imageId}/i.jpg?p=thumb`" 
               :alt="match.matchInfo.team2.name" 
               class="w-16 h-16 rounded-full shadow-lg border-2 border-slate-700">
        </div>
      </div>

      <!-- Venue Info with Stadium Visualization -->
      <div class="bg-slate-800/60 rounded-lg p-4 mb-6">
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-10 h-10 rounded-full bg-slate-700/80 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <div>
            <h3 class="text-white font-medium">{{ match.matchInfo.venue.name }}</h3>
            <p class="text-sm text-slate-400">{{ match.matchInfo.venue.city }}, {{ match.matchInfo.venue.country }}</p>
          </div>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
          <div class="bg-slate-700/40 rounded p-2 text-center">
            <p class="text-xs text-slate-400">Capacity</p>
            <p class="text-sm font-medium text-white">{{ match.venueInfo?.capacity || 'N/A' }}</p>
          </div>
          <div class="bg-slate-700/40 rounded p-2 text-center">
            <p class="text-xs text-slate-400">Floodlights</p>
            <p class="text-sm font-medium text-white">{{ match.venueInfo?.floodlights ? 'Yes' : 'No' }}</p>
          </div>
          <div class="bg-slate-700/40 rounded p-2 text-center">
            <p class="text-xs text-slate-400">Established</p>
            <p class="text-sm font-medium text-white">{{ match.venueInfo?.established || 'N/A' }}</p>
          </div>
          <div class="bg-slate-700/40 rounded p-2 text-center">
            <p class="text-xs text-slate-400">Known As</p>
            <p class="text-sm font-medium text-white">{{ match.venueInfo?.knownAs || 'N/A' }}</p>
          </div>
        </div>

        <div v-if="match.venueInfo?.ends" class="bg-slate-700/40 rounded p-2 mb-3">
          <p class="text-xs text-slate-400 mb-1">Ends</p>
          <div class="flex justify-between">
            <span class="text-sm font-medium text-white">{{ match.venueInfo.ends.split(',')[0] }}</span>
            <span class="text-sm font-medium text-white">{{ match.venueInfo.ends.split(',')[1] }}</span>
          </div>
        </div>
        
        <div v-if="match.venueInfo?.profile" class="bg-slate-700/40 rounded p-2">
          <p class="text-xs text-slate-400 mb-1">Pitch Profile</p>
          <p class="text-sm text-white">{{ match.venueInfo.profile }}</p>
        </div>
      </div>

      <!-- Match Info Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="text-center p-3 rounded-lg bg-slate-700/50 hover:bg-slate-700/70 transition-colors">
          <p class="text-sm text-slate-400">Format</p>
          <p class="font-medium text-white">{{ match.matchInfo.matchFormat }}</p>
        </div>
        <div class="text-center p-3 rounded-lg bg-slate-700/50 hover:bg-slate-700/70 transition-colors">
          <p class="text-sm text-slate-400">Toss</p>
          <p class="font-medium text-white">{{ getTossResult }}</p>
        </div>
        <div class="text-center p-3 rounded-lg bg-slate-700/50 hover:bg-slate-700/70 transition-colors">
          <p class="text-sm text-slate-400">Match Date</p>
          <p class="font-medium text-white">{{ formatDate(match.matchInfo.matchStartTimestamp) }}</p>
        </div>
        <div class="text-center p-3 rounded-lg bg-slate-700/50 hover:bg-slate-700/70 transition-colors">
          <p class="text-sm text-slate-400">Day/Night</p>
          <p class="font-medium text-white">{{ match.matchInfo.dayNight ? 'Yes' : 'No' }}</p>
        </div>
      </div>
    </div>

    <!-- Broadcast Information -->
    <div v-if="match.broadcastInfo && match.broadcastInfo.length" class="bg-slate-800 rounded-lg p-4 shadow-lg">
      <h3 class="text-lg font-bold text-white mb-3 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
        Broadcast Information
      </h3>
      <div class="space-y-3">
        <div v-for="broadcast in match.broadcastInfo" :key="broadcast.country" class="bg-slate-700/30 rounded-lg p-3">
          <div class="flex items-center mb-2">
            <span class="text-sm font-medium text-white">{{ getCountryName(broadcast.country) }}</span>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div v-for="(caster, index) in broadcast.broadcaster" :key="index" 
                 class="bg-slate-800/50 rounded p-2 flex items-center">
              <div class="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center mr-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path v-if="caster.broadcastType === 'TV'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.636 18.364a9 9 0 010-12.728m12.728 0a9 9 0 010 12.728m-9.9-2.829a5 5 0 010-7.07m7.072 0a5 5 0 010 7.07M13 12a1 1 0 11-2 0 1 1 0 012 0z" />
                </svg>
              </div>
              <div class="flex-1">
                <p class="text-xs text-slate-400">{{ caster.broadcastType }}</p>
                <p class="text-sm font-medium text-white">{{ caster.value }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Match Officials and Umpires -->
    <div class="bg-slate-800 rounded-lg p-4 shadow-lg mb-6">
      <h3 class="text-lg font-bold text-white mb-3 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        Match Officials
      </h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-slate-700/30 rounded-lg p-3">
          <h4 class="text-sm text-indigo-400 mb-2">Umpires</h4>
          <div class="space-y-3">
            <div v-if="match.matchInfo.umpire1" class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="w-8 h-8 rounded-full bg-slate-600 flex items-center justify-center mr-2">
                  <span class="text-xs font-medium text-white">U1</span>
                </div>
                <span class="text-sm font-medium text-white">{{ match.matchInfo.umpire1.name }}</span>
              </div>
              <span class="text-xs text-slate-400">{{ match.matchInfo.umpire1.country }}</span>
            </div>
            
            <div v-if="match.matchInfo.umpire2" class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="w-8 h-8 rounded-full bg-slate-600 flex items-center justify-center mr-2">
                  <span class="text-xs font-medium text-white">U2</span>
                </div>
                <span class="text-sm font-medium text-white">{{ match.matchInfo.umpire2.name }}</span>
              </div>
              <span class="text-xs text-slate-400">{{ match.matchInfo.umpire2.country }}</span>
            </div>
            
            <div v-if="match.matchInfo.umpire3" class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="w-8 h-8 rounded-full bg-slate-600 flex items-center justify-center mr-2">
                  <span class="text-xs font-medium text-white">TV</span>
                </div>
                <span class="text-sm font-medium text-white">{{ match.matchInfo.umpire3.name }}</span>
              </div>
              <span class="text-xs text-slate-400">{{ match.matchInfo.umpire3.country }}</span>
            </div>
          </div>
        </div>
        
        <div class="bg-slate-700/30 rounded-lg p-3">
          <h4 class="text-sm text-indigo-400 mb-2">Match Referee</h4>
          <div v-if="match.matchInfo.referee" class="flex items-center justify-between">
            <div class="flex items-center">
              <div class="w-8 h-8 rounded-full bg-slate-600 flex items-center justify-center mr-2">
                <span class="text-xs font-medium text-white">R</span>
              </div>
              <span class="text-sm font-medium text-white">{{ match.matchInfo.referee.name }}</span>
            </div>
            <span class="text-xs text-slate-400">{{ match.matchInfo.referee.country }}</span>
          </div>
          
          <!-- Additional Venue Details -->
          <div class="mt-4 pt-4 border-t border-slate-600/30">
            <h4 class="text-sm text-indigo-400 mb-2">Additional Details</h4>
            <div class="grid grid-cols-2 gap-2">
              <div class="bg-slate-800/50 rounded p-2">
                <p class="text-xs text-slate-400">Match Type</p>
                <p class="text-sm font-medium text-white">{{ match.matchInfo.matchType }}</p>
              </div>
              <div class="bg-slate-800/50 rounded p-2">
                <p class="text-xs text-slate-400">Known As</p>
                <p class="text-sm font-medium text-white">{{ match.venueInfo?.knownAs || 'N/A' }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tab Navigation -->
    <div class="relative">
      <div class="overflow-x-auto hide-scrollbar">
        <div class="flex gap-4 px-4">
          <button v-for="tab in tabs"
                  :key="tab.value"
                  @click="activeTab = tab.value"
                  class="px-4 py-2 whitespace-nowrap font-medium transition-colors relative"
                  :class="activeTab === tab.value ? 'text-indigo-400' : 'text-slate-400 hover:text-slate-300'">
            {{ tab.label }}
            <div v-if="activeTab === tab.value"
                 class="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-indigo-500 to-indigo-400"></div>
          </button>
        </div>
      </div>
    </div>

    <!-- Tab Content -->
    <div class="bg-gradient-to-br from-slate-800 to-slate-900 rounded-lg p-6 shadow-lg border border-slate-700/30">
      <component :is="currentTab" 
                :match="match" 
                :matchData="match"
                :loading="loading">
      </component>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import RunRateAnalysis from '../components/match-details/RunRateAnalysis.vue'
import PartnershipAnalysis from '../components/match-details/PartnershipAnalysis.vue'
import BattingAnalysis from '../components/match-details/BattingAnalysis.vue'
import BowlingAnalysis from '../components/match-details/BowlingAnalysis.vue'
import PlayerDetails from '../components/match-details/PlayerDetails.vue'
import MatchOfficials from '../components/match-details/MatchOfficials.vue'
import Commentary from '../components/match-details/Commentary.vue'
import Highlights from '../components/match-details/Highlights.vue'
import Scorecard from '../components/match-details/Scorecard.vue'
import MatchOversAnalysis from '../components/match-details/MatchOversAnalysis.vue'
import matchInfo from '../sample-responses/match-info.json'
import matchScoreCard from '../sample-responses/match-score-card.json'
import matchHighlights from '../sample-responses/match-highlights.json'
import matchSquad from '../sample-responses/match-squad.json'
import matchCommentary from '../sample-responses/commentry.json'
import matchOvers from '../sample-responses/match-overs.json'

// Loading state
const loading = ref(false)

// Match data from JSON files
const match = ref({
  matchInfo: {
    matchId: 0,
    matchDescription: '',
    matchFormat: '',
    matchType: '',
    complete: false,
    domestic: false,
    matchStartTimestamp: 0,
    matchCompleteTimestamp: 0,
    dayNight: false,
    year: 0,
    state: '',
    status: '',
    team1: {
      id: 0,
      name: '',
      playerDetails: [],
      shortName: ''
    },
    team2: {
      id: 0,
      name: '',
      playerDetails: [],
      shortName: ''
    },
    venue: {
      id: 0,
      name: '',
      city: '',
      country: ''
    },
    tossResults: {
      tossWinnerId: 0,
      tossWinnerName: '',
      decision: ''
    },
    result: {
      resultType: '',
      winningTeam: '',
      winningteamId: 0,
      winningMargin: 0,
      winByRuns: false,
      winByInnings: false
    },
    series: {
      id: 0,
      name: '',
      seriesType: ''
    }
  },
  scoreCard: [],
  matchHighlights: [],
  squad: {
    team1: {
      team: {
        teamId: 0,
        teamName: '',
        teamSName: '',
        imageId: 0
      },
      players: {
        'playing XI': [],
        bench: []
      }
    },
    team2: {
      team: {
        teamId: 0,
        teamName: '',
        teamSName: '',
        imageId: 0
      },
      players: {
        'playing XI': [],
        bench: []
      }
    }
  },
  commentary:[]
})

// Load match data
const loadMatchData = async () => {
  try {
    loading.value = true;
    match.value = {
      matchInfo: matchInfo.matchInfo,
      scoreCard: matchScoreCard.scoreCard,
      matchHighlights: matchHighlights.commentaryList,
      squad: matchSquad,
      commentary: matchCommentary,
      overs: matchOvers,
      matchHeader: matchInfo,
      venueInfo: matchInfo.venueInfo,
      broadcastInfo: matchInfo.broadcastInfo
    };
    loading.value = false;
  } catch (error) {
    console.error('Error loading match data:', error);
    loading.value = false;
  }
}

// Load data on component mount
loadMatchData()

// Helper functions
const getTeamScore = (teamId) => {
  const innings = match.value.scoreCard?.find(inning => inning.batTeamDetails.batTeamId === teamId)
  if (!innings) return ''
  const { runs, wickets, overs } = innings.scoreDetails
  const extras = innings.extrasData.total
  return `${runs}/${wickets} (${overs})${extras ? ` (${extras} extras)` : ''}`
}

const getTossResult = computed(() => {
  const toss = match.value.matchInfo?.tossResults
  if (!toss) return ''
  return `${toss.tossWinnerName} won & ${toss.decision.toLowerCase()}`
})

const getWinningTeamName = () => {
  const result = match.value.matchInfo?.result
  if (!result || !result.winningTeam) return ''
  return result.winningTeam
}

const formatDate = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

const getCountryName = (code) => {
  const countries = {
    'IN': 'India',
    'US': 'United States',
    'UK': 'United Kingdom',
    'AU': 'Australia',
    'NZ': 'New Zealand',
    'SA': 'South Africa',
    'PAK': 'Pakistan'
  }
  return countries[code] || code
}

// Tabs configuration
const tabs = [
  { label: 'Scorecard', value: 'scorecard' },
  { label: 'Commentary', value: 'commentary' },
  { label: 'Run Rate Analysis', value: 'run-rate' },
  { label: 'Over-by-Over Analysis', value: 'over-analysis' },
  { label: 'Partnership Analysis', value: 'partnership' },
  { label: 'Batting Analysis', value: 'batting' },
  { label: 'Bowling Analysis', value: 'bowling' },
  { label: 'Player Details', value: 'players' },
  { label: 'Match Officials', value: 'officials' },
  { label: 'Highlights', value: 'highlights' }
]

const activeTab = ref('scorecard')

// Map tab values to components
const tabComponents = {
  'scorecard': Scorecard,
  'commentary': Commentary,
  'run-rate': RunRateAnalysis,
  'over-analysis': MatchOversAnalysis,
  'partnership': PartnershipAnalysis,
  'batting': BattingAnalysis,
  'bowling': BowlingAnalysis,
  'players': PlayerDetails,
  'officials': MatchOfficials,
  'highlights': Highlights
}

// Current active component
const currentTab = computed(() => tabComponents[activeTab.value])
</script>

<style scoped>
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}
</style>