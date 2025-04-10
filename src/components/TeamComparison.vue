<template>
  <div class="container mx-auto px-4 py-8 space-y-8">
    <!-- Team Selection Section -->
    <div class="bg-slate-800/60 rounded-lg p-6 backdrop-blur-sm">
      <div class="flex items-center space-x-3 mb-6">
        <div class="w-10 h-10 bg-indigo-500/20 rounded-full flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <h2 class="text-xl font-bold text-white">Team Comparison</h2>
      </div>
      
      <!-- Team Selection Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-for="(team, index) in selectedTeams" :key="index" 
             class="bg-slate-700/40 rounded-lg p-4 transform hover:scale-105 transition-all duration-300 hover:bg-slate-700/60">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center border border-blue-500/20">
                <img 
                  :src="getTeamImage(team.imageId)" 
                  :alt="team.name"
                  class="w-full h-full rounded-full object-cover"
                />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-white">{{ team.name }}</h3>
                <p class="text-sm text-slate-400">{{ team.shortName }}</p>
              </div>
            </div>
            <button @click="removeTeam(team.id)"
                    class="text-slate-400 hover:text-red-400 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <div class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span class="text-slate-400">Matches</span>
              <span class="text-white font-medium">{{ getTeamStats(team.id).totalMatches }}</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-slate-400">Win Rate</span>
              <span class="text-white font-medium">{{ getTeamStats(team.id).winRate }}</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-slate-400">Highest Score</span>
              <span class="text-white font-medium">{{ getTeamStats(team.id).highestScore }}</span>
            </div>
          </div>
        </div>
        
        <!-- Add Team Button -->
        <div v-if="selectedTeams.length < 3" 
             class="bg-slate-700/40 rounded-lg p-4 flex items-center justify-center cursor-pointer transform hover:scale-105 transition-all duration-300 hover:bg-slate-700/60"
             @click="showTeamSelector = true">
          <div class="text-center">
            <div class="w-12 h-12 bg-indigo-500/20 rounded-full flex items-center justify-center mx-auto mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            </div>
            <p class="text-slate-400">Add Team</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Comparison Stats -->
    <div v-if="selectedTeams.length >= 2" class="space-y-6">
      <!-- Head to Head Stats -->
      <div class="bg-slate-800/60 rounded-lg p-6 backdrop-blur-sm">
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-10 h-10 bg-indigo-500/20 rounded-full flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-bold text-white">Head to Head Statistics</h3>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div v-for="stat in headToHeadStats" :key="stat.label" 
               class="bg-slate-700/40 rounded-lg p-4 text-center">
            <p class="text-sm text-slate-400 mb-1">{{ stat.label }}</p>
            <p class="text-xl font-bold text-white">{{ stat.value }}</p>
          </div>
        </div>
      </div>

      <!-- Performance Comparison -->
      <div class="bg-slate-800/60 rounded-lg p-6 backdrop-blur-sm">
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-10 h-10 bg-indigo-500/20 rounded-full flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <h3 class="text-lg font-bold text-white">Performance Comparison</h3>
        </div>
        <div class="space-y-4">
          <div v-for="metric in performanceMetrics" :key="metric.label" class="space-y-2">
            <div class="flex items-center justify-between text-sm">
              <span class="text-slate-400">{{ metric.label }}</span>
              <span class="text-white font-medium">{{ metric.value }}</span>
            </div>
            <div class="h-2 bg-slate-700/40 rounded-full overflow-hidden">
              <div class="h-full bg-indigo-500 rounded-full" :style="{ width: metric.percentage + '%' }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Matches -->
      <div class="bg-slate-800/60 rounded-lg p-6 backdrop-blur-sm">
        <div class="flex items-center space-x-3 mb-4">
          <div class="w-10 h-10 bg-indigo-500/20 rounded-full flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 class="text-lg font-bold text-white">Recent Matches</h3>
        </div>
        <div class="space-y-4">
          <div v-for="match in recentMatches" :key="match.matchId" 
               class="bg-slate-700/40 rounded-lg p-4">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-3">
                <img :src="getTeamImage(match.team1.imageId)" 
                     :alt="match.team1.name"
                     class="w-8 h-8 rounded-full border-2 border-slate-600" />
                <span class="text-sm font-medium text-white">{{ match.team1.shortName }}</span>
              </div>
              <span class="text-sm font-medium text-indigo-400">VS</span>
              <div class="flex items-center space-x-3">
                <span class="text-sm font-medium text-white">{{ match.team2.shortName }}</span>
                <img :src="getTeamImage(match.team2.imageId)" 
                     :alt="match.team2.name"
                     class="w-8 h-8 rounded-full border-2 border-slate-600" />
              </div>
            </div>
            <div class="text-center">
              <p class="text-sm text-slate-300">{{ formatDate(match.startDate) }}</p>
              <p class="text-xs text-slate-400">{{ match.status }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Team Selector Modal -->
    <div v-if="showTeamSelector" 
         class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
         @click.self="showTeamSelector = false">
      <div class="bg-slate-800/90 rounded-xl p-6 w-full max-w-md mx-4 transform transition-all duration-300 scale-100">
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-indigo-500/20 rounded-full flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-bold text-white">Select Team</h3>
          </div>
          <button @click="showTeamSelector = false" 
                  class="text-slate-400 hover:text-white transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <!-- Search Bar -->
        <div class="relative mb-4">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search teams..." 
            class="w-full pl-10 pr-4 py-2 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          />
        </div>
        
        <!-- Filter Tabs -->
        <div class="flex space-x-2 mb-4 overflow-x-auto pb-2">
          <button 
            v-for="category in teamCategories" 
            :key="category.id"
            @click="selectedCategory = category.id"
            :class="[
              'px-3 py-1 rounded-full text-sm font-medium whitespace-nowrap transition-colors',
              selectedCategory === category.id 
                ? 'bg-indigo-500 text-white' 
                : 'bg-slate-700/50 text-slate-300 hover:bg-slate-700'
            ]"
          >
            {{ category.name }}
          </button>
        </div>
        
        <!-- Team List -->
        <div class="space-y-2 max-h-[50vh] overflow-y-auto pr-2">
          <div v-for="team in filteredTeamsList" :key="team.teamId" 
               class="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-700/50 cursor-pointer transition-all duration-300 hover:scale-105"
               @click="addTeam(team)">
            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center border border-blue-500/20">
              <img 
                :src="getTeamImage(team.imageId)" 
                :alt="team.teamName"
                class="w-full h-full rounded-full object-cover"
              />
            </div>
            <div class="flex-1">
              <h4 class="font-medium text-slate-200">{{ team.teamName }}</h4>
              <p class="text-sm text-slate-400">{{ team.teamSName }}</p>
              <p v-if="team.countryName" class="text-xs text-slate-500">{{ team.countryName }}</p>
            </div>
          </div>
          
          <!-- No Results Message -->
          <div v-if="filteredTeamsList.length === 0" class="text-center py-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-slate-500 mx-auto mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-slate-400">No teams found matching your search</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import teamDetailsInt from '../sample-responses/team-details-int.json'

