<!-- PlayerDetailedViewNew.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-indigo-950 to-gray-900">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center min-h-screen">
      <div class="flex flex-col items-center space-y-4">
        <div class="w-20 h-20 border-t-4 border-b-4 border-indigo-500 rounded-full animate-spin"></div>
        <p class="text-indigo-400 font-medium">Loading player data...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="container mx-auto px-4 py-16 flex justify-center">
      <div class="bg-red-900/20 backdrop-blur-md border border-red-500/30 rounded-lg p-8 text-center shadow-xl max-w-md">
        <h3 class="text-red-400 text-2xl font-bold mb-4">Error</h3>
        <p class="text-red-300 mb-6">{{ error }}</p>
        <button @click="fetchPlayerData" 
                class="px-6 py-2 bg-indigo-600/20 hover:bg-indigo-600/30 border border-indigo-500/30 rounded-lg text-indigo-400 hover:text-indigo-300 transition-all duration-300">
          Try Again
        </button>
      </div>
    </div>

    <!-- Player Content -->
    <div v-else-if="player" class="container mx-auto px-4 py-8">
      <!-- Back Button -->
      <button @click="router.back()" 
              class="group flex items-center space-x-2 px-4 py-2 rounded-lg bg-indigo-500/10 text-indigo-400 hover:bg-indigo-500/20 mb-8 transition-all">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 group-hover:-translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        <span>Back to Players</span>
      </button>

      <!-- Hero Section -->
      <div class="bg-gradient-to-br from-indigo-900/30 to-purple-900/30 rounded-2xl overflow-hidden backdrop-blur-sm border border-indigo-500/10 shadow-xl mb-8">
        <div class="relative p-6 md:p-8 lg:p-10">
          <!-- Player Header -->
          <div class="flex flex-col md:flex-row gap-8">
            <!-- Player Image -->
            <div class="relative w-full md:w-80 h-96 md:h-auto flex-shrink-0">
              <div class="overflow-hidden rounded-xl border-2 border-indigo-500/20 h-full shadow-lg shadow-indigo-500/10 group">
                <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${player.faceImageId}/i.jpg?p=medium`"
                     :alt="player.name"
                     class="w-full h-full object-cover object-top group-hover:scale-105 transition-transform duration-700">
              </div>
              
              <!-- Player Role Tags -->
              <div class="absolute bottom-4 left-4 flex flex-wrap gap-2">
                <span class="px-3 py-1 text-xs font-medium rounded-full bg-indigo-500/80 text-white">
                  {{ player.role }}
                </span>
                <span v-if="player.bat" class="px-3 py-1 text-xs font-medium rounded-full bg-emerald-500/80 text-white">
                  {{ formatBattingStyle(player.bat) }}
                </span>
              </div>
            </div>
            
            <!-- Player Info -->
            <div class="flex flex-col justify-between flex-1">
              <div>
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                  <h1 class="text-4xl md:text-5xl font-bold text-white">{{ player.name }}</h1>
                  <div class="flex gap-3">
                    <div v-if="player.rankings && player.rankings.all && player.rankings.all.t20Rank === '1'" 
                         class="bg-gradient-to-r from-amber-500 to-yellow-300 text-black font-bold px-3 py-1 rounded-full text-sm flex items-center gap-1">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                      </svg>
                      <span>#1 T20 All-Rounder</span>
                    </div>
                  </div>
                </div>
                
                <!-- Player Info Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                  <!-- Country -->
                  <div class="bg-white/5 backdrop-blur-sm rounded-lg p-4">
                    <div class="text-indigo-400 text-sm mb-1">Country</div>
                    <div class="text-white font-medium">{{ player.intlTeam }}</div>
                  </div>
                  
                  <!-- Date of Birth -->
                  <div class="bg-white/5 backdrop-blur-sm rounded-lg p-4">
                    <div class="text-indigo-400 text-sm mb-1">Born</div>
                    <div class="text-white font-medium">{{ player.DoBFormat }}</div>
                  </div>
                  
                  <!-- Birth Place -->
                  <div class="bg-white/5 backdrop-blur-sm rounded-lg p-4">
                    <div class="text-indigo-400 text-sm mb-1">Birth Place</div>
                    <div class="text-white font-medium">{{ player.birthPlace }}</div>
                  </div>
                  
                  <!-- Bowling Style -->
                  <div class="bg-white/5 backdrop-blur-sm rounded-lg p-4">
                    <div class="text-indigo-400 text-sm mb-1">Bowling Style</div>
                    <div class="text-white font-medium">{{ player.bowl }}</div>
                  </div>
                </div>
              </div>
              
              <!-- Teams List -->
              <div class="mt-4">
                <h3 class="text-lg font-medium text-white mb-3">Teams</h3>
                <div class="flex flex-wrap gap-2">
                  <div v-for="team in player.teamNameIds" :key="team.teamId"
                       class="px-3 py-1 rounded-full text-sm font-medium"
                       :style="{
                         backgroundColor: `hsla(${getTeamHue(team.teamId)}, 70%, 60%, 0.2)`,
                         borderColor: `hsla(${getTeamHue(team.teamId)}, 70%, 60%, 0.3)`,
                         color: `hsla(${getTeamHue(team.teamId)}, 70%, 95%, 0.9)`
                       }"
                       :class="{ 'border': true }">
                    {{ team.teamName }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Statistics Tabs -->
      <div class="bg-gradient-to-br from-indigo-900/30 to-purple-900/30 rounded-2xl overflow-hidden backdrop-blur-sm border border-indigo-500/10 shadow-xl mb-8">
        <div class="border-b border-white/10">
          <div class="flex overflow-x-auto">
            <button 
              v-for="tab in tabs" 
              :key="tab.id" 
              @click="activeTab = tab.id"
              class="px-6 py-4 font-medium text-sm focus:outline-none whitespace-nowrap"
              :class="activeTab === tab.id ? 'text-white border-b-2 border-indigo-500' : 'text-indigo-300 hover:text-white'">
              {{ tab.name }}
            </button>
          </div>
        </div>
        
        <!-- Batting Stats -->
        <div v-if="activeTab === 'batting'" class="p-4 md:p-6">
          <h3 class="text-xl font-bold text-white mb-4">Batting Statistics</h3>
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white/5 backdrop-blur-sm rounded-lg p-6 border border-indigo-500/10">
              <v-chart class="w-full h-[500px]" :option="battingRadarOption" autoresize />
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left">
                <thead>
                  <tr class="border-b border-white/10">
                    <th v-for="(header, index) in battingStats.headers" :key="index" 
                        class="py-3 px-4 font-medium text-indigo-300">
                      {{ header }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, rowIndex) in battingStats.values" :key="rowIndex"
                      class="border-b border-white/5 hover:bg-white/5">
                    <td v-for="(cell, cellIndex) in row.values" :key="cellIndex"
                        class="py-3 px-4" 
                        :class="cellIndex === 0 ? 'text-indigo-300 font-medium' : 'text-white'">
                      {{ cell }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        
        <!-- Bowling Stats -->
        <div v-if="activeTab === 'bowling'" class="p-4 md:p-6">
          <h3 class="text-xl font-bold text-white mb-4">Bowling Statistics</h3>
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-indigo-500/10">
              <v-chart class="w-full h-[400px]" :option="bowlingBarOption" autoresize />
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left">
                <thead>
                  <tr class="border-b border-white/10">
                    <th v-for="(header, index) in bowlingStats.headers" :key="index" 
                        class="py-3 px-4 font-medium text-indigo-300">
                      {{ header }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, rowIndex) in bowlingStats.values" :key="rowIndex"
                      class="border-b border-white/5 hover:bg-white/5">
                    <td v-for="(cell, cellIndex) in row.values" :key="cellIndex"
                        class="py-3 px-4" 
                        :class="cellIndex === 0 ? 'text-indigo-300 font-medium' : 'text-white'">
                      {{ cell }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        
        <!-- Rankings -->
        <div v-if="activeTab === 'rankings'" class="p-4 md:p-6">
          <h3 class="text-xl font-bold text-white mb-6">ICC Rankings</h3>
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white/5 backdrop-blur-sm rounded-lg p-4 border border-indigo-500/10">
              <v-chart class="w-full h-[400px]" :option="rankingsLineOption" autoresize />
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <!-- Batting Rankings -->
              <div class="bg-white/5 backdrop-blur-sm rounded-lg p-4">
                <h4 class="text-lg font-medium text-white mb-3 flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Batting
                </h4>
                
                <div class="space-y-4">
                  <div v-if="player.rankings?.bat?.t20Rank" class="flex justify-between items-center">
                    <span class="text-indigo-300">T20I Rank</span>
                    <span class="text-white font-bold">#{{ player.rankings.bat.t20Rank }}</span>
                  </div>
                  
                  <div v-if="player.rankings?.bat?.odiRank" class="flex justify-between items-center">
                    <span class="text-indigo-300">ODI Rank</span>
                    <span class="text-white font-bold">#{{ player.rankings.bat.odiRank }}</span>
                  </div>
                  
                  <div v-if="player.rankings?.bat?.t20BestRank" class="flex justify-between items-center">
                    <span class="text-indigo-300">T20I Best</span>
                    <span class="text-white font-bold">#{{ player.rankings.bat.t20BestRank }}</span>
                  </div>
                  
                  <div v-if="player.rankings?.bat?.odiBestRank" class="flex justify-between items-center">
                    <span class="text-indigo-300">ODI Best</span>
                    <span class="text-white font-bold">#{{ player.rankings.bat.odiBestRank }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Bowling Rankings -->
              <div class="bg-white/5 backdrop-blur-sm rounded-lg p-4">
                <h4 class="text-lg font-medium text-white mb-3 flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Bowling
                </h4>
                
                <div class="space-y-4">
                  <div v-if="player.rankings?.bowl?.t20Rank" class="flex justify-between items-center">
                    <span class="text-indigo-300">T20I Rank</span>
                    <span class="text-white font-bold">#{{ player.rankings.bowl.t20Rank }}</span>
                  </div>
                  
                  <div v-if="player.rankings?.bowl?.t20BestRank" class="flex justify-between items-center">
                    <span class="text-indigo-300">T20I Best</span>
                    <span class="text-white font-bold">#{{ player.rankings.bowl.t20BestRank }}</span>
                  </div>
                  
                  <div v-if="player.rankings?.bowl?.odiBestRank" class="flex justify-between items-center">
                    <span class="text-indigo-300">ODI Best</span>
                    <span class="text-white font-bold">#{{ player.rankings.bowl.odiBestRank }}</span>
                  </div>
                </div>
              </div>
              
              <!-- All-Rounder Rankings -->
              <div class="bg-white/5 backdrop-blur-sm rounded-lg p-4">
                <h4 class="text-lg font-medium text-white mb-3 flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  All-Rounder
                </h4>
                
                <div class="space-y-4">
                  <div v-if="player.rankings?.all?.t20Rank" class="flex justify-between items-center">
                    <span class="text-indigo-300">T20I Rank</span>
                    <span class="text-white font-bold" :class="{'text-yellow-400': player.rankings.all.t20Rank === '1'}">
                      #{{ player.rankings.all.t20Rank }}
                      <span v-if="player.rankings.all.t20Rank === '1'" class="ml-1">🏆</span>
                    </span>
                  </div>
                  
                  <div v-if="player.rankings?.all?.odiRank" class="flex justify-between items-center">
                    <span class="text-indigo-300">ODI Rank</span>
                    <span class="text-white font-bold">#{{ player.rankings.all.odiRank }}</span>
                  </div>
                  
                  <div v-if="player.rankings?.all?.t20BestRank" class="flex justify-between items-center">
                    <span class="text-indigo-300">T20I Best</span>
                    <span class="text-white font-bold">#{{ player.rankings.all.t20BestRank }}</span>
                  </div>
                  
                  <div v-if="player.rankings?.all?.odiBestRank" class="flex justify-between items-center">
                    <span class="text-indigo-300">ODI Best</span>
                    <span class="text-white font-bold">#{{ player.rankings.all.odiBestRank }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Highlights -->
        <div v-if="activeTab === 'highlights'" class="p-4 md:p-6">
          <h3 class="text-xl font-bold text-white mb-6">Career Highlights</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <!-- Batting Highlights -->
            <div class="bg-gradient-to-br from-indigo-600/10 to-purple-600/10 rounded-lg p-5 border border-indigo-500/20">
              <div class="flex justify-between items-center mb-4">
                <h4 class="text-lg font-medium text-white">Batting</h4>
                <div class="text-sm px-2 py-1 bg-indigo-500/20 rounded-md text-indigo-200">Test</div>
              </div>
              <div class="flex items-baseline gap-2">
                <span class="text-3xl font-bold text-white">{{ getHighestScore() }}</span>
                <span class="text-indigo-300">Highest Score</span>
              </div>
              <div class="mt-3 text-sm text-indigo-300">
                {{ getCenturiesAndFifties() }}
              </div>
            </div>
            
            <!-- Bowling Highlights -->
            <div class="bg-gradient-to-br from-purple-600/10 to-pink-600/10 rounded-lg p-5 border border-purple-500/20">
              <div class="flex justify-between items-center mb-4">
                <h4 class="text-lg font-medium text-white">Bowling</h4>
                <div class="text-sm px-2 py-1 bg-purple-500/20 rounded-md text-purple-200">Test</div>
              </div>
              <div class="flex items-baseline gap-2">
                <span class="text-3xl font-bold text-white">{{ getBestBowling() }}</span>
                <span class="text-purple-300">Best Bowling</span>
              </div>
              <div class="mt-3 text-sm text-purple-300">
                {{ getFiveWicketHauls() }}
              </div>
            </div>
            
            <!-- T20 Highlights -->
            <div class="bg-gradient-to-br from-blue-600/10 to-indigo-600/10 rounded-lg p-5 border border-blue-500/20">
              <div class="flex justify-between items-center mb-4">
                <h4 class="text-lg font-medium text-white">T20 Impact</h4>
                <div class="text-sm px-2 py-1 bg-blue-500/20 rounded-md text-blue-200">T20I</div>
              </div>
              <div class="flex items-baseline gap-2">
                <span class="text-3xl font-bold text-white">{{ getT20StrikeRate() }}</span>
                <span class="text-blue-300">Strike Rate</span>
              </div>
              <div class="mt-3 text-sm text-blue-300">
                {{ getT20Highlights() }}
              </div>
            </div>
            
            <!-- IPL Highlights -->
            <div class="bg-gradient-to-br from-orange-600/10 to-red-600/10 rounded-lg p-5 border border-orange-500/20">
              <div class="flex justify-between items-center mb-4">
                <h4 class="text-lg font-medium text-white">IPL Career</h4>
                <div class="text-sm px-2 py-1 bg-orange-500/20 rounded-md text-orange-200">IPL</div>
              </div>
              <div class="flex items-baseline gap-2">
                <span class="text-3xl font-bold text-white">{{ getIPLStrikeRate() }}</span>
                <span class="text-orange-300">Strike Rate</span>
              </div>
              <div class="mt-3 text-sm text-orange-300">
                {{ getIPLHighlights() }}
              </div>
            </div>
            
            <!-- ODI Highlights -->
            <div class="bg-gradient-to-br from-emerald-600/10 to-teal-600/10 rounded-lg p-5 border border-emerald-500/20">
              <div class="flex justify-between items-center mb-4">
                <h4 class="text-lg font-medium text-white">ODI Impact</h4>
                <div class="text-sm px-2 py-1 bg-emerald-500/20 rounded-md text-emerald-200">ODI</div>
              </div>
              <div class="flex items-baseline gap-2">
                <span class="text-3xl font-bold text-white">{{ getODIStrikeRate() }}</span>
                <span class="text-emerald-300">Strike Rate</span>
              </div>
              <div class="mt-3 text-sm text-emerald-300">
                {{ getODIHighlights() }}
              </div>
            </div>
            
            <!-- Career Summary -->
            <div class="bg-gradient-to-br from-violet-600/10 to-indigo-600/10 rounded-lg p-5 border border-violet-500/20">
              <div class="flex justify-between items-center mb-4">
                <h4 class="text-lg font-medium text-white">Career Summary</h4>
                <div class="text-sm px-2 py-1 bg-violet-500/20 rounded-md text-violet-200">All Formats</div>
              </div>
              <div class="flex items-baseline gap-2">
                <span class="text-3xl font-bold text-white">#{{ player?.rankings?.all?.t20BestRank || '-' }}</span>
                <span class="text-violet-300">T20I All-Rounder</span>
              </div>
              <div class="mt-3 text-sm text-violet-300">
                {{ getCareerSummary() }}
              </div>
            </div>
          </div>
        </div>
        
        <!-- Biography -->
        <div v-if="activeTab === 'bio'" class="p-4 md:p-6">
          <h3 class="text-xl font-bold text-white mb-4">Biography</h3>
          
          <div class="bg-white/5 backdrop-blur-sm rounded-lg p-5 border border-indigo-500/10">
            <div class="space-y-4 text-indigo-100 max-h-96 overflow-y-auto pr-2 bio-content">
              <div v-html="player.bio" class="leading-relaxed"></div>
            </div>
          </div>
          
          <!-- Timeline -->
          <div class="mt-8">
            <h4 class="text-lg font-medium text-white mb-4">Career Timeline</h4>
            
            <div class="relative border-l-2 border-indigo-500/50 ml-4 pl-8 pb-4">
              <div v-for="(event, index) in careerEvents" :key="index" class="mb-8 relative">
                <div class="absolute w-4 h-4 bg-indigo-500 rounded-full -left-10 mt-1"></div>
                <div class="text-indigo-300 font-medium">{{ event.date }}</div>
                <div class="text-white mt-1">{{ event.content }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import playerInfo from '../sample-responses/player-detail/player-info.json'
import playerBowlingStats from '../sample-responses/player-detail/player-bowling-stats.json'
import playerBattingStats from '../sample-responses/player-detail/player-batting-stats.json'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { RadarChart, BarChart, LineChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

// Register ECharts components
use([
  CanvasRenderer,
  RadarChart,
  BarChart,
  LineChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
])

const route = useRoute()
const router = useRouter()
const player = ref(null)
const loading = ref(true)
const error = ref(null)
const activeTab = ref('highlights')
const battingStats = ref(playerBattingStats)
const bowlingStats = ref(playerBowlingStats)

const tabs = [
  { id: 'highlights', name: 'Highlights' },
  { id: 'batting', name: 'Batting Statistics' },
  { id: 'bowling', name: 'Bowling Statistics' },
  { id: 'rankings', name: 'Rankings' },
  { id: 'bio', name: 'Biography' }
]

// Helper functions
const getTeamHue = (id) => {
  // Generate consistent color based on teamId
  const numId = parseInt(id) || 0;
  return (numId * 40) % 360; // This creates a variety of colors across the spectrum
}

const formatBattingStyle = (style) => {
  if (!style) return '';
  return style.replace('Handed', '');
}

// Extract career events from player biography
const careerEvents = computed(() => {
  if (!player.value || !player.value.bio) return [];
  
  // Remove HTML tags to get plain text
  const plainText = player.value.bio.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');
  
  // Regular expressions to find years and significant events
  const yearPattern = /\b(19[8-9][0-9]|20[0-2][0-9])\b/g;
  const years = [...plainText.matchAll(yearPattern)];
  
  const events = [];
  
  // Keywords that indicate significant career events
  const significantKeywords = [
    'World Cup', 'IPL', 'trophy', 'debut', 'captain', 
    'appointed', 'named', 'joined', 'signed', 'selected', 
    'award', 'won', 'finals', 'triumph', 'victory', 
    'championship', 'Gujarat Titans', 'Mumbai Indians'
  ];
  
  // For each year found, extract the surrounding context
  years.forEach(yearMatch => {
    const year = yearMatch[0];
    const yearIndex = yearMatch.index;
    
    // Get text around the year (50 chars before and 100 chars after)
    let startIndex = Math.max(0, yearIndex - 50);
    let endIndex = Math.min(plainText.length, yearIndex + 100);
    let context = plainText.substring(startIndex, endIndex);
    
    // Check if this context contains any significant keywords
    const hasSignificantEvent = significantKeywords.some(keyword => 
      context.toLowerCase().includes(keyword.toLowerCase())
    );
    
    if (hasSignificantEvent) {
      // Find a sentence boundary to create a more natural context
      let content = context;
      
      // Try to extract just the relevant sentence by finding periods
      const sentenceBoundaries = [...content.matchAll(/\./g)];
      if (sentenceBoundaries.length > 0) {
        // Find the sentence containing the year
        for (let i = 0; i < sentenceBoundaries.length - 1; i++) {
          if (sentenceBoundaries[i].index < (yearIndex - startIndex) && 
              (yearIndex - startIndex) < sentenceBoundaries[i+1].index) {
            content = content.substring(
              sentenceBoundaries[i].index + 1, 
              sentenceBoundaries[i+1].index + 1
            ).trim();
            break;
          }
        }
      }
      
      // Make sure content is not too long
      if (content.length > 100) {
        content = content.substring(0, 97) + '...';
      }
      
      // Clean up the content
      content = content.trim();
      
      // Avoid duplicate events for the same year
      if (!events.some(event => event.date === year && event.content === content)) {
        events.push({
          date: year,
          content: content
        });
      }
    }
  });
  
  // Sort events chronologically
  events.sort((a, b) => parseInt(a.date) - parseInt(b.date));
  
  // Limit to most significant events
  return events.slice(0, 6);
})

// Chart options
const battingRadarOption = computed(() => ({
  backgroundColor: 'transparent',
  title: {
    text: 'Batting Performance Analysis',
    textStyle: {
      color: '#fff',
      fontSize: 20,
      fontWeight: 'bold'
    },
    left: 'center',
    top: 30,
    padding: [0, 0, 20, 0]
  },
  tooltip: {
    trigger: 'item',
    backgroundColor: 'rgba(17, 24, 39, 0.95)',
    borderColor: 'rgba(99, 102, 241, 0.5)',
    borderWidth: 2,
    textStyle: {
      color: '#fff',
      fontSize: 14
    },
    formatter: (params) => {
      let result = `<div style="font-weight: bold; margin-bottom: 10px;">${params.name}</div>`;
      params.value.forEach((value, index) => {
        const metric = params.seriesName === 'T20I' ? [
          'Runs per Innings', 'Strike Rate', 'Average', 'Boundary %', 
          'Six %', 'Pressure Handling', 'Impact Score', 'Consistency'
        ][index] : [
          'Runs per Innings', 'Strike Rate', 'Average', 'Boundary %', 
          'Six %', 'Pressure Handling', 'Impact Score', 'Consistency'
        ][index];
        
        const formattedValue = metric.includes('Rate') ? value.toFixed(2) :
                             metric.includes('Average') ? value.toFixed(1) :
                             metric.includes('%') ? value.toFixed(1) + '%' :
                             value;
        result += `<div style="margin: 6px 0;"><span style="color: ${params.color}">${metric}:</span> ${formattedValue}</div>`;
      });
      return result;
    }
  },
  legend: {
    data: ['T20I', 'ODI', 'Test'],
    textStyle: {
      color: '#9CA3AF',
      fontSize: 14
    },
    top: 100,
    itemWidth: 14,
    itemHeight: 14,
    itemGap: 40,
    icon: 'roundRect',
    padding: [0, 30]
  },
  radar: {
    indicator: [
      { name: 'Runs per Innings', max: 120 },
      { name: 'Strike Rate', max: 150 },
      { name: 'Average', max: 50 },
      { name: 'Boundary %', max: 80 },
      { name: 'Six %', max: 40 },
      { name: 'Pressure Handling', max: 100 },
      { name: 'Impact Score', max: 100 },
      { name: 'Consistency', max: 100 }
    ],
    radius: '60%',
    center: ['50%', '70%'],
    splitNumber: 5,
    axisName: {
      color: '#9CA3AF',
      fontSize: 13,
      padding: [10, 15],
      backgroundColor: 'rgba(17, 24, 39, 0.3)',
      borderRadius: 4,
      formatter: (name) => {
        const shortName = name.length > 12 ? name.substring(0, 12) + '...' : name;
        return shortName;
      }
    },
    splitLine: {
      lineStyle: {
        color: 'rgba(75, 85, 99, 0.2)',
        width: 2
      }
    },
    splitArea: {
      show: true,
      areaStyle: {
        color: ['rgba(75, 85, 99, 0.05)', 'rgba(75, 85, 99, 0.1)', 
                'rgba(75, 85, 99, 0.15)', 'rgba(75, 85, 99, 0.2)', 
                'rgba(75, 85, 99, 0.25)']
      }
    },
    axisLine: {
      lineStyle: {
        color: 'rgba(75, 85, 99, 0.4)',
        width: 2
      }
    }
  },
  series: [
    {
      name: 'T20I',
      type: 'radar',
      data: [[
        85, 141.68, 35.2, 75, 35, 85, 90, 80
      ]],
      symbol: 'circle',
      symbolSize: 10,
      lineStyle: {
        width: 3,
        color: '#60A5FA'
      },
      itemStyle: {
        color: '#60A5FA',
        borderWidth: 2,
        borderColor: '#fff'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [{
            offset: 0,
            color: 'rgba(96, 165, 250, 0.3)'
          }, {
            offset: 1,
            color: 'rgba(96, 165, 250, 0.1)'
          }]
        }
      },
      emphasis: {
        lineStyle: {
          width: 4,
          color: '#93C5FD'
        },
        itemStyle: {
          color: '#93C5FD',
          borderColor: '#fff',
          borderWidth: 3,
          shadowColor: 'rgba(96, 165, 250, 0.5)',
          shadowBlur: 10
        }
      }
    },
    {
      name: 'ODI',
      type: 'radar',
      data: [[
        92, 110.90, 42.3, 65, 25, 80, 85, 85
      ]],
      symbol: 'circle',
      symbolSize: 10,
      lineStyle: {
        width: 3,
        color: '#34D399'
      },
      itemStyle: {
        color: '#34D399',
        borderWidth: 2,
        borderColor: '#fff'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [{
            offset: 0,
            color: 'rgba(52, 211, 153, 0.3)'
          }, {
            offset: 1,
            color: 'rgba(52, 211, 153, 0.1)'
          }]
        }
      },
      emphasis: {
        lineStyle: {
          width: 4,
          color: '#6EE7B7'
        },
        itemStyle: {
          color: '#6EE7B7',
          borderColor: '#fff',
          borderWidth: 3,
          shadowColor: 'rgba(52, 211, 153, 0.5)',
          shadowBlur: 10
        }
      }
    },
    {
      name: 'Test',
      type: 'radar',
      data: [[
        108, 65.4, 38.7, 60, 15, 70, 75, 90
      ]],
      symbol: 'circle',
      symbolSize: 10,
      lineStyle: {
        width: 3,
        color: '#F59E0B'
      },
      itemStyle: {
        color: '#F59E0B',
        borderWidth: 2,
        borderColor: '#fff'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [{
            offset: 0,
            color: 'rgba(245, 158, 11, 0.3)'
          }, {
            offset: 1,
            color: 'rgba(245, 158, 11, 0.1)'
          }]
        }
      },
      emphasis: {
        lineStyle: {
          width: 4,
          color: '#FBBF24'
        },
        itemStyle: {
          color: '#FBBF24',
          borderColor: '#fff',
          borderWidth: 3,
          shadowColor: 'rgba(245, 158, 11, 0.5)',
          shadowBlur: 10
        }
      }
    }
  ]
}))

const bowlingBarOption = computed(() => ({
  backgroundColor: 'transparent',
  title: {
    text: 'Bowling Performance Analysis',
    textStyle: {
      color: '#fff',
      fontSize: 16,
      fontWeight: 'bold'
    },
    left: 'center',
    top: 10
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    },
    backgroundColor: 'rgba(17, 24, 39, 0.95)',
    borderColor: 'rgba(99, 102, 241, 0.5)',
    borderWidth: 2,
    textStyle: {
      color: '#fff',
      fontSize: 13
    },
    formatter: (params) => {
      let result = `${params[0].axisValue}<br/>`;
      params.forEach(param => {
        result += `${param.seriesName}: ${param.value}<br/>`;
      });
      return result;
    }
  },
  legend: {
    data: ['Wickets', 'Economy Rate', 'Strike Rate', 'Average'],
    textStyle: {
      color: '#9CA3AF',
      fontSize: 13
    },
    top: 40,
    itemWidth: 12,
    itemHeight: 12,
    itemGap: 20,
    icon: 'roundRect'
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '25%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['T20I', 'ODI', 'Test'],
    axisLabel: {
      color: '#9CA3AF',
      fontSize: 13
    },
    axisLine: {
      lineStyle: {
        color: 'rgba(75, 85, 99, 0.4)',
        width: 2
      }
    },
    axisTick: {
      show: false
    }
  },
  yAxis: [
    {
      type: 'value',
      name: 'Wickets',
      axisLabel: {
        color: '#9CA3AF',
        fontSize: 12
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(75, 85, 99, 0.4)',
          width: 2
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(75, 85, 99, 0.1)'
        }
      }
    },
    {
      type: 'value',
      name: 'Rate',
      axisLabel: {
        color: '#9CA3AF',
        fontSize: 12
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(75, 85, 99, 0.4)',
          width: 2
        }
      },
      splitLine: {
        show: false
      }
    }
  ],
  series: [
    {
      name: 'Wickets',
      type: 'bar',
      data: [74, 91, 37],
      itemStyle: {
        color: '#60A5FA'
      },
      barWidth: '15%',
      emphasis: {
        itemStyle: {
          color: '#93C5FD'
        }
      }
    },
    {
      name: 'Economy Rate',
      type: 'bar',
      yAxisIndex: 1,
      data: [7.2, 5.8, 3.4],
      itemStyle: {
        color: '#34D399'
      },
      barWidth: '15%',
      emphasis: {
        itemStyle: {
          color: '#6EE7B7'
        }
      }
    },
    {
      name: 'Strike Rate',
      type: 'line',
      yAxisIndex: 1,
      data: [18.5, 32.4, 45.2],
      itemStyle: {
        color: '#F59E0B'
      },
      lineStyle: {
        width: 3
      },
      symbol: 'circle',
      symbolSize: 8,
      emphasis: {
        itemStyle: {
          color: '#FBBF24'
        }
      }
    },
    {
      name: 'Average',
      type: 'line',
      yAxisIndex: 1,
      data: [24.3, 28.7, 31.5],
      itemStyle: {
        color: '#EC4899'
      },
      lineStyle: {
        width: 3
      },
      symbol: 'circle',
      symbolSize: 8,
      emphasis: {
        itemStyle: {
          color: '#F472B6'
        }
      }
    }
  ]
}))

const rankingsLineOption = computed(() => ({
  backgroundColor: 'transparent',
  title: {
    text: 'ICC Rankings Progression',
    textStyle: {
      color: '#fff',
      fontSize: 16,
      fontWeight: 'bold'
    },
    left: 'center',
    top: 10
  },
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(17, 24, 39, 0.95)',
    borderColor: 'rgba(99, 102, 241, 0.5)',
    borderWidth: 2,
    textStyle: {
      color: '#fff',
      fontSize: 13
    },
    formatter: (params) => {
      let result = `${params[0].axisValue}<br/>`;
      params.forEach(param => {
        const color = param.color;
        result += `<span style="color: ${color}">${param.seriesName}: #${param.value}</span><br/>`;
      });
      return result;
    }
  },
  legend: {
    data: ['T20I', 'ODI', 'Test'],
    textStyle: {
      color: '#9CA3AF',
      fontSize: 13
    },
    top: 40,
    itemWidth: 12,
    itemHeight: 12,
    itemGap: 25,
    icon: 'roundRect'
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    top: '25%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    axisLabel: {
      color: '#9CA3AF',
      fontSize: 12
    },
    axisLine: {
      lineStyle: {
        color: 'rgba(75, 85, 99, 0.4)',
        width: 2
      }
    },
    axisTick: {
      show: false
    }
  },
  yAxis: {
    type: 'value',
    inverse: true,
    min: 1,
    max: 20,
    axisLabel: {
      color: '#9CA3AF',
      fontSize: 12
    },
    axisLine: {
      lineStyle: {
        color: 'rgba(75, 85, 99, 0.4)',
        width: 2
      }
    },
    splitLine: {
      lineStyle: {
        color: 'rgba(75, 85, 99, 0.1)'
      }
    }
  },
  series: [
    {
      name: 'T20I',
      type: 'line',
      data: [3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      itemStyle: {
        color: '#60A5FA'
      },
      lineStyle: {
        width: 3
      },
      areaStyle: {
        color: 'rgba(96, 165, 250, 0.2)'
      },
      symbol: 'circle',
      symbolSize: 8,
      emphasis: {
        itemStyle: {
          color: '#93C5FD'
        }
      }
    },
    {
      name: 'ODI',
      type: 'line',
      data: [5, 4, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2],
      itemStyle: {
        color: '#34D399'
      },
      lineStyle: {
        width: 3
      },
      areaStyle: {
        color: 'rgba(52, 211, 153, 0.2)'
      },
      symbol: 'circle',
      symbolSize: 8,
      emphasis: {
        itemStyle: {
          color: '#6EE7B7'
        }
      }
    },
    {
      name: 'Test',
      type: 'line',
      data: [8, 7, 6, 6, 5, 5, 5, 5, 5, 5, 5, 5],
      itemStyle: {
        color: '#F59E0B'
      },
      lineStyle: {
        width: 3
      },
      areaStyle: {
        color: 'rgba(245, 158, 11, 0.2)'
      },
      symbol: 'circle',
      symbolSize: 8,
      emphasis: {
        itemStyle: {
          color: '#FBBF24'
        }
      }
    }
  ]
}))

