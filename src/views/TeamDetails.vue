<!-- TeamDetails.vue -->
<template>
  <div class="p-6 h-screen flex flex-col">
    <!-- Header Section with Team Info -->
    <div class="sticky top-0 z-10 bg-dark-800/95 backdrop-blur-sm">
      <div class="flex items-center justify-between p-4">
        <!-- Team Logo and Name -->
        <div class="flex items-center space-x-4">
          <div class="relative w-12 h-12">
            <div class="absolute inset-0 bg-primary-500/20 rounded-full blur-md"></div>
            <div class="relative w-full h-full rounded-full overflow-hidden border-2 border-dark-600">
              <img
                :src="`https://static.cricbuzz.com/a/img/v1/i1/c${teamInfo.imageId}/i.jpg?p=thumb`"
                :alt="teamInfo.teamName"
                class="w-full h-full object-cover"
              >
            </div>
          </div>
          
          <!-- Team Info -->
          <div>
            <h1 class="text-2xl font-bold bg-gradient-to-r from-primary-400 via-accent-400 to-primary-400 bg-clip-text text-transparent animate-gradient">
              {{ teamInfo.teamName }}
            </h1>
            <p class="text-gray-400 text-sm">{{ teamInfo.teamSName }}</p>
          </div>
        </div>

        <!-- Tabs Navigation in Header -->
        <div class="flex space-x-1">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            class="group relative px-4 py-2 text-sm font-medium rounded-lg transition-all duration-300"
            :class="[
              activeTab === tab.id
                ? 'bg-primary-500/10 text-primary-400'
                : 'text-gray-400 hover:bg-dark-700 hover:text-primary-400'
            ]"
          >
            <!-- Content -->
            <div class="relative flex items-center space-x-2">
              <span class="material-icons-outlined text-base">{{ tab.icon }}</span>
              <span>{{ tab.name }}</span>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Tab Content -->
    <div class="h-[calc(100vh-76px)] overflow-hidden">
      <div class="h-full overflow-y-auto custom-scrollbar">
        <!-- Results Tab -->
        <div v-if="activeTab === 'results'" class="space-y-4 px-4 py-3">
          <!-- Filters Section - Condensed -->
          <div class="bg-dark-800/70 rounded-lg p-3">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-3">
              <div class="flex items-center space-x-3">
                <span class="material-icons-outlined text-primary-400">filter_list</span>
                <div>
                  <h3 class="text-white text-sm">Results</h3>
                  <p class="text-gray-400 text-xs">{{ processedTeamResults.length }} matches</p>
                </div>
              </div>
              
              <!-- Filter by Series -->
              <div>
                <select v-model="resultsFilters.series" class="w-full bg-dark-700 text-white border border-dark-600 rounded px-3 py-1.5 text-sm focus:border-primary-500 focus:outline-none">
                  <option value="">All Series</option>
                  <option v-for="series in availableSeries" :key="series" :value="series">{{ series }}</option>
                </select>
              </div>
              
              <!-- Filter by Year -->
              <div>
                <select v-model="resultsFilters.year" class="w-full bg-dark-700 text-white border border-dark-600 rounded px-3 py-1.5 text-sm focus:border-primary-500 focus:outline-none">
                  <option value="">All Years</option>
                  <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
                </select>
              </div>
              
              <!-- Sort Order -->
              <div>
                <select v-model="resultsFilters.sort" class="w-full bg-dark-700 text-white border border-dark-600 rounded px-3 py-1.5 text-sm focus:border-primary-500 focus:outline-none">
                  <option value="newest">Newest First</option>
                  <option value="oldest">Oldest First</option>
                </select>
              </div>
            </div>
          </div>
          
          <!-- Group matches by series -->
          <div v-for="(matches, series) in groupedResults" :key="series" class="mb-6">
            <div class="flex items-center space-x-3 mb-3 px-2">
              <div class="w-1 h-5 bg-gradient-to-b from-primary-500 to-accent-500 rounded-full"></div>
              <h3 class="text-white text-base font-medium">{{ series }}</h3>
            </div>
            
            <!-- Matches in this series -->
            <div class="space-y-3">
              <div v-for="match in matches" :key="match.id"
                   class="group bg-dark-700/50 rounded-lg border border-dark-600 overflow-hidden transition-all duration-300 hover:border-primary-500/50 hover:bg-dark-700/70">
                <div class="px-4 py-3">
                  <!-- Match Header with Date -->
                  <div class="flex justify-between items-center mb-3">
                    <div class="text-xs text-gray-400">
                      <span class="inline-flex items-center">
                        <span class="material-icons-outlined text-xs mr-1">event</span>
                        {{ formatDate(match.date) }}
                      </span>
                    </div>
                    <div class="px-2 py-0.5 rounded-full text-xs font-medium bg-dark-600 text-white">
                      {{ match.matchDesc }}
                    </div>
                  </div>
                  
                  <!-- Teams and Score -->
                  <div class="flex items-center gap-2 mb-3">
                    <!-- Team 1 -->
                    <div class="flex-1 flex items-center">
                      <div class="relative w-10 h-10 mr-2">
                        <div class="absolute inset-0 bg-primary-500/20 rounded-full blur-md"></div>
                        <img 
                          :src="`https://static.cricbuzz.com/a/img/v1/i1/c${match.team1.imageId}/i.jpg?p=thumb`"
                          :alt="match.team1.teamName"
                          class="relative w-full h-full rounded-full border border-dark-600 object-cover"
                        >
                      </div>
                      <div>
                        <div class="text-white text-sm font-medium">{{ match.team1.teamName }}</div>
                        <div class="text-primary-400 text-xs mt-0.5 font-bold" v-if="match.score?.team1?.inngs1">
                          {{ match.score.team1.inngs1.runs }}/{{ match.score.team1.inngs1.wickets }}
                          <span class="text-gray-400 font-normal">({{ match.score.team1.inngs1.overs }} ov)</span>
                        </div>
                      </div>
                    </div>
                    
                    <!-- vs -->
                    <div class="w-8 text-center text-gray-500 text-xs font-medium">VS</div>
                    
                    <!-- Team 2 -->
                    <div class="flex-1 flex items-center">
                      <div class="relative w-10 h-10 mr-2">
                        <div class="absolute inset-0 bg-accent-500/20 rounded-full blur-md"></div>
                        <img 
                          :src="`https://static.cricbuzz.com/a/img/v1/i1/c${match.team2.imageId}/i.jpg?p=thumb`"
                          :alt="match.team2.teamName"
                          class="relative w-full h-full rounded-full border border-dark-600 object-cover"
                        >
                      </div>
                      <div>
                        <div class="text-white text-sm font-medium">{{ match.team2.teamName }}</div>
                        <div class="text-accent-400 text-xs mt-0.5 font-bold" v-if="match.score?.team2?.inngs1">
                          {{ match.score.team2.inngs1.runs }}/{{ match.score.team2.inngs1.wickets }}
                          <span class="text-gray-400 font-normal">({{ match.score.team2.inngs1.overs }} ov)</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Match Details -->
                  <div class="flex justify-between items-center text-xs mb-3">
                    <div class="flex items-center text-gray-300">
                      <span class="material-icons-outlined text-xs mr-1">location_on</span>
                      {{ match.venue }}
                    </div>
                    <div class="flex items-center text-gray-300">
                      <span class="material-icons-outlined text-xs mr-1">sports_cricket</span>
                      {{ match.format }}
                    </div>
                  </div>
                  
                  <!-- Result -->
                  <div class="rounded bg-dark-800 p-2 border-l-2" 
                       :class="match.status.toLowerCase().includes('won') ? 'border-green-500' : 'border-gray-600'">
                    <div class="text-accent-400 text-xs">{{ match.status }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- No matches found -->
          <div v-if="Object.keys(groupedResults).length === 0" class="flex flex-col items-center justify-center py-12">
            <span class="material-icons-outlined text-4xl text-gray-600">search_off</span>
            <p class="text-gray-400 mt-3 text-sm">No matches found with current filters</p>
            <button @click="resetResultsFilters" class="mt-3 px-3 py-1.5 bg-primary-500/20 text-primary-400 rounded-lg text-xs hover:bg-primary-500/30 transition-colors">
              Reset Filters
            </button>
          </div>
        </div>

        <!-- Schedule Tab -->
        <div v-if="activeTab === 'schedule'" class="space-y-4 px-4 py-3">
          <!-- Filters Row -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
            <!-- Monthly Calendar View -->
            <div class="md:col-span-2 bg-dark-800/50 rounded-lg p-3">
              <h4 class="text-white text-xs font-medium mb-2">Match Calendar</h4>
              <div class="overflow-x-auto">
                <div class="flex space-x-2 pb-1">
                  <div v-for="month in upcomingMonths" :key="month.id" 
                       class="min-w-[100px] cursor-pointer rounded-lg p-2 transition-colors"
                       :class="selectedMonth === month.id ? 'bg-dark-700 border border-dark-600' : 'hover:bg-dark-700/50'"
                       @click="selectedMonth = month.id">
                    <div class="text-center">
                      <div class="text-xs text-gray-400">{{ month.year }}</div>
                      <div class="text-white text-sm font-medium">{{ month.name }}</div>
                      <div class="mt-1 text-xs px-2 py-0.5 rounded-full inline-block"
                           :class="getMonthMatchCount(month.id) > 0 ? 'bg-primary-500/20 text-primary-400' : 'bg-dark-600 text-gray-400'">
                        {{ getMonthMatchCount(month.id) }} matches
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Filters Panel -->
            <div class="bg-dark-800/50 rounded-lg p-3 space-y-2">
              <div class="flex items-center justify-between mb-1">
                <h4 class="text-white text-xs font-medium">Filters</h4>
                <span class="text-gray-400 text-xs">{{ filteredSchedule.length }} matches</span>
              </div>
              <!-- Venue Filter -->
              <select v-model="scheduleFilters.venue" class="w-full bg-dark-700 text-white border border-dark-600 rounded px-3 py-1.5 text-xs focus:border-primary-500 focus:outline-none">
                <option value="">All Venues</option>
                <option v-for="venue in availableVenues" :key="venue" :value="venue">{{ venue }}</option>
              </select>
              
              <!-- Sort Order -->
              <select v-model="scheduleFilters.sort" class="w-full bg-dark-700 text-white border border-dark-600 rounded px-3 py-1.5 text-xs focus:border-primary-500 focus:outline-none">
                <option value="soonest">Soonest First</option>
                <option value="latest">Latest First</option>
              </select>
              
              <!-- Reset Button -->
              <button @click="resetScheduleFilters" class="w-full mt-1 px-3 py-1.5 bg-accent-500/10 text-accent-400 rounded text-xs hover:bg-accent-500/20 transition-colors">
                Reset Filters
              </button>
            </div>
          </div>
          
          <!-- Scheduled Matches -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div v-for="match in filteredSchedule" :key="match.id"
                 class="group bg-dark-700/50 rounded-lg border border-dark-600 overflow-hidden transition-all duration-300 hover:border-primary-500/50 hover:bg-dark-700/70">
              <div class="p-3">
                <!-- Match Date Header -->
                <div class="flex justify-between items-center mb-3">
                  <div class="flex items-center">
                    <div class="bg-dark-600 rounded p-1.5 text-center min-w-[40px]">
                      <div class="text-accent-400 text-sm font-bold">{{ formatDateDay(match.date) }}</div>
                      <div class="text-gray-400 text-xs">{{ formatDateMonth(match.date) }}</div>
                    </div>
                    <div class="ml-2">
                      <div class="text-white text-xs font-medium">{{ formatDateWeekday(match.date) }}</div>
                      <div class="text-gray-400 text-xs">{{ formatDateTime(match.date) }}</div>
                    </div>
                  </div>
                  <div class="px-2 py-0.5 rounded-full text-xs bg-dark-600 text-white">
                    {{ match.matchDesc }}
                  </div>
                </div>
                
                <!-- Teams -->
                <div class="flex items-center mb-3">
                  <!-- Team 1 -->
                  <div class="flex-1 flex items-center justify-end text-right">
                    <div class="mr-2">
                      <div class="text-white text-xs font-medium">{{ match.team1.teamName }}</div>
                      <div class="text-gray-400 text-xs">{{ match.team1.teamSName }}</div>
                    </div>
                    <div class="relative w-8 h-8">
                      <div class="absolute inset-0 bg-primary-500/20 rounded-full blur-sm"></div>
                      <img 
                        :src="`https://static.cricbuzz.com/a/img/v1/i1/c${match.team1.imageId}/i.jpg?p=thumb`"
                        :alt="match.team1.teamName"
                        class="relative w-full h-full rounded-full border border-dark-600 object-cover"
                      >
                    </div>
                  </div>
                  
                  <!-- VS -->
                  <div class="mx-2">
                    <div class="rounded-full w-6 h-6 flex items-center justify-center bg-dark-600">
                      <span class="text-gray-400 text-[10px]">VS</span>
                    </div>
                  </div>
                  
                  <!-- Team 2 -->
                  <div class="flex-1 flex items-center">
                    <div class="relative w-8 h-8">
                      <div class="absolute inset-0 bg-accent-500/20 rounded-full blur-sm"></div>
                      <img 
                        :src="`https://static.cricbuzz.com/a/img/v1/i1/c${match.team2.imageId}/i.jpg?p=thumb`"
                        :alt="match.team2.teamName"
                        class="relative w-full h-full rounded-full border border-dark-600 object-cover"
                      >
                    </div>
                    <div class="ml-2">
                      <div class="text-white text-xs font-medium">{{ match.team2.teamName }}</div>
                      <div class="text-gray-400 text-xs">{{ match.team2.teamSName }}</div>
                    </div>
                  </div>
                </div>
                
                <!-- Match Details -->
                <div class="rounded bg-dark-800/70 p-2 flex justify-between items-center text-xs">
                  <div class="flex items-center">
                    <span class="material-icons-outlined text-accent-400 text-xs mr-1">location_on</span>
                    <div class="text-white">{{ match.venue }}</div>
                  </div>
                  
                  <div class="px-2 py-0.5 bg-accent-500/10 text-accent-400 rounded text-xs">
                    {{ match.status }}
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- No matches found -->
          <div v-if="filteredSchedule.length === 0" class="flex flex-col items-center justify-center py-12">
            <span class="material-icons-outlined text-4xl text-gray-600">event_busy</span>
            <p class="text-gray-400 mt-3 text-sm">No upcoming matches found</p>
            <button @click="resetScheduleFilters" class="mt-3 px-3 py-1.5 bg-accent-500/20 text-accent-400 rounded-lg text-xs hover:bg-accent-500/30 transition-colors">
              Reset Filters
            </button>
          </div>
        </div>

        <!-- Players Tab -->
        <div v-if="activeTab === 'players'" class="px-4 py-3">
          <!-- Player Search and Filter -->
          <div class="flex flex-wrap items-center gap-3 mb-4">      
            <!-- Search -->
            <div class="relative flex-1 min-w-[200px]">
              <span class="absolute left-3 top-1.5 text-gray-400 material-icons-outlined text-xs">search</span>
              <input v-model="playerFilters.search" 
                     type="text" 
                     placeholder="Search by name or style..." 
                     class="w-full bg-dark-700 text-white border border-dark-600 rounded-full px-8 py-1.5 text-xs focus:border-primary-500 focus:outline-none">
              <button v-if="playerFilters.search"
                      @click="playerFilters.search = ''" 
                      class="absolute right-3 top-1.5 text-gray-400 material-icons-outlined text-xs hover:text-gray-300">
                close
              </button>
            </div>
            
            <!-- Category Filter -->
            <div class="min-w-[120px]">
              <select v-model="playerFilters.category" class="w-full bg-dark-700 text-white border border-dark-600 rounded-full px-3 py-1.5 text-xs focus:border-primary-500 focus:outline-none">
                <option value="">All Roles</option>
                <option value="BATSMEN">Batsmen</option>
                <option value="ALL ROUNDER">All-Rounders</option>
                <option value="WICKET KEEPER">Wicket Keepers</option>
                <option value="BOWLER">Bowlers</option>
              </select>
            </div>
            
            <!-- View Selector -->
            <div class="flex">
              <button @click="playerView = 'grid'" 
                      class="px-2 py-1.5 rounded-l-lg text-xs flex items-center"
                      :class="playerView === 'grid' ? 'bg-primary-500/20 text-primary-400' : 'bg-dark-800 text-gray-400 hover:bg-dark-700'">
                <span class="material-icons-outlined text-xs">grid_view</span>
              </button>
              <button @click="playerView = 'detailed'" 
                      class="px-2 py-1.5 rounded-r-lg text-xs flex items-center"
                      :class="playerView === 'detailed' ? 'bg-primary-500/20 text-primary-400' : 'bg-dark-800 text-gray-400 hover:bg-dark-700'">
                <span class="material-icons-outlined text-xs">view_list</span>
              </button>
            </div>
            
            <!-- Total count -->
            <div class="ml-auto text-right">
              <span class="text-xs text-gray-400">{{ totalPlayers }} players</span>
            </div>
          </div>
          
          <!-- Categories with Players -->
          <div v-if="filteredPlayerCategories.length">
            <div v-for="(category, index) in filteredPlayerCategories" :key="index" class="mb-6">
              <!-- Category Header -->
              <div class="flex items-center mb-3">
                <div class="flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center" 
                     :class="getCategoryColor(category.name)">
                  <span class="material-icons-outlined text-xs">{{ getCategoryIcon(category.name) }}</span>
                </div>
                <div class="ml-2">
                  <div class="flex items-center">
                    <h3 class="text-white text-sm font-bold">{{ getCategoryLabel(category.name) }}</h3>
                    <span class="ml-2 text-xs text-gray-400">{{ category.players.length }} players</span>
                  </div>
                </div>
              </div>
              
              <!-- Grid View -->
              <div v-if="playerView === 'grid'" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
                <div v-for="player in category.players" :key="player.id"
                     class="group bg-dark-700/50 rounded-lg border border-dark-600 overflow-hidden transition-all duration-300 hover:border-primary-500/50 hover:bg-dark-700/70">
                  <div class="p-3">
                    <div class="flex flex-col items-center text-center">
                      <div class="relative mb-2">
                        <div class="absolute inset-0 bg-primary-500/20 rounded-full blur-md"></div>
                        <img :src="`https://static.cricbuzz.com/a/img/v1/i1/c${player.imageId}/i.jpg?p=thumb`"
                             :alt="player.name"
                             class="relative w-14 h-14 rounded-full border-2 border-dark-600 object-cover">
                      </div>
                      <h4 class="text-white text-xs font-medium">{{ player.name }}</h4>
                      <div class="mt-1 space-y-1">
                        <p v-if="player.battingStyle" class="text-xs text-gray-400 flex items-center justify-center">
                          <span class="material-icons-outlined text-[10px] mr-1">sports_cricket</span>
                          {{ player.battingStyle }}
                        </p>
                        <p v-if="player.bowlingStyle" class="text-xs text-gray-400 flex items-center justify-center">
                          <span class="material-icons-outlined text-[10px] mr-1">fitness_center</span>
                          {{ player.bowlingStyle }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Detailed View -->
              <div v-else class="space-y-3">
                <div v-for="player in category.players" :key="player.id"
                     class="bg-dark-700/50 rounded-lg border border-dark-600 overflow-hidden transition-all duration-300 hover:border-primary-500/50 group">
                  <div class="p-3">
                    <div class="flex items-start space-x-3">
                      <!-- Player Image -->
                      <div class="relative">
                        <div class="absolute inset-0 bg-primary-500/20 rounded-full blur-lg"></div>
                        <img :src="`https://static.cricbuzz.com/a/img/v1/i1/c${player.imageId}/i.jpg?p=thumb`"
                             :alt="player.name"
                             class="relative w-12 h-12 rounded-full border-2 border-dark-600 object-cover">
                      </div>
                      
                      <!-- Player Details -->
                      <div class="flex-1">
                        <div class="flex items-center flex-wrap">
                          <h3 class="text-white text-sm font-bold">{{ player.name }}</h3>
                          <div class="ml-auto flex space-x-1">
                            <span class="px-2 py-0.5 text-[10px] rounded-full bg-accent-500/10 text-accent-400">
                              {{ getCategoryLabel(category.name) }}
                            </span>
                            <span v-if="player.id" class="px-2 py-0.5 text-[10px] rounded-full bg-dark-600 text-gray-300">
                              ID: {{ player.id }}
                            </span>
                          </div>
                        </div>
                        
                        <!-- Playing Styles -->
                        <div class="mt-2 grid grid-cols-1 md:grid-cols-2 gap-2">
                          <div v-if="player.battingStyle" class="bg-dark-800/50 p-2 rounded text-xs">
                            <div class="text-gray-400 text-[10px]">Batting Style</div>
                            <div class="text-white flex items-center">
                              <span class="material-icons-outlined text-primary-400 text-xs mr-1">sports_cricket</span>
                              {{ player.battingStyle }}
                            </div>
                          </div>
                          
                          <div v-if="player.bowlingStyle" class="bg-dark-800/50 p-2 rounded text-xs">
                            <div class="text-gray-400 text-[10px]">Bowling Style</div>
                            <div class="text-white flex items-center">
                              <span class="material-icons-outlined text-accent-400 text-xs mr-1">fitness_center</span>
                              {{ player.bowlingStyle }}
                            </div>
                          </div>
                        </div>
                        
                        <!-- Additional stats (placeholder) -->
                        <div class="mt-2 flex space-x-2 text-center">
                          <div class="bg-dark-800/70 rounded px-2 py-1 text-xs flex-1">
                            <div class="text-primary-400 font-bold">120+</div>
                            <div class="text-gray-400 text-[10px]">Matches</div>
                          </div>
                          <div class="bg-dark-800/70 rounded px-2 py-1 text-xs flex-1">
                            <div class="text-accent-400 font-bold">3500+</div>
                            <div class="text-gray-400 text-[10px]">Runs</div>
                          </div>
                          <div class="bg-dark-800/70 rounded px-2 py-1 text-xs flex-1">
                            <div class="text-green-400 font-bold">30+</div>
                            <div class="text-gray-400 text-[10px]">Wickets</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- No players found -->
          <div v-else class="flex flex-col items-center justify-center py-12">
            <span class="material-icons-outlined text-4xl text-gray-600">person_off</span>
            <p class="text-gray-400 mt-3 text-sm">No players found matching the criteria</p>
            <button @click="resetPlayerFilters" class="mt-3 px-3 py-1.5 bg-primary-500/20 text-primary-400 rounded-lg text-xs hover:bg-primary-500/30 transition-colors">
              Reset Filters
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

// Import JSON data
import teamPlayers from '../sample-responses/team-responses/team-players.json'
import teamResultsData from '../sample-responses/team-responses/team-result.json'
import teamSchedule from '../sample-responses/team-responses/team-schedule.json'

const route = useRoute()
const activeTab = ref('results')

// Sample team info - In real app, this would come from API
const teamInfo = {
  teamId: 58,
  teamName: "Chennai Super Kings",
  teamSName: "CSK",
  imageId: 225641
}

const tabs = [
  { id: 'results', name: 'Results', icon: 'emoji_events' },
  { id: 'schedule', name: 'Schedule', icon: 'calendar_today' },
  { id: 'players', name: 'Players', icon: 'group' }
]

// Results filters
const resultsFilters = ref({
  series: '',
  year: '',
  sort: 'newest'
})

const resetResultsFilters = () => {
  resultsFilters.value = {
    series: '',
    year: '',
    sort: 'newest'
  }
}

// Format date helper
const formatDate = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(parseInt(timestamp))
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Get year from timestamp
const getYear = (timestamp) => {
  if (!timestamp) return ''
  return new Date(parseInt(timestamp)).getFullYear().toString()
}

// Process team results
const processedTeamResults = computed(() => {
  const allMatches = []
  if (!teamResultsData?.teamMatchesData) return allMatches
  
  teamResultsData.teamMatchesData.forEach(series => {
    if (!series?.matchDetailsMap?.match) return
    const seriesName = series.matchDetailsMap.key || ''
    
    series.matchDetailsMap.match.forEach(match => {
      if (!match?.matchInfo) return
      allMatches.push({
        id: match.matchInfo.matchId,
        date: match.matchInfo.startDate,
        matchDesc: match.matchInfo.matchDesc,
        format: match.matchInfo.matchFormat,
        seriesId: match.matchInfo.seriesId,
        seriesName: seriesName,
        teams: `${match.matchInfo.team1?.teamSName || ''} vs ${match.matchInfo.team2?.teamSName || ''}`,
        venue: match.matchInfo.venueInfo?.ground || '',
        city: match.matchInfo.venueInfo?.city || '',
        status: match.matchInfo.status || '',
        state: match.matchInfo.state || '',
        result: match.matchInfo.result || '',
        team1: match.matchInfo.team1 || {},
        team2: match.matchInfo.team2 || {},
        score: match.matchScore || {}
      })
    })
  })
  
  return allMatches
})

// Available filters
const availableSeries = computed(() => {
  const series = new Set()
  processedTeamResults.value.forEach(match => {
    if (match.seriesName) series.add(match.seriesName)
  })
  return Array.from(series)
})

const availableYears = computed(() => {
  const years = new Set()
  processedTeamResults.value.forEach(match => {
    if (match.date) {
      const year = getYear(match.date)
      if (year) years.add(year)
    }
  })
  return Array.from(years).sort().reverse()
})

// Filtered and sorted results
const filteredResults = computed(() => {
  let results = [...processedTeamResults.value]
  
  // Apply series filter
  if (resultsFilters.value.series) {
    results = results.filter(match => match.seriesName === resultsFilters.value.series)
  }
  
  // Apply year filter
  if (resultsFilters.value.year) {
    results = results.filter(match => getYear(match.date) === resultsFilters.value.year)
  }
  
  // Apply sorting
  results.sort((a, b) => {
    const dateA = a.date ? parseInt(a.date) : 0
    const dateB = b.date ? parseInt(b.date) : 0
    
    if (resultsFilters.value.sort === 'newest') {
      return dateB - dateA
    } else {
      return dateA - dateB
    }
  })
  
  return results
})

// Group results by series
const groupedResults = computed(() => {
  const groups = {}
  
  filteredResults.value.forEach(match => {
    const seriesName = match.seriesName || 'Other Matches'
    if (!groups[seriesName]) {
      groups[seriesName] = []
    }
    groups[seriesName].push(match)
  })
  
  return groups
})

// Schedule filters
const scheduleFilters = ref({
  venue: '',
  sort: 'soonest'
})

const selectedMonth = ref('')

const resetScheduleFilters = () => {
  scheduleFilters.value = {
    venue: '',
    sort: 'soonest'
  }
  selectedMonth.value = upcomingMonths.value[0]?.id || ''
}

// Additional date format helpers
const formatDateDay = (timestamp) => {
  if (!timestamp) return ''
  return new Date(parseInt(timestamp)).getDate()
}

const formatDateMonth = (timestamp) => {
  if (!timestamp) return ''
  return new Date(parseInt(timestamp)).toLocaleDateString('en-US', { month: 'short' })
}

const formatDateWeekday = (timestamp) => {
  if (!timestamp) return ''
  return new Date(parseInt(timestamp)).toLocaleDateString('en-US', { weekday: 'long' })
}

const formatDateTime = (timestamp) => {
  if (!timestamp) return ''
  return new Date(parseInt(timestamp)).toLocaleTimeString('en-US', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: true
  })
}

// Get month and year from timestamp
const getMonthYear = (timestamp) => {
  if (!timestamp) return { month: '', year: '' }
  const date = new Date(parseInt(timestamp))
  return {
    month: date.getMonth(),
    year: date.getFullYear(),
    monthName: date.toLocaleDateString('en-US', { month: 'long' })
  }
}

// Process team schedule
const processedTeamSchedule = computed(() => {
  const allMatches = []
  if (!teamSchedule?.teamMatchesData) return allMatches
  
  teamSchedule.teamMatchesData.forEach(series => {
    if (!series?.matchDetailsMap?.match) return
    const seriesName = series.matchDetailsMap.key || ''
    
    series.matchDetailsMap.match.forEach(match => {
      if (!match?.matchInfo) return
      allMatches.push({
        id: match.matchInfo.matchId,
        date: match.matchInfo.startDate,
        matchDesc: match.matchInfo.matchDesc,
        format: match.matchInfo.matchFormat || 'T20',
        seriesId: match.matchInfo.seriesId,
        seriesName: seriesName,
        teams: `${match.matchInfo.team1?.teamSName || ''} vs ${match.matchInfo.team2?.teamSName || ''}`,
        venue: match.matchInfo.venueInfo?.ground || '',
        city: match.matchInfo.venueInfo?.city || '',
        status: match.matchInfo.status || '',
        state: match.matchInfo.state || '',
        team1: match.matchInfo.team1 || {},
        team2: match.matchInfo.team2 || {}
      })
    })
  })
  
  return allMatches
})

// Generate upcoming months
const upcomingMonths = computed(() => {
  const months = []
  const monthSet = new Set()
  
  processedTeamSchedule.value.forEach(match => {
    if (match.date) {
      const { month, year, monthName } = getMonthYear(match.date)
      const monthId = `${year}-${month}`
      
      if (!monthSet.has(monthId)) {
        monthSet.add(monthId)
        months.push({
          id: monthId,
          name: monthName,
          year: year,
          month: month
        })
      }
    }
  })
  
  // Sort months chronologically
  months.sort((a, b) => {
    if (a.year !== b.year) return a.year - b.year
    return a.month - b.month
  })
  
  // Set default selected month to the first available one
  if (months.length > 0 && !selectedMonth.value) {
    selectedMonth.value = months[0].id
  }
  
  return months
})

// Count matches per month
const getMonthMatchCount = (monthId) => {
  if (!monthId) return 0
  
  return processedTeamSchedule.value.filter(match => {
    if (!match.date) return false
    const { month, year } = getMonthYear(match.date)
    return `${year}-${month}` === monthId
  }).length
}

// Available venues
const availableVenues = computed(() => {
  const venues = new Set()
  processedTeamSchedule.value.forEach(match => {
    if (match.venue) venues.add(match.venue)
  })
  return Array.from(venues).sort()
})

// Filtered schedule
const filteredSchedule = computed(() => {
  let schedule = [...processedTeamSchedule.value]
  
  // Filter by venue
  if (scheduleFilters.value.venue) {
    schedule = schedule.filter(match => match.venue === scheduleFilters.value.venue)
  }
  
  // Filter by selected month
  if (selectedMonth.value) {
    schedule = schedule.filter(match => {
      if (!match.date) return false
      const { month, year } = getMonthYear(match.date)
      return `${year}-${month}` === selectedMonth.value
    })
  }
  
  // Apply sorting
  schedule.sort((a, b) => {
    const dateA = a.date ? parseInt(a.date) : 0
    const dateB = b.date ? parseInt(b.date) : 0
    
    if (scheduleFilters.value.sort === 'soonest') {
      return dateA - dateB
    } else {
      return dateB - dateA
    }
  })
  
  return schedule
})

// Player view and filters
const playerView = ref('grid')
const playerFilters = ref({
  search: '',
  category: ''
})

const resetPlayerFilters = () => {
  playerFilters.value = {
    search: '',
    category: ''
  }
}

// Process players by category
const playerCategories = computed(() => {
  const categories = {
    'BATSMEN': [],
    'ALL ROUNDER': [],
    'WICKET KEEPER': [],
    'BOWLER': []
  }

  if (!teamPlayers?.player) return Object.entries(categories).map(([name, players]) => ({
    name,
    players
  }))

  let currentCategory = null
  teamPlayers.player.forEach(item => {
    if (!item.id) {
      // This is a category header
      currentCategory = item.name
    } else if (currentCategory && categories[currentCategory]) {
      // This is a player
      categories[currentCategory].push(item)
    }
  })

  return Object.entries(categories).map(([name, players]) => ({
    name,
    players
  }))
})

// Filtered player categories
const filteredPlayerCategories = computed(() => {
  let categories = [...playerCategories.value]
  
  // Filter by category
  if (playerFilters.value.category) {
    categories = categories.filter(category => 
      category.name === playerFilters.value.category
    )
  }
  
  // Filter players by search query
  if (playerFilters.value.search) {
    const searchTerm = playerFilters.value.search.toLowerCase()
    
    // Map each category, filtering its players
    categories = categories.map(category => {
      const filteredPlayers = category.players.filter(player => 
        player.name?.toLowerCase().includes(searchTerm) ||
        player.battingStyle?.toLowerCase().includes(searchTerm) || 
        player.bowlingStyle?.toLowerCase().includes(searchTerm)
      )
      
      return {
        ...category,
        players: filteredPlayers
      }
    }).filter(category => category.players.length > 0)
  }
  
  return categories
})

// Helper to get nice category label
const getCategoryLabel = (categoryName) => {
  switch(categoryName) {
    case 'BATSMEN': return 'Batsmen'
    case 'ALL ROUNDER': return 'All-Rounders'
    case 'WICKET KEEPER': return 'Wicket Keepers'
    case 'BOWLER': return 'Bowlers'
    default: return categoryName
  }
}

// Helper to get category icon
const getCategoryIcon = (categoryName) => {
  switch(categoryName) {
    case 'BATSMEN': return 'sports_cricket'
    case 'ALL ROUNDER': return 'stars'
    case 'WICKET KEEPER': return 'pan_tool'
    case 'BOWLER': return 'fitness_center'
    default: return 'person'
  }
}

// Helper to get category color
const getCategoryColor = (categoryName) => {
  switch(categoryName) {
    case 'BATSMEN': return 'bg-primary-500/20 text-primary-400'
    case 'ALL ROUNDER': return 'bg-purple-500/20 text-purple-400'
    case 'WICKET KEEPER': return 'bg-accent-500/20 text-accent-400'
    case 'BOWLER': return 'bg-green-500/20 text-green-400'
    default: return 'bg-gray-500/20 text-gray-400'
  }
}

// Total players count
const totalPlayers = computed(() => {
  return playerCategories.value.reduce((total, category) => {
    return total + category.players.length
  }, 0)
})
</script>

<style scoped>
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