const selectedTeams = ref([])
const showTeamSelector = ref(false)
const searchQuery = ref('')
const selectedCategory = ref('all')
const isLoading = ref(false)
const errorMessage = ref('')

// Store team data
const teamResultsData = ref({})
const teamPlayersData = ref({})

// Store computed stats
const teamStats = ref({})
const headToHeadStatsData = ref([])
const performanceMetricsData = ref([])
const recentMatchesData = ref([])

// Team categories for filtering
const teamCategories = [
  { id: 'all', name: 'All Teams' },
  { id: 'test', name: 'Test Teams' },
  { id: 'associate', name: 'Associate Teams' }
]

// Process teams from team-details-int.json
const availableTeams = computed(() => {
  return teamDetailsInt.list.filter(team => team.teamId && team.teamName && team.teamSName)
})

// Filter teams based on search query and category
const filteredTeamsList = computed(() => {
  let filtered = availableTeams.value
  
  // Apply category filter
  if (selectedCategory.value !== 'all') {
    if (selectedCategory.value === 'test') {
      // Test teams are typically the first 12 teams in the list
      filtered = filtered.slice(0, 12)
    } else if (selectedCategory.value === 'associate') {
      // Associate teams are the rest
      filtered = filtered.slice(12)
    }
  }
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(team => 
      team.teamName.toLowerCase().includes(query) || 
      team.teamSName.toLowerCase().includes(query) ||
      (team.countryName && team.countryName.toLowerCase().includes(query))
    )
  }
  
  // Exclude already selected teams
  filtered = filtered.filter(team => 
    !selectedTeams.value.find(t => t.teamId === team.teamId)
  )
  
  return filtered
})