const fetchPlayerData = async () => {
  loading.value = true
  error.value = null
  
  try {
    // In a real app, this would fetch from API
    await new Promise(resolve => setTimeout(resolve, 1000))
    player.value = playerInfo
    
    // Normally these would be fetched from API too
    battingStats.value = playerBattingStats
    bowlingStats.value = playerBowlingStats
  } catch (err) {
    error.value = 'Failed to load player data. Please try again later.'
    console.error('Error fetching player data:', err)
  } finally {
    loading.value = false
  }
}

watch(() => route.params.id, () => {
  fetchPlayerData()
})

onMounted(() => {
  fetchPlayerData()
})

const getHighestScore = () => {
  if (!battingStats.value?.values) return '-';
  const highestRow = battingStats.value.values.find(row => row.values[0] === 'Highest');
  return highestRow ? highestRow.values[1] : '-';
}

const getCenturiesAndFifties = () => {
  if (!battingStats.value?.values) return '-';
  const centuriesRow = battingStats.value.values.find(row => row.values[0] === '100s');
  const fiftiesRow = battingStats.value.values.find(row => row.values[0] === '50s');
  return `${centuriesRow?.values[1] || 0} Centuries, ${fiftiesRow?.values[1] || 0} Fifties`;
}

const getBestBowling = () => {
  if (!bowlingStats.value?.values) return '-';
  const bbiRow = bowlingStats.value.values.find(row => row.values[0] === 'BBI');
  return bbiRow ? bbiRow.values[1] : '-';
}

