<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Player Selection Section -->
    <div class="bg-slate-800/60 rounded-lg p-6 backdrop-blur-sm mb-8">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-white">Player Comparison</h2>
        <div class="flex items-center space-x-4">
          <span class="text-sm text-slate-400">{{ selectedPlayers.length }}/11 Players</span>
          <button v-if="selectedPlayers.length > 0" 
                  @click="clearAllPlayers"
                  class="text-sm text-red-400 hover:text-red-300">
            Clear All
          </button>
        </div>
      </div>
      
      <!-- Player Selection Grid -->
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <!-- Selected Players -->
        <div v-for="(player, index) in selectedPlayers" :key="index" 
             class="bg-slate-700/40 rounded-lg p-3 relative group">
          <div class="flex flex-col items-center">
            <img :src="getPlayerImage(player.faceImageId)" 
                  :alt="player.name"
                 class="w-16 h-16 rounded-full object-cover mb-2" />
            <div class="text-center">
              <h3 class="text-sm font-semibold text-white truncate">{{ player.name }}</h3>
              <p class="text-xs text-slate-400">{{ player.role }}</p>
            </div>
            <button @click="removePlayer(index)"
                    class="absolute top-1 right-1 text-slate-400 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Add Player Button -->
        <div v-if="selectedPlayers.length < 11" 
             @click="showPlayerSelector = true"
             class="bg-slate-700/40 rounded-lg p-3 flex items-center justify-center cursor-pointer hover:bg-slate-700/60">
          <div class="text-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-400 mx-auto mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            <p class="text-xs text-slate-400">Add Player</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Comparison Charts -->
    <div v-if="selectedPlayers.length >= 2" class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Overall Stats -->
      <div class="bg-slate-800/60 rounded-lg p-4 backdrop-blur-sm">
        <h3 class="text-lg font-bold text-white mb-4">Overall Performance</h3>
        <div ref="overallStatsChart" class="w-full h-[300px]"></div>
      </div>

      <!-- Batting Comparison -->
      <div class="bg-slate-800/60 rounded-lg p-4 backdrop-blur-sm">
        <h3 class="text-lg font-bold text-white mb-4">Batting Statistics</h3>
        <div ref="battingChart" class="w-full h-[300px]"></div>
      </div>

      <!-- Bowling Comparison -->
      <div class="bg-slate-800/60 rounded-lg p-4 backdrop-blur-sm">
        <h3 class="text-lg font-bold text-white mb-4">Bowling Statistics</h3>
        <div ref="bowlingChart" class="w-full h-[300px]"></div>
      </div>
      
      <!-- Form Trend -->
      <div class="bg-slate-800/60 rounded-lg p-4 backdrop-blur-sm">
        <h3 class="text-lg font-bold text-white mb-4">Recent Form</h3>
        <div ref="formChart" class="w-full h-[300px]"></div>
    </div>
  </div>

  <!-- Player Selector Modal -->
  <div v-if="showPlayerSelector" 
       class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
       @click.self="showPlayerSelector = false">
      <div class="bg-slate-800/90 rounded-xl p-6 w-full max-w-2xl mx-4">
      <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-bold text-white">Select Player</h3>
          <button @click="showPlayerSelector = false" class="text-slate-400 hover:text-white">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <!-- Search Bar -->
      <div class="relative mb-4">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search players..." 
            class="w-full pl-10 pr-4 py-2 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-400 absolute left-3 top-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
      </div>
      
      <!-- Player List -->
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 max-h-[50vh] overflow-y-auto">
          <div v-for="player in filteredPlayers" 
               :key="player.id"
               @click="addPlayer(player)"
               class="flex items-center gap-2 p-2 rounded-lg hover:bg-slate-700/50 cursor-pointer">
            <img :src="getPlayerImage(player.faceImageId)" 
              :alt="player.name"
                 class="w-10 h-10 rounded-full object-cover" />
            <div>
              <h4 class="text-sm font-medium text-white">{{ player.name }}</h4>
              <p class="text-xs text-slate-400">{{ player.role }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

// State
const selectedPlayers = ref([])
const showPlayerSelector = ref(false)
const searchQuery = ref('')

// Chart refs
const overallStatsChart = ref(null)
const battingChart = ref(null)
const bowlingChart = ref(null)
const formChart = ref(null)

// Chart instances
let charts = {
  overall: null,
  batting: null,
  bowling: null,
  form: null
}

// Sample players data with detailed stats
const players = ref([
  {
    id: "1413",
    name: "Virat Kohli",
    role: "Batsman",
    bat: "Right Handed Bat",
    bowl: "Right-arm medium",
    faceImageId: 616517,
    stats: {
      test: {
        batting: {
          matches: 123,
          innings: 210,
          runs: 9230,
          balls: 16608,
          highest: 254,
          average: 46.85,
          strikeRate: 55.58,
          notOut: 13,
          fours: 1027,
          sixes: 30,
          ducks: 15,
          fifties: 31,
          hundreds: 30,
          twoHundreds: 7
        },
        bowling: {
          matches: 123,
          innings: 11,
          balls: 175,
          runs: 84,
          maidens: 2,
          wickets: 0,
          average: 0.0,
          economy: 2.88,
          strikeRate: 0.0,
          bestBowling: "0/0",
          bestBowlingMatch: "0/0"
        }
      },
      odi: {
        batting: {
          matches: 302,
          innings: 290,
          runs: 14181,
          balls: 15192,
          highest: 183,
          average: 57.88,
          strikeRate: 93.35,
          notOut: 45,
          fours: 1325,
          sixes: 153,
          ducks: 16,
          fifties: 74,
          hundreds: 51
        },
        bowling: {
          matches: 302,
          innings: 50,
          balls: 662,
          runs: 680,
          maidens: 1,
          wickets: 5,
          average: 136.0,
          economy: 6.16,
          strikeRate: 132.4,
          bestBowling: "1/13",
          bestBowlingMatch: "1/13"
        }
      },
      t20: {
        batting: {
          matches: 125,
          innings: 117,
          runs: 4188,
          balls: 3056,
          highest: 122,
          average: 48.7,
          strikeRate: 137.05,
          notOut: 31,
          fours: 369,
          sixes: 124,
          ducks: 7,
          fifties: 38,
          hundreds: 1
        },
        bowling: {
          matches: 125,
          innings: 13,
          balls: 152,
          runs: 204,
          maidens: 0,
          wickets: 4,
          average: 51.0,
          economy: 8.05,
          strikeRate: 38.0,
          bestBowling: "1/13",
          bestBowlingMatch: "1/13"
        }
      },
      ipl: {
        batting: {
          matches: 256,
          innings: 248,
          runs: 8168,
          balls: 6179,
          highest: 113,
          average: 38.9,
          strikeRate: 132.19,
          notOut: 38,
          fours: 720,
          sixes: 278,
          ducks: 10,
          fifties: 57,
          hundreds: 8
        },
        bowling: {
          matches: 256,
          innings: 26,
          balls: 251,
          runs: 368,
          maidens: 0,
          wickets: 4,
          average: 92.0,
          economy: 8.8,
          strikeRate: 62.75,
          bestBowling: "2/25",
          bestBowlingMatch: "2/25"
        }
      }
    }
  },
  {
    id: "576",
    name: "Rohit Sharma",
    role: "Batsman",
    bat: "Right Handed Bat",
    bowl: "Right-arm offbreak",
    faceImageId: 616514,
    stats: {
      test: {
        batting: {
          matches: 52,
          innings: 88,
          runs: 3677,
          balls: 6421,
          highest: 212,
          average: 46.54,
          strikeRate: 57.27,
          notOut: 6,
          fours: 405,
          sixes: 52,
          ducks: 8,
          fifties: 16,
          hundreds: 10,
          twoHundreds: 1
        },
        bowling: {
          matches: 52,
          innings: 8,
          balls: 120,
          runs: 80,
          maidens: 0,
          wickets: 2,
          average: 40.0,
          economy: 4.0,
          strikeRate: 60.0,
          bestBowling: "1/26",
          bestBowlingMatch: "1/26"
        }
      },
      odi: {
        batting: {
          matches: 262,
          innings: 254,
          runs: 10709,
          balls: 11647,
          highest: 264,
          average: 49.12,
          strikeRate: 91.97,
          notOut: 36,
          fours: 994,
          sixes: 323,
          ducks: 15,
          fifties: 55,
          hundreds: 31
        },
        bowling: {
          matches: 262,
          innings: 35,
          balls: 383,
          runs: 361,
          maidens: 1,
          wickets: 8,
          average: 45.12,
          economy: 5.65,
          strikeRate: 47.87,
          bestBowling: "2/27",
          bestBowlingMatch: "2/27"
        }
      },
      t20: {
        batting: {
          matches: 151,
          innings: 140,
          runs: 3853,
          balls: 2767,
          highest: 118,
          average: 31.32,
          strikeRate: 139.24,
          notOut: 17,
          fours: 337,
          sixes: 182,
          ducks: 10,
          fifties: 21,
          hundreds: 4
        },
        bowling: {
          matches: 151,
          innings: 9,
          balls: 78,
          runs: 116,
          maidens: 0,
          wickets: 4,
          average: 29.0,
          economy: 8.92,
          strikeRate: 19.5,
          bestBowling: "1/22",
          bestBowlingMatch: "1/22"
        }
      },
      ipl: {
        batting: {
          matches: 243,
          innings: 235,
          runs: 6211,
          balls: 4572,
          highest: 109,
          average: 29.58,
          strikeRate: 135.85,
          notOut: 23,
          fours: 554,
          sixes: 257,
          ducks: 14,
          fifties: 40,
          hundreds: 1
        },
        bowling: {
          matches: 243,
          innings: 15,
          balls: 120,
          runs: 180,
          maidens: 0,
          wickets: 4,
          average: 45.0,
          economy: 9.0,
          strikeRate: 30.0,
          bestBowling: "1/6",
          bestBowlingMatch: "1/6"
        }
      }
    }
  }
])

// Computed
const filteredPlayers = computed(() => {
  if (!searchQuery.value) return players.value
  const query = searchQuery.value.toLowerCase()
  return players.value.filter(player => 
    player.name.toLowerCase().includes(query) || 
    player.role.toLowerCase().includes(query)
  )
})

// Methods
const getPlayerImage = (imageId) => {
  return `http://static.cricbuzz.com/a/img/v1/i1/c${imageId}/i.jpg?p=thumb`
}

const addPlayer = (player) => {
  if (selectedPlayers.value.length < 11 && !selectedPlayers.value.find(p => p.id === player.id)) {
    selectedPlayers.value.push(player)
    showPlayerSelector.value = false
  }
}

const removePlayer = (index) => {
  selectedPlayers.value.splice(index, 1)
}

const clearAllPlayers = () => {
  selectedPlayers.value = []
}

// Chart initialization
const initCharts = () => {
  if (selectedPlayers.value.length < 2) return

  // Clean up existing charts first
  Object.values(charts).forEach(chart => {
    if (chart) {
      chart.dispose()
    }
  })

  // Reset chart instances
  charts = {
    overall: null,
    batting: null,
    bowling: null,
    form: null
  }

  // Wait for next tick to ensure DOM is ready
  nextTick(() => {
    try {
      // Initialize charts only if elements exist
      if (overallStatsChart.value) {
        charts.overall = echarts.init(overallStatsChart.value)
      }
      if (battingChart.value) {
        charts.batting = echarts.init(battingChart.value)
      }
      if (bowlingChart.value) {
        charts.bowling = echarts.init(bowlingChart.value)
      }
      if (formChart.value) {
        charts.form = echarts.init(formChart.value)
      }

      // Update charts after initialization
      updateCharts()
    } catch (error) {
      console.error('Error initializing charts:', error)
    }
  })
}

// Update charts with detailed stats
const updateCharts = () => {
  if (selectedPlayers.value.length < 2) return

  try {
    // Overall Stats Chart - Advanced Radar with Multiple Indicators
    if (charts.overall) {
      const overallOption = {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'item',
          formatter: function(params) {
            const data = params.data;
            let result = `<div style="font-weight:bold;margin-bottom:5px">${data.name}</div>`;
            const indicators = ['Test Average', 'ODI Average', 'Test 100s', 'ODI 100s', 'Test SR', 'ODI SR'];
            data.value.forEach((value, index) => {
              result += `${indicators[index]}: ${value}<br/>`;
            });
            return result;
          }
        },
        legend: {
          data: selectedPlayers.value.map(p => p.name),
          textStyle: { color: '#fff' },
          icon: 'circle',
          itemWidth: 10,
          itemHeight: 10,
          itemGap: 20,
          top: 0
        },
        radar: {
          indicator: [
            { name: 'Test Average', max: 60 },
            { name: 'ODI Average', max: 60 },
            { name: 'Test 100s', max: 40 },
            { name: 'ODI 100s', max: 60 },
            { name: 'Test Strike Rate', max: 60 },
            { name: 'ODI Strike Rate', max: 100 }
          ],
          splitArea: {
            areaStyle: {
              color: ['rgba(255,255,255,0.02)', 'rgba(255,255,255,0.05)',
                     'rgba(255,255,255,0.08)', 'rgba(255,255,255,0.11)',
                     'rgba(255,255,255,0.14)']
            }
          },
          axisLine: {
            lineStyle: { 
              color: 'rgba(255,255,255,0.2)',
              width: 2
            }
          },
          splitLine: {
            lineStyle: { 
              color: 'rgba(255,255,255,0.2)',
              width: 1
            }
          },
          name: {
            textStyle: {
              color: '#94a3b8',
              fontSize: 12
            }
          },
          center: ['50%', '55%'],
          radius: '65%'
        },
        series: [{
          type: 'radar',
          data: selectedPlayers.value.map((player, index) => {
            const colors = [
              { start: 'rgba(99, 102, 241, 0.8)', end: 'rgba(99, 102, 241, 0.2)', line: '#6366f1' },
              { start: 'rgba(244, 63, 94, 0.8)', end: 'rgba(244, 63, 94, 0.2)', line: '#f43f5e' },
              { start: 'rgba(34, 197, 94, 0.8)', end: 'rgba(34, 197, 94, 0.2)', line: '#22c55e' },
              { start: 'rgba(234, 179, 8, 0.8)', end: 'rgba(234, 179, 8, 0.2)', line: '#eab308' },
              { start: 'rgba(168, 85, 247, 0.8)', end: 'rgba(168, 85, 247, 0.2)', line: '#a855f7' },
              { start: 'rgba(14, 165, 233, 0.8)', end: 'rgba(14, 165, 233, 0.2)', line: '#0ea5e9' },
              { start: 'rgba(249, 115, 22, 0.8)', end: 'rgba(249, 115, 22, 0.2)', line: '#f97316' },
              { start: 'rgba(236, 72, 153, 0.8)', end: 'rgba(236, 72, 153, 0.2)', line: '#ec4899' },
              { start: 'rgba(6, 182, 212, 0.8)', end: 'rgba(6, 182, 212, 0.2)', line: '#06b6d4' },
              { start: 'rgba(220, 38, 38, 0.8)', end: 'rgba(220, 38, 38, 0.2)', line: '#dc2626' },
              { start: 'rgba(79, 70, 229, 0.8)', end: 'rgba(79, 70, 229, 0.2)', line: '#4f46e5' }
            ];
            const color = colors[index % colors.length];
            
            return {
              value: [
                player.stats.test.batting.average,
                player.stats.odi.batting.average,
                player.stats.test.batting.hundreds,
                player.stats.odi.batting.hundreds,
                player.stats.test.batting.strikeRate,
                player.stats.odi.batting.strikeRate
              ],
              name: player.name,
              areaStyle: { 
                opacity: 0.3,
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: color.start },
                  { offset: 1, color: color.end }
                ])
              },
              lineStyle: {
                width: 3,
                color: color.line
              },
              itemStyle: {
                color: color.line
              }
            };
          })
        }]
      }
      charts.overall.setOption(overallOption)
    }

    // Batting Comparison Chart - Advanced Bar Chart with Multiple Metrics
    if (charts.batting) {
      const battingOption = {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'axis',
          axisPointer: { 
            type: 'shadow',
            shadowStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          }
        },
        legend: {
          data: ['Test', 'ODI', 'T20', 'IPL'],
          textStyle: { color: '#fff' },
          icon: 'circle',
          itemWidth: 10,
          itemHeight: 10,
          itemGap: 20,
          top: 0
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          top: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: selectedPlayers.value.map(p => p.name),
          axisLabel: { 
            color: '#fff',
            fontSize: 12,
            fontWeight: 'bold'
          },
          axisLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.2)'
            }
          }
        },
        yAxis: {
          type: 'value',
          axisLabel: { 
            color: '#94a3b8',
            fontSize: 12
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          }
        },
        series: [
          {
            name: 'Test',
            type: 'bar',
            stack: 'total',
            barWidth: '60%',
            data: selectedPlayers.value.map((player, index) => {
              const colors = [
                { start: '#6366f1', end: '#4f46e5' },
                { start: '#f43f5e', end: '#e11d48' },
                { start: '#22c55e', end: '#16a34a' },
                { start: '#eab308', end: '#ca8a04' },
                { start: '#a855f7', end: '#9333ea' },
                { start: '#0ea5e9', end: '#0284c7' },
                { start: '#f97316', end: '#ea580c' },
                { start: '#ec4899', end: '#db2777' },
                { start: '#06b6d4', end: '#0891b2' },
                { start: '#dc2626', end: '#b91c1c' },
                { start: '#4f46e5', end: '#4338ca' }
              ];
              const color = colors[index % colors.length];
              
              return {
                value: player.stats.test.batting.average,
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: color.start },
                    { offset: 1, color: color.end }
                  ])
                }
              };
            })
          },
          {
            name: 'ODI',
            type: 'bar',
            stack: 'total',
            barWidth: '60%',
            data: selectedPlayers.value.map((player, index) => {
              const colors = [
                { start: '#818cf8', end: '#6366f1' },
                { start: '#fb7185', end: '#f43f5e' },
                { start: '#4ade80', end: '#22c55e' },
                { start: '#facc15', end: '#eab308' },
                { start: '#c084fc', end: '#a855f7' },
                { start: '#38bdf8', end: '#0ea5e9' },
                { start: '#fb923c', end: '#f97316' },
                { start: '#f472b6', end: '#ec4899' },
                { start: '#22d3ee', end: '#06b6d4' },
                { start: '#ef4444', end: '#dc2626' },
                { start: '#6366f1', end: '#4f46e5' }
              ];
              const color = colors[index % colors.length];
              
              return {
                value: player.stats.odi.batting.average,
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: color.start },
                    { offset: 1, color: color.end }
                  ])
                }
              };
            })
          },
          {
            name: 'T20',
            type: 'bar',
            stack: 'total',
            barWidth: '60%',
            data: selectedPlayers.value.map((player, index) => {
              const colors = [
                { start: '#a5b4fc', end: '#818cf8' },
                { start: '#fda4af', end: '#fb7185' },
                { start: '#86efac', end: '#4ade80' },
                { start: '#fde047', end: '#facc15' },
                { start: '#d8b4fe', end: '#c084fc' },
                { start: '#7dd3fc', end: '#38bdf8' },
                { start: '#fdba74', end: '#fb923c' },
                { start: '#f9a8d4', end: '#f472b6' },
                { start: '#67e8f9', end: '#22d3ee' },
                { start: '#f87171', end: '#ef4444' },
                { start: '#818cf8', end: '#6366f1' }
              ];
              const color = colors[index % colors.length];
              
              return {
                value: player.stats.t20.batting.average,
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: color.start },
                    { offset: 1, color: color.end }
                  ])
                }
              };
            })
          },
          {
            name: 'IPL',
            type: 'bar',
            stack: 'total',
            barWidth: '60%',
            data: selectedPlayers.value.map((player, index) => {
              const colors = [
                { start: '#c7d2fe', end: '#a5b4fc' },
                { start: '#fecdd3', end: '#fda4af' },
                { start: '#bbf7d0', end: '#86efac' },
                { start: '#fef08a', end: '#fde047' },
                { start: '#e9d5ff', end: '#d8b4fe' },
                { start: '#bae6fd', end: '#7dd3fc' },
                { start: '#fed7aa', end: '#fdba74' },
                { start: '#fbcfe8', end: '#f9a8d4' },
                { start: '#a5f3fc', end: '#67e8f9' },
                { start: '#fca5a5', end: '#f87171' },
                { start: '#a5b4fc', end: '#818cf8' }
              ];
              const color = colors[index % colors.length];
              
              return {
                value: player.stats.ipl.batting.average,
                itemStyle: {
                  color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                    { offset: 0, color: color.start },
                    { offset: 1, color: color.end }
                  ])
                }
              };
            })
          }
        ]
      }
      charts.batting.setOption(battingOption)
    }

    // Bowling Comparison Chart - Advanced Scatter Plot
    if (charts.bowling) {
      const bowlingOption = {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'item',
          formatter: function(params) {
            const data = params.data;
            return `${data.name}<br/>
                    Format: ${data.format}<br/>
                    Wickets: ${data.value[1]}<br/>
                    Economy: ${data.economy}<br/>
                    Average: ${data.average}`;
          }
        },
        legend: {
          data: ['Test', 'ODI', 'T20', 'IPL'],
          textStyle: { color: '#fff' },
          icon: 'circle',
          itemWidth: 10,
          itemHeight: 10,
          itemGap: 20,
          top: 0
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          top: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: 'Economy Rate',
          nameTextStyle: {
            color: '#94a3b8'
          },
          axisLabel: { 
            color: '#94a3b8',
            fontSize: 12
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          }
        },
        yAxis: {
          type: 'value',
          name: 'Wickets',
          nameTextStyle: {
            color: '#94a3b8'
          },
          axisLabel: { 
            color: '#94a3b8',
            fontSize: 12
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          }
        },
        series: [
          {
            name: 'Test',
            type: 'scatter',
            symbolSize: function(data) {
              return Math.sqrt(data[1]) * 8;
            },
            data: selectedPlayers.value.flatMap((player, index) => {
              const colors = [
                '#6366f1', '#f43f5e', '#22c55e', '#eab308', '#a855f7', 
                '#0ea5e9', '#f97316', '#ec4899', '#06b6d4', '#dc2626', '#4f46e5'
              ];
              const color = colors[index % colors.length];
              
              return [{
                name: player.name,
                value: [player.stats.test.bowling.economy, player.stats.test.bowling.wickets],
                format: 'Test',
                economy: player.stats.test.bowling.economy,
                average: player.stats.test.bowling.average,
                itemStyle: {
                  color: color
                }
              }];
            })
          },
          {
            name: 'ODI',
            type: 'scatter',
            symbolSize: function(data) {
              return Math.sqrt(data[1]) * 8;
            },
            data: selectedPlayers.value.flatMap((player, index) => {
              const colors = [
                '#818cf8', '#fb7185', '#4ade80', '#facc15', '#c084fc', 
                '#38bdf8', '#fb923c', '#f472b6', '#22d3ee', '#ef4444', '#6366f1'
              ];
              const color = colors[index % colors.length];
              
              return [{
                name: player.name,
                value: [player.stats.odi.bowling.economy, player.stats.odi.bowling.wickets],
                format: 'ODI',
                economy: player.stats.odi.bowling.economy,
                average: player.stats.odi.bowling.average,
                itemStyle: {
                  color: color
                }
              }];
            })
          },
          {
            name: 'T20',
            type: 'scatter',
            symbolSize: function(data) {
              return Math.sqrt(data[1]) * 8;
            },
            data: selectedPlayers.value.flatMap((player, index) => {
              const colors = [
                '#a5b4fc', '#fda4af', '#86efac', '#fde047', '#d8b4fe', 
                '#7dd3fc', '#fdba74', '#f9a8d4', '#67e8f9', '#f87171', '#818cf8'
              ];
              const color = colors[index % colors.length];
              
              return [{
                name: player.name,
                value: [player.stats.t20.bowling.economy, player.stats.t20.bowling.wickets],
                format: 'T20',
                economy: player.stats.t20.bowling.economy,
                average: player.stats.t20.bowling.average,
                itemStyle: {
                  color: color
                }
              }];
            })
          },
          {
            name: 'IPL',
            type: 'scatter',
            symbolSize: function(data) {
              return Math.sqrt(data[1]) * 8;
            },
            data: selectedPlayers.value.flatMap((player, index) => {
              const colors = [
                '#c7d2fe', '#fecdd3', '#bbf7d0', '#fef08a', '#e9d5ff', 
                '#bae6fd', '#fed7aa', '#fbcfe8', '#a5f3fc', '#fca5a5', '#a5b4fc'
              ];
              const color = colors[index % colors.length];
              
              return [{
                name: player.name,
                value: [player.stats.ipl.bowling.economy, player.stats.ipl.bowling.wickets],
                format: 'IPL',
                economy: player.stats.ipl.bowling.economy,
                average: player.stats.ipl.bowling.average,
                itemStyle: {
                  color: color
                }
              }];
            })
          }
        ]
      }
      charts.bowling.setOption(bowlingOption)
    }

    // Form Trend Chart - Advanced Line Chart with Area
    if (charts.form) {
      const formOption = {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985'
            }
          }
        },
        legend: {
          data: selectedPlayers.value.map(p => p.name),
          textStyle: { color: '#fff' },
          icon: 'circle',
          itemWidth: 10,
          itemHeight: 10,
          itemGap: 20,
          top: 0
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          top: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['Match 1', 'Match 2', 'Match 3', 'Match 4', 'Match 5', 'Match 6', 'Match 7', 'Match 8', 'Match 9', 'Match 10'],
          axisLabel: { 
            color: '#94a3b8',
            fontSize: 12
          },
          axisLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.2)'
            }
          }
        },
        yAxis: {
          type: 'value',
          axisLabel: { 
            color: '#94a3b8',
            fontSize: 12
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255,255,255,0.1)'
            }
          }
        },
        series: selectedPlayers.value.map((player, index) => {
          const colors = [
            { line: '#6366f1', area: ['rgba(99, 102, 241, 0.3)', 'rgba(99, 102, 241, 0.1)'] },
            { line: '#f43f5e', area: ['rgba(244, 63, 94, 0.3)', 'rgba(244, 63, 94, 0.1)'] },
            { line: '#22c55e', area: ['rgba(34, 197, 94, 0.3)', 'rgba(34, 197, 94, 0.1)'] },
            { line: '#eab308', area: ['rgba(234, 179, 8, 0.3)', 'rgba(234, 179, 8, 0.1)'] },
            { line: '#a855f7', area: ['rgba(168, 85, 247, 0.3)', 'rgba(168, 85, 247, 0.1)'] },
            { line: '#0ea5e9', area: ['rgba(14, 165, 233, 0.3)', 'rgba(14, 165, 233, 0.1)'] },
            { line: '#f97316', area: ['rgba(249, 115, 22, 0.3)', 'rgba(249, 115, 22, 0.1)'] },
            { line: '#ec4899', area: ['rgba(236, 72, 153, 0.3)', 'rgba(236, 72, 153, 0.1)'] },
            { line: '#06b6d4', area: ['rgba(6, 182, 212, 0.3)', 'rgba(6, 182, 212, 0.1)'] },
            { line: '#dc2626', area: ['rgba(220, 38, 38, 0.3)', 'rgba(220, 38, 38, 0.1)'] },
            { line: '#4f46e5', area: ['rgba(79, 70, 229, 0.3)', 'rgba(79, 70, 229, 0.1)'] }
          ];
          const color = colors[index % colors.length];
          
          return {
            name: player.name,
            type: 'line',
            smooth: true,
            symbol: 'circle',
            symbolSize: 8,
            lineStyle: {
              width: 3,
              color: color.line
            },
            itemStyle: {
              color: color.line,
              borderWidth: 2,
              borderColor: '#fff'
            },
            data: generateRandomScores(10),
            areaStyle: {
              opacity: 0.3,
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: color.area[0] },
                { offset: 1, color: color.area[1] }
              ])
            }
          };
        })
      }
      charts.form.setOption(formOption)
    }
  } catch (error) {
    console.error('Error updating charts:', error)
  }
}

// Helper functions
const calculateBattingScore = (player) => {
  const avg = player.stats.batting.average
  const sr = player.stats.batting.strikeRate
  return Math.min(100, (avg * 0.6 + sr * 0.4))
}

const calculateBowlingScore = (player) => {
  const avg = player.stats.bowling.average
  const eco = player.stats.bowling.economy
  return Math.min(100, (100 - avg) * 0.6 + (10 - eco) * 10 * 0.4)
}

const generateRandomScores = (count) => {
  return Array.from({ length: count }, () => Math.floor(Math.random() * 100) + 20)
}

// Lifecycle hooks
onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  Object.values(charts).forEach(chart => {
    if (chart) {
      chart.dispose()
    }
  })
})

// Watch for player changes
watch(selectedPlayers, () => {
  initCharts()
}, { deep: true })

// Handle window resize
const handleResize = () => {
  Object.values(charts).forEach(chart => {
    if (chart) {
      chart.resize()
    }
  })
}
</script>

<style scoped>
.backdrop-blur-sm {
  backdrop-filter: blur(8px);
}

/* Add smooth transitions */
.group {
  transition: all 0.2s ease-in-out;
}

.group:hover {
  transform: translateY(-2px);
}
</style> 