// Get team image URL
const getTeamImage = (imageId) => {
  if (!imageId) return ''
  return 'http://static.cricbuzz.com/a/img/v1/i1/c' + imageId + '/i.jpg?p=thumb'
}

// Fetch team results data
const fetchTeamResults = async (teamId) => {
  if (!teamId) return null
  if (teamResultsData.value[teamId]) return teamResultsData.value[teamId]
  
  try {
    isLoading.value = true
    errorMessage.value = ''
    
    const response = await fetch(`https://Cricbuzz-Official-Cricket-API.proxy-production.allthingsdev.co/team/${teamId}/result`, {
      headers: {
        'x-apihub-key': 'kdsEAjlPR-s-b0PcUssh24FaSMnF6Zb8NwiRaYxWXvRhYmgoWR',
        'x-apihub-host': 'Cricbuzz-Official-Cricket-API.allthingsdev.co',
        'x-apihub-endpoint': '0aa890a7-1fe7-4e5a-947d-4c7d61b7f706'
      }
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch team results: ${response.status}`)
    }
    
    const data = await response.json()
    teamResultsData.value[teamId] = data
    return data
  } catch (error) {
    console.error('Error fetching team results:', error)
    errorMessage.value = `Failed to load team results: ${error.message}`
    return null
  } finally {
    isLoading.value = false
  }
}

// Fetch team players data
const fetchTeamPlayers = async (teamId) => {
  if (!teamId) return null
  if (teamPlayersData.value[teamId]) return teamPlayersData.value[teamId]
  
  try {
    isLoading.value = true
    errorMessage.value = ''
    
    const response = await fetch(`https://Cricbuzz-Official-Cricket-API.proxy-production.allthingsdev.co/team/${teamId}/players`, {
      headers: {
        'x-apihub-key': 'kdsEAjlPR-s-b0PcUssh24FaSMnF6Zb8NwiRaYxWXvRhYmgoWR',
        'x-apihub-host': 'Cricbuzz-Official-Cricket-API.allthingsdev.co',
        'x-apihub-endpoint': '2b298a5d-fb51-4e29-aa15-c5385291fcd8'
      }
    })
    
    if (!response.ok) {
      throw new Error(`Failed to fetch team players: ${response.status}`)
    }
    
    const data = await response.json()
    teamPlayersData.value[teamId] = data
    return data
  } catch (error) {
    console.error('Error fetching team players:', error)
    errorMessage.value = `Failed to load team players: ${error.message}`
    return null
  } finally {
    isLoading.value = false
  }
}

// Get team stats from actual match data
const getTeamStats = (teamId) => {
  if (!teamId) return { totalMatches: '0', winRate: '0%', highestScore: '0' }
  return teamStats.value[teamId] || { totalMatches: '0', winRate: '0%', highestScore: '0' }
}