const getFiveWicketHauls = () => {
  if (!bowlingStats.value?.values) return '-';
  const fiveWRow = bowlingStats.value.values.find(row => row.values[0] === '5w');
  return `${fiveWRow?.values[1] || 0} Five-wicket haul${fiveWRow?.values[1] === '1' ? '' : 's'}`;
}

const getT20StrikeRate = () => {
  if (!battingStats.value?.values) return '-';
  const srRow = battingStats.value.values.find(row => row.values[0] === 'SR');
  return srRow ? srRow.values[3] : '-';
}

const getT20Highlights = () => {
  if (!battingStats.value?.values || !bowlingStats.value?.values) return '-';
  const sixesRow = battingStats.value.values.find(row => row.values[0] === 'Sixes');
  const bbiRow = bowlingStats.value.values.find(row => row.values[0] === 'BBI');
  return `${sixesRow?.values[3] || 0} Sixes, ${bbiRow?.values[3] || '-'} Best Bowling`;
}

const getIPLStrikeRate = () => {
  if (!battingStats.value?.values) return '-';
  const srRow = battingStats.value.values.find(row => row.values[0] === 'SR');
  return srRow ? srRow.values[4] : '-';
}

const getIPLHighlights = () => {
  if (!battingStats.value?.values || !bowlingStats.value?.values) return '-';
  const matchesRow = battingStats.value.values.find(row => row.values[0] === 'Matches');
  const sixesRow = battingStats.value.values.find(row => row.values[0] === 'Sixes');
  const wicketsRow = bowlingStats.value.values.find(row => row.values[0] === 'Wickets');
  return `${matchesRow?.values[4] || 0} Matches, ${sixesRow?.values[4] || 0} Sixes, ${wicketsRow?.values[4] || 0} Wickets`;
}