// Calculate team stats
const calculateTeamStats = async (teamId) => {
  if (!teamId) return
  
  const teamResults = await fetchTeamResults(teamId)
  if (!teamResults) return
  
  // Find all matches for this team
  const teamMatches = teamResults.teamMatchesData.flatMap(series => 
    series.matchDetailsMap.match.filter(match => 
      match.matchInfo.team1.teamId === teamId || match.matchInfo.team2.teamId === teamId
    )
  )
  
  // Calculate stats
  const totalMatches = teamMatches.length
  const wins = teamMatches.filter(match => {
    const isTeam1 = match.matchInfo.team1.teamId === teamId
    const isTeam2 = match.matchInfo.team2.teamId === teamId
    
    if (isTeam1) {
      return match.matchInfo.status.includes(match.matchInfo.team1.teamName)
    } else if (isTeam2) {
      return match.matchInfo.status.includes(match.matchInfo.team2.teamName)
    }
    return false
  }).length
  
  const winRate = totalMatches > 0 ? ((wins / totalMatches) * 100).toFixed(1) : 0
  
  // Find highest score
  const highestScore = teamMatches.reduce((highest, match) => {
    const isTeam1 = match.matchInfo.team1.teamId === teamId
    const isTeam2 = match.matchInfo.team2.teamId === teamId
    
    if (isTeam1 && match.matchScore.team1Score.inngs1) {
      const score = match.matchScore.team1Score.inngs1.runs
      return score > highest ? score : highest
    } else if (isTeam2 && match.matchScore.team2Score.inngs1) {
      const score = match.matchScore.team2Score.inngs1.runs
      return score > highest ? score : highest
    }
    return highest
  }, 0)
  
  teamStats.value[teamId] = {
    totalMatches: totalMatches.toString(),
    winRate: `${winRate}%`,
    highestScore: `${highestScore}`
  }
}

// Calculate head-to-head stats between selected teams
const calculateHeadToHeadStats = async () => {
  if (selectedTeams.value.length < 2) {
    headToHeadStatsData.value = []
    return
  }
  
  const team1Id = selectedTeams.value[0].teamId
  const team2Id = selectedTeams.value[1].teamId
  
  if (!team1Id || !team2Id) {
    headToHeadStatsData.value = []
    return
  }
  
  // Fetch data for both teams
  const team1Results = await fetchTeamResults(team1Id)
  const team2Results = await fetchTeamResults(team2Id)
  
  if (!team1Results || !team2Results) {
    headToHeadStatsData.value = []
    return
  }
  
  // Find all matches between these two teams
  const headToHeadMatches = team1Results.teamMatchesData.flatMap(series => 
    series.matchDetailsMap.match.filter(match => 
      (match.matchInfo.team1.teamId === team1Id && match.matchInfo.team2.teamId === team2Id) ||
      (match.matchInfo.team1.teamId === team2Id && match.matchInfo.team2.teamId === team1Id)
    )
  )
  
  const totalMatches = headToHeadMatches.length
  
  // Count wins for each team
  const team1Wins = headToHeadMatches.filter(match => 
    match.matchInfo.status.includes(selectedTeams.value[0].teamName)
  ).length
  
  const team2Wins = headToHeadMatches.filter(match => 
    match.matchInfo.status.includes(selectedTeams.value[1].teamName)
  ).length
  
  const draws = totalMatches - team1Wins - team2Wins
  
  // Calculate average scores
  const team1Scores = headToHeadMatches.filter(match => match.matchInfo.team1.teamId === team1Id)
    .map(match => match.matchScore.team1Score.inngs1?.runs || 0)
  
  const team2Scores = headToHeadMatches.filter(match => match.matchInfo.team2.teamId === team1Id)
    .map(match => match.matchScore.team2Score.inngs1?.runs || 0)
  
  const team1AvgScore = team1Scores.length > 0 
    ? (team1Scores.reduce((sum, score) => sum + score, 0) / team1Scores.length).toFixed(1)
    : 0
  
  const team2Scores1 = headToHeadMatches.filter(match => match.matchInfo.team1.teamId === team2Id)
    .map(match => match.matchScore.team1Score.inngs1?.runs || 0)
  
  const team2Scores2 = headToHeadMatches.filter(match => match.matchInfo.team2.teamId === team2Id)
    .map(match => match.matchScore.team2Score.inngs1?.runs || 0)
  
  const team2AvgScore = (team2Scores1.length + team2Scores2.length) > 0
    ? ((team2Scores1.reduce((sum, score) => sum + score, 0) + 
        team2Scores2.reduce((sum, score) => sum + score, 0)) / 
       (team2Scores1.length + team2Scores2.length)).toFixed(1)
    : 0
  
  headToHeadStatsData.value = [
    { label: 'Total Matches', value: totalMatches.toString() },
    { label: `${selectedTeams.value[0].shortName} Wins`, value: team1Wins.toString() },
    { label: `${selectedTeams.value[1].shortName} Wins`, value: team2Wins.toString() },
    { label: 'Draws', value: draws.toString() },
    { label: `${selectedTeams.value[0].shortName} Avg Score`, value: team1AvgScore },
    { label: `${selectedTeams.value[1].shortName} Avg Score`, value: team2AvgScore }
  ]
}

// Calculate performance metrics
const calculatePerformanceMetrics = async () => {
  if (selectedTeams.value.length < 2) {
    performanceMetricsData.value = []
    return
  }
  
  const team1Id = selectedTeams.value[0].teamId
  const team2Id = selectedTeams.value[1].teamId
  
  if (!team1Id || !team2Id) {
    performanceMetricsData.value = []
    return
  }
  
  // Fetch data for both teams
  const team1Results = await fetchTeamResults(team1Id)
  const team2Results = await fetchTeamResults(team2Id)
  
  if (!team1Results || !team2Results) {
    performanceMetricsData.value = []
    return
  }
  
  // Find all matches for both teams
  const team1Matches = team1Results.teamMatchesData.flatMap(series => 
    series.matchDetailsMap.match.filter(match => 
      match.matchInfo.team1.teamId === team1Id || match.matchInfo.team2.teamId === team1Id
    )
  )
  
  const team2Matches = team2Results.teamMatchesData.flatMap(series => 
    series.matchDetailsMap.match.filter(match => 
      match.matchInfo.team1.teamId === team2Id || match.matchInfo.team2.teamId === team2Id
    )
  )
  
  // Calculate batting average (runs per wicket)
  const team1BattingAvg = calculateBattingAverage(team1Matches, team1Id)
  const team2BattingAvg = calculateBattingAverage(team2Matches, team2Id)
  
  // Calculate bowling average (runs per wicket)
  const team1BowlingAvg = calculateBowlingAverage(team1Matches, team1Id)
  const team2BowlingAvg = calculateBowlingAverage(team2Matches, team2Id)
  
  // Calculate run rate
  const team1RunRate = calculateRunRate(team1Matches, team1Id)
  const team2RunRate = calculateRunRate(team2Matches, team2Id)
  
  // Calculate win percentage
  const team1WinPct = calculateWinPercentage(team1Matches, team1Id, selectedTeams.value[0].teamName)
  const team2WinPct = calculateWinPercentage(team2Matches, team2Id, selectedTeams.value[1].teamName)
  
  // Find the maximum values for percentage calculations
  const maxBattingAvg = Math.max(team1BattingAvg, team2BattingAvg)
  const maxBowlingAvg = Math.max(team1BowlingAvg, team2BowlingAvg)
  const maxRunRate = Math.max(team1RunRate, team2RunRate)
  const maxWinPct = Math.max(team1WinPct, team2WinPct)
  
  performanceMetricsData.value = [
    { 
      label: 'Batting Average', 
      value: `${team1BattingAvg.toFixed(2)} vs ${team2BattingAvg.toFixed(2)}`, 
      percentage: maxBattingAvg > 0 ? (team1BattingAvg / maxBattingAvg * 100) : 50 
    },
    { 
      label: 'Bowling Average', 
      value: `${team1BowlingAvg.toFixed(2)} vs ${team2BowlingAvg.toFixed(2)}`, 
      percentage: maxBowlingAvg > 0 ? (team1BowlingAvg / maxBowlingAvg * 100) : 50 
    },
    { 
      label: 'Run Rate', 
      value: `${team1RunRate.toFixed(2)} vs ${team2RunRate.toFixed(2)}`, 
      percentage: maxRunRate > 0 ? (team1RunRate / maxRunRate * 100) : 50 
    },
    { 
      label: 'Win Percentage', 
      value: `${team1WinPct.toFixed(1)}% vs ${team2WinPct.toFixed(1)}%`, 
      percentage: maxWinPct > 0 ? (team1WinPct / maxWinPct * 100) : 50 
    }
  ]
}