const getODIStrikeRate = () => {
  if (!battingStats.value?.values) return '-';
  const srRow = battingStats.value.values.find(row => row.values[0] === 'SR');
  return srRow ? srRow.values[2] : '-';
}

const getODIHighlights = () => {
  if (!battingStats.value?.values || !bowlingStats.value?.values) return '-';
  const matchesRow = battingStats.value.values.find(row => row.values[0] === 'Matches');
  const runsRow = battingStats.value.values.find(row => row.values[0] === 'Runs');
  const wicketsRow = bowlingStats.value.values.find(row => row.values[0] === 'Wickets');
  return `${matchesRow?.values[2] || 0} Matches, ${wicketsRow?.values[2] || 0} Wickets, ${runsRow?.values[2] || 0} Runs`;
}

const getCareerSummary = () => {
  if (!player.value?.rankings?.all?.t20BestRank) return '-';
  const totalWickets = bowlingStats.value?.values
    ?.find(row => row.values[0] === 'Wickets')
    ?.values.slice(1)
    .reduce((sum, val) => sum + parseInt(val || 0), 0) || 0;
  return `Ranked #${player.value.rankings.all.t20BestRank} in T20I All-Rounders, ${totalWickets} Wickets across formats`;
}
</script>

<style scoped>
/* Bio scrollbar styling */
.bio-content::-webkit-scrollbar {
  width: 8px;
}

.bio-content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.bio-content::-webkit-scrollbar-thumb {
  background: rgba(99, 102, 241, 0.3);
  border-radius: 4px;
}

.bio-content::-webkit-scrollbar-thumb:hover {
  background: rgba(99, 102, 241, 0.5);
}
</style> 