// Helper functions for calculations
function calculateBattingAverage(matches, teamId) {
  let totalRuns = 0
  let totalWickets = 0
  
  matches.forEach(match => {
    if (match.matchInfo.team1.teamId === teamId && match.matchScore.team1Score.inngs1) {
      totalRuns += match.matchScore.team1Score.inngs1.runs || 0
      totalWickets += match.matchScore.team1Score.inngs1.wickets || 0
    } else if (match.matchInfo.team2.teamId === teamId && match.matchScore.team2Score.inngs1) {
      totalRuns += match.matchScore.team2Score.inngs1.runs || 0
      totalWickets += match.matchScore.team2Score.inngs1.wickets || 0
    }
  })
  
  return totalWickets > 0 ? totalRuns / totalWickets : 0
}

function calculateBowlingAverage(matches, teamId) {
  let totalRuns = 0
  let totalWickets = 0
  
  matches.forEach(match => {
    if (match.matchInfo.team1.teamId === teamId && match.matchScore.team2Score.inngs1) {
      totalRuns += match.matchScore.team2Score.inngs1.runs || 0
      totalWickets += match.matchScore.team2Score.inngs1.wickets || 0
    } else if (match.matchInfo.team2.teamId === teamId && match.matchScore.team1Score.inngs1) {
      totalRuns += match.matchScore.team1Score.inngs1.runs || 0
      totalWickets += match.matchScore.team1Score.inngs1.wickets || 0
    }
  })
  
  return totalWickets > 0 ? totalRuns / totalWickets : 0
}

function calculateRunRate(matches, teamId) {
  let totalRuns = 0
  let totalOvers = 0
  
  matches.forEach(match => {
    if (match.matchInfo.team1.teamId === teamId && match.matchScore.team1Score.inngs1) {
      totalRuns += match.matchScore.team1Score.inngs1.runs || 0
      totalOvers += match.matchScore.team1Score.inngs1.overs || 0
    } else if (match.matchInfo.team2.teamId === teamId && match.matchScore.team2Score.inngs1) {
      totalRuns += match.matchScore.team2Score.inngs1.runs || 0
      totalOvers += match.matchScore.team2Score.inngs1.overs || 0
    }
  })
  
  return totalOvers > 0 ? totalRuns / totalOvers : 0
}

function calculateWinPercentage(matches, teamId, teamName) {
  const wins = matches.filter(match => 
    match.matchInfo.status.includes(teamName)
  ).length
  
  return matches.length > 0 ? (wins / matches.length * 100) : 0
}

// Get recent matches between selected teams
const calculateRecentMatches = async () => {
  if (selectedTeams.value.length < 2) {
    recentMatchesData.value = []
    return
  }
  
  const team1Id = selectedTeams.value[0].teamId
  const team2Id = selectedTeams.value[1].teamId
  
  if (!team1Id || !team2Id) {
    recentMatchesData.value = []
    return
  }
  
  // Fetch data for both teams
  const team1Results = await fetchTeamResults(team1Id)
  const team2Results = await fetchTeamResults(team2Id)
  
  if (!team1Results || !team2Results) {
    recentMatchesData.value = []
    return
  }
  
  // Find all matches between these two teams
  const headToHeadMatches = team1Results.teamMatchesData.flatMap(series => 
    series.matchDetailsMap.match.filter(match => 
      (match.matchInfo.team1.teamId === team1Id && match.matchInfo.team2.teamId === team2Id) ||
      (match.matchInfo.team1.teamId === team2Id && match.matchInfo.team2.teamId === team1Id)
    )
  )
  
  // Sort by date (newest first) and take the most recent 5
  recentMatchesData.value = headToHeadMatches
    .sort((a, b) => parseInt(b.matchInfo.startDate) - parseInt(a.matchInfo.startDate))
    .slice(0, 5)
    .map(match => ({
      matchId: match.matchInfo.matchId,
      startDate: match.matchInfo.startDate,
      status: match.matchInfo.status,
      team1: {
        name: match.matchInfo.team1.teamName,
        shortName: match.matchInfo.team1.teamSName,
        imageId: match.matchInfo.team1.imageId
      },
      team2: {
        name: match.matchInfo.team2.teamName,
        shortName: match.matchInfo.team2.teamSName,
        imageId: match.matchInfo.team2.imageId
      },
      score1: match.matchScore.team1Score.inngs1 ? 
        `${match.matchScore.team1Score.inngs1.runs}/${match.matchScore.team1Score.inngs1.wickets}` : '',
      score2: match.matchScore.team2Score.inngs1 ? 
        `${match.matchScore.team2Score.inngs1.runs}/${match.matchScore.team2Score.inngs1.wickets}` : ''
    }))
}

// Computed properties for template
const headToHeadStats = computed(() => headToHeadStatsData.value)
const performanceMetrics = computed(() => performanceMetricsData.value)
const recentMatches = computed(() => recentMatchesData.value)

// Add team to comparison
const addTeam = async (team) => {
  if (selectedTeams.value.length < 3 && !selectedTeams.value.find(t => t.teamId === team.teamId)) {
    // Create a team object with the necessary properties
    const teamObj = {
      id: team.teamId,
      teamId: team.teamId,
      name: team.teamName,
      shortName: team.teamSName,
      imageId: team.imageId
    }
    
    // Fetch team data before adding
    await fetchTeamResults(team.teamId)
    await fetchTeamPlayers(team.teamId)
    
    selectedTeams.value.push(teamObj)
    showTeamSelector.value = false
    
    // Calculate stats for the new team
    await calculateTeamStats(team.teamId)
    
    // If we have 2 teams, calculate comparison stats
    if (selectedTeams.value.length === 2) {
      await calculateHeadToHeadStats()
      await calculatePerformanceMetrics()
      await calculateRecentMatches()
    }
  }
}

// Remove team from comparison
const removeTeam = (teamId) => {
  selectedTeams.value = selectedTeams.value.filter(team => team.teamId !== teamId)
  
  // Recalculate stats if we still have teams
  if (selectedTeams.value.length > 0) {
    calculateTeamStats(selectedTeams.value[0].teamId)
  }
  
  if (selectedTeams.value.length >= 2) {
    calculateHeadToHeadStats()
    calculatePerformanceMetrics()
    calculateRecentMatches()
  } else {
    // Clear comparison data if we don't have enough teams
    headToHeadStatsData.value = []
    performanceMetricsData.value = []
    recentMatchesData.value = []
  }
}

// Watch for changes in selected teams
watch(selectedTeams, async (newTeams) => {
  if (newTeams.length >= 2) {
    await calculateHeadToHeadStats()
    await calculatePerformanceMetrics()
    await calculateRecentMatches()
  }
}, { deep: true })

const formatDate = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(parseInt(timestamp))
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}
</script>

<style scoped>
.backdrop-blur-sm {
  backdrop-filter: blur(8px);
}
</style> 