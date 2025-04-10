<template>
  <div class="space-y-8">
    <!-- Team Tabs -->
    <div class="flex space-x-4 border-b border-slate-700">
      <button v-for="(innings, index) in match.scoreCard" 
              :key="innings.inningsId"
              @click="activeInnings = index"
              class="px-4 py-2 transition-colors relative"
              :class="activeInnings === index ? 'text-indigo-400 border-b-2 border-indigo-400' : 'text-slate-400 hover:text-slate-300'">
        {{ getTeamName(innings.batTeamDetails.batTeamId) }}
      </button>
    </div>

    <!-- Current Innings Analysis -->
    <div v-if="currentInnings">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Batting Summary Stats -->
        <div class="stat-card hover-card">
          <h4 class="text-lg font-semibold mb-4 text-slate-200">Batting Summary</h4>
          <div class="grid grid-cols-2 gap-4">
            <div class="p-3 bg-slate-700/30 rounded-lg border border-slate-700 transition-all hover:border-indigo-500/50 hover:bg-slate-700/50">
              <p class="text-sm text-slate-400">Total Runs</p>
              <p class="text-2xl font-bold text-indigo-400">{{ currentInnings.scoreDetails.runs }}</p>
            </div>
            <div class="p-3 bg-slate-700/30 rounded-lg border border-slate-700 transition-all hover:border-indigo-500/50 hover:bg-slate-700/50">
              <p class="text-sm text-slate-400">Run Rate</p>
              <p class="text-2xl font-bold text-indigo-400">{{ currentInnings.scoreDetails.runRate }}</p>
            </div>
            <div class="p-3 bg-slate-700/30 rounded-lg border border-slate-700 transition-all hover:border-indigo-500/50 hover:bg-slate-700/50">
              <p class="text-sm text-slate-400">Boundaries</p>
              <p class="text-2xl font-bold text-indigo-400">{{ totalBoundaries }}</p>
            </div>
            <div class="p-3 bg-slate-700/30 rounded-lg border border-slate-700 transition-all hover:border-indigo-500/50 hover:bg-slate-700/50">
              <p class="text-sm text-slate-400">Dot Ball %</p>
              <p class="text-2xl font-bold text-indigo-400">{{ dotBallPercentage }}%</p>
            </div>
          </div>
        </div>

        <!-- Top Performers -->
        <div class="stat-card hover-card">
          <h4 class="text-lg font-semibold mb-4 text-slate-200">Key Performers</h4>
          <div class="space-y-4">
            <div class="flex items-center p-3 bg-slate-700/30 rounded-lg border border-slate-700 transition-all hover:border-indigo-500/30 hover:shadow-glow">
              <div class="mr-3">
                <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${getBatterImage(topScorer.batId)}/i.jpg?p=thumb`"
                     :alt="topScorer.batName"
                     class="w-12 h-12 rounded-full border-2 border-indigo-500/50">
              </div>
              <div class="flex-1">
                <div class="flex justify-between items-center">
                  <p class="font-medium text-slate-200">{{ topScorer.batName }} <span class="text-xs text-indigo-400 ml-1 font-bold">Top Scorer</span></p>
                  <p class="font-bold text-xl text-indigo-400">{{ topScorer.runs }} <span class="text-sm text-slate-400">({{ topScorer.balls }})</span></p>
                </div>
                <div class="mt-1 text-sm text-slate-400">
                  <span class="text-slate-200">{{ topScorer.fours }}</span> fours, 
                  <span class="text-slate-200">{{ topScorer.sixes }}</span> sixes, 
                  SR: <span class="text-slate-200">{{ topScorer.strikeRate }}</span>
                </div>
              </div>
            </div>
            <div class="flex items-center p-3 bg-slate-700/30 rounded-lg border border-slate-700 transition-all hover:border-indigo-500/30 hover:shadow-glow">
              <div class="mr-3">
                <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${getBatterImage(highestStrikeRate.batId)}/i.jpg?p=thumb`"
                     :alt="highestStrikeRate.batName"
                     class="w-12 h-12 rounded-full border-2 border-indigo-500/50">
              </div>
              <div class="flex-1">
                <div class="flex justify-between items-center">
                  <p class="font-medium text-slate-200">{{ highestStrikeRate.batName }} <span class="text-xs text-indigo-400 ml-1 font-bold">Highest SR</span></p>
                  <p class="font-bold text-xl text-indigo-400">{{ highestStrikeRate.runs }} <span class="text-sm text-slate-400">({{ highestStrikeRate.balls }})</span></p>
                </div>
                <div class="mt-1 text-sm text-slate-400">
                  SR: <span class="text-slate-200">{{ highestStrikeRate.strikeRate }}</span>, 
                  <span class="text-slate-200">{{ highestStrikeRate.fours }}</span> fours, 
                  <span class="text-slate-200">{{ highestStrikeRate.sixes }}</span> sixes
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Run Distribution -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Shot Type Distribution -->
        <div class="stat-card hover-card">
          <h4 class="text-lg font-semibold mb-4 text-slate-200">Run Distribution</h4>
          <div ref="runDistributionChart" class="chart-container"></div>
        </div>

        <!-- Batting Position Impact -->
        <div class="stat-card hover-card">
          <h4 class="text-lg font-semibold mb-4 text-slate-200">Batting Position Impact</h4>
          <div ref="positionImpactChart" class="chart-container"></div>
        </div>
      </div>

      <!-- Batsmen Stats Table -->
      <div class="stat-card hover-card">
        <h4 class="text-lg font-semibold mb-4 text-slate-200">Batting Scorecard</h4>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="text-sm text-slate-400 border-b border-slate-700">
              <th class="text-left py-3">Batter</th>
              <th class="text-left py-3">Dismissal</th>
              <th class="text-right py-3">R</th>
              <th class="text-right py-3">B</th>
              <th class="text-right py-3">4s</th>
              <th class="text-right py-3">6s</th>
              <th class="text-right py-3">SR</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700">
              <tr v-for="batter in currentInnings.batTeamDetails.batsmenData" 
                :key="batter.batId"
                  class="transition-colors hover:bg-slate-700/60">
              <td class="py-3">
                <div class="flex items-center gap-3">
                  <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${getBatterImage(batter.batId)}/i.jpg?p=thumb`"
                       :alt="batter.batName"
                         class="w-8 h-8 rounded-full border border-slate-600">
                  <div>
                      <span class="font-medium text-slate-200">{{ batter.batName }}</span>
                      <span v-if="batter.isCaptain || batter.isKeeper" class="text-xs text-indigo-400 ml-1 font-bold">
                      {{ batter.isCaptain ? '(c)' : '' }}{{ batter.isKeeper ? '(wk)' : '' }}
                    </span>
                  </div>
                </div>
              </td>
              <td class="py-3 text-slate-400">{{ batter.outDesc || 'not out' }}</td>
                <td class="text-right py-3 font-medium text-slate-200">{{ batter.runs }}</td>
              <td class="text-right py-3">{{ batter.balls }}</td>
              <td class="text-right py-3">{{ batter.fours }}</td>
              <td class="text-right py-3">{{ batter.sixes }}</td>
                <td class="text-right py-3" :class="batter.strikeRate > 150 ? 'text-green-400' : batter.strikeRate > 100 ? 'text-indigo-400' : ''">
                  {{ batter.strikeRate }}
                </td>
            </tr>
          </tbody>
          <tfoot>
            <tr class="border-t border-slate-700 font-medium">
                <td class="py-3 text-slate-200">Extras</td>
              <td class="py-3 text-slate-400" colspan="6">
                  {{ formatExtras(currentInnings.extrasData) }}
              </td>
            </tr>
            <tr class="font-medium">
                <td class="py-3 text-slate-200">Total</td>
                <td class="py-3 text-slate-200" colspan="6">
                  {{ currentInnings.scoreDetails.runs }}/{{ currentInnings.scoreDetails.wickets }}
                  <span class="text-slate-400">({{ currentInnings.scoreDetails.overs }} Ov, RR: {{ currentInnings.scoreDetails.runRate }})</span>
              </td>
            </tr>
          </tfoot>
        </table>
        </div>
      </div>

      <!-- Partnerships -->
      <div class="stat-card hover-card mt-8">
        <h4 class="text-lg font-semibold mb-4 text-slate-200">Partnerships</h4>
        <div class="grid gap-4 md:grid-cols-2">
          <div v-for="(p, index) in currentInnings.partnershipsData" 
               :key="index"
               class="bg-slate-700/30 rounded-lg p-4 border border-slate-700 transition-all hover:border-indigo-500/30 hover:bg-slate-700/50">
            <div class="flex justify-between items-center mb-2">
              <div class="flex items-center gap-2">
                <span class="font-medium text-slate-200">{{ p.bat1Name }} - {{ p.bat2Name }}</span>
              </div>
              <span class="text-xl font-semibold text-indigo-400">{{ p.totalRuns }}</span>
            </div>
            <div class="text-sm text-slate-400">
              {{ p.totalBalls }} balls
            </div>
            <div class="mt-2 h-2 bg-slate-600 rounded-full overflow-hidden">
              <div class="h-full bg-gradient-to-r from-indigo-500 to-indigo-400"
                   :style="{ width: `${(p.totalRuns / getMaxPartnershipRuns(currentInnings)) * 100}%` }">
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Wagon Wheel -->
      <div v-if="wagonWheelData[currentInnings.inningsId]" class="stat-card hover-card mt-8">
        <h4 class="text-lg font-semibold mb-4 text-slate-200">Shot Distribution</h4>
        <WagonWheel :shots="wagonWheelData[currentInnings.inningsId]" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { echarts, chartConfig } from './chartConfig'
import WagonWheel from './WagonWheel.vue'

const props = defineProps({
  match: {
    type: Object,
    required: true
  }
})

// Active innings
const activeInnings = ref(0)

// Chart references
const runDistributionChart = ref(null)
const positionImpactChart = ref(null)

// Store chart instances
const charts = ref({
  runDistribution: null,
  positionImpact: null
})

// Current innings data
const currentInnings = computed(() => {
  if (!props.match.scoreCard || props.match.scoreCard.length === 0) {
    return null
  }
  return props.match.scoreCard[activeInnings.value]
})

// Batting analytics
const topScorer = computed(() => {
  if (!currentInnings.value) return {}
  
  const batsmen = currentInnings.value.batTeamDetails.batsmenData
  return batsmen.length 
    ? [...batsmen].sort((a, b) => b.runs - a.runs)[0] 
    : {}
})

const highestStrikeRate = computed(() => {
  if (!currentInnings.value) return {}
  
  const batsmen = currentInnings.value.batTeamDetails.batsmenData.filter(b => b.runs >= 20)
  return batsmen.length 
    ? [...batsmen].sort((a, b) => b.strikeRate - a.strikeRate)[0] 
    : topScorer.value
})

const totalBoundaries = computed(() => {
  if (!currentInnings.value) return 0
  
  return currentInnings.value.batTeamDetails.batsmenData.reduce(
    (sum, batter) => sum + batter.fours + batter.sixes, 0
  )
})

const dotBallPercentage = computed(() => {
  if (!currentInnings.value) return 0
  
  const totalDots = currentInnings.value.batTeamDetails.batsmenData.reduce(
    (sum, batter) => sum + batter.dots, 0
  )
  const totalBalls = currentInnings.value.scoreDetails.ballNbr || 120
  
  return Math.round((totalDots / totalBalls) * 100)
})

// Helper functions
const getTeamName = (teamId) => {
  const team = props.match.matchInfo.team1.id === teamId 
    ? props.match.matchInfo.team1 
    : props.match.matchInfo.team2
  return team.name
}

const getBatterImage = (batterId) => {
  const allPlayers = [
    ...props.match.squad?.team1?.players['playing XI'] || [],
    ...props.match.squad?.team1?.players?.bench || [],
    ...props.match.squad?.team2?.players['playing XI'] || [],
    ...props.match.squad?.team2?.players?.bench || []
  ]
  return allPlayers.find(p => p.id === batterId)?.faceImageId || ''
}

const formatExtras = (extras) => {
  if (!extras) return '0'
  
  const parts = []
  if (extras.byes) parts.push(`b ${extras.byes}`)
  if (extras.legByes) parts.push(`lb ${extras.legByes}`)
  if (extras.wides) parts.push(`w ${extras.wides}`)
  if (extras.noBalls) parts.push(`nb ${extras.noBalls}`)
  if (extras.penalty) parts.push(`p ${extras.penalty}`)
  return `${extras.total} (${parts.join(', ')})`
}

const getMaxPartnershipRuns = (innings) => {
  if (!innings || !innings.partnershipsData) return 0
  return Math.max(...innings.partnershipsData.map(p => p.totalRuns), 1)
}

// Wagon wheel data
const wagonWheelData = computed(() => {
  const data = {}
  if (props.match.scoreCard) {
  props.match.scoreCard.forEach(innings => {
    data[innings.inningsId] = innings.batTeamDetails.batsmenData
      .filter(batter => batter.runs > 0)
      .map(batter => ({
        // This is placeholder data - you'll need to get real shot data
        angle: Math.random() * 360,
        distance: 30 + Math.random() * 70,
        runs: batter.runs,
        type: batter.sixes > 0 ? 'SIX' : batter.fours > 0 ? 'FOUR' : 'OTHER'
      }))
  })
  }
  return data
})

// Initialize charts
const initializeCharts = () => {
  if (!currentInnings.value) return
  
  if (runDistributionChart.value) {
    charts.value.runDistribution = echarts.init(runDistributionChart.value)
    initializeRunDistributionChart()
  }
  
  if (positionImpactChart.value) {
    charts.value.positionImpact = echarts.init(positionImpactChart.value)
    initializePositionImpactChart()
  }
}

// Initialize run distribution chart
const initializeRunDistributionChart = () => {
  if (!currentInnings.value) return
  
  const batsmen = currentInnings.value.batTeamDetails.batsmenData
  const totalRuns = currentInnings.value.scoreDetails.runs
  
  const singlesPercentage = Math.round(
    batsmen.reduce((sum, b) => sum + b.ones, 0) / totalRuns * 100
  )
  
  const twosPercentage = Math.round(
    batsmen.reduce((sum, b) => sum + b.twos * 2, 0) / totalRuns * 100
  )
  
  const foursPercentage = Math.round(
    batsmen.reduce((sum, b) => sum + b.fours * 4, 0) / totalRuns * 100
  )
  
  const sixesPercentage = Math.round(
    batsmen.reduce((sum, b) => sum + b.sixes * 6, 0) / totalRuns * 100
  )
  
  // Calculate extras and other runs
  const extrasPercentage = Math.round(currentInnings.value.extrasData.total / totalRuns * 100)
  const otherPercentage = 100 - singlesPercentage - twosPercentage - foursPercentage - sixesPercentage - extrasPercentage
  
  const option = {
    ...chartConfig,
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: { color: '#94a3b8' }
    },
    series: [
      {
        name: 'Run Distribution',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#1e293b',
          borderWidth: 2
        },
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '18',
            fontWeight: 'bold',
            color: '#94a3b8'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: singlesPercentage, name: 'Singles', itemStyle: { color: '#6366f1' } },
          { value: twosPercentage, name: 'Twos', itemStyle: { color: '#ec4899' } },
          { value: foursPercentage, name: 'Fours', itemStyle: { color: '#10b981' } },
          { value: sixesPercentage, name: 'Sixes', itemStyle: { color: '#f59e0b' } },
          { value: extrasPercentage, name: 'Extras', itemStyle: { color: '#8b5cf6' } },
          { value: otherPercentage, name: 'Other', itemStyle: { color: '#64748b' } }
        ]
      }
    ]
  }
  
  charts.value.runDistribution.setOption(option)
}

// Initialize position impact chart
const initializePositionImpactChart = () => {
  if (!currentInnings.value) return
  
  const batsmen = currentInnings.value.batTeamDetails.batsmenData
  // Group batsmen into positions (top, middle, lower)
  const topOrder = batsmen.slice(0, 3)
  const middleOrder = batsmen.slice(3, 6)
  const lowerOrder = batsmen.slice(6)
  
  const topOrderRuns = topOrder.reduce((sum, b) => sum + b.runs, 0)
  const middleOrderRuns = middleOrder.reduce((sum, b) => sum + b.runs, 0)
  const lowerOrderRuns = lowerOrder.reduce((sum, b) => sum + b.runs, 0)
  
  const topOrderBalls = topOrder.reduce((sum, b) => sum + b.balls, 0)
  const middleOrderBalls = middleOrder.reduce((sum, b) => sum + b.balls, 0)
  const lowerOrderBalls = lowerOrder.reduce((sum, b) => sum + b.balls, 0)
  
  const option = {
    ...chartConfig,
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['Runs', 'Balls Faced'],
      textStyle: { color: '#94a3b8' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: [
      {
        type: 'category',
        data: ['Top Order (1-3)', 'Middle Order (4-6)', 'Lower Order (7+)'],
        axisTick: {
          alignWithLabel: true
        },
        ...chartConfig.axisStyle
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: 'Runs / Balls',
        ...chartConfig.axisStyle
      }
    ],
    series: [
      {
        name: 'Runs',
        type: 'bar',
        barWidth: '40%',
        data: [
          {
            value: topOrderRuns,
            itemStyle: { color: '#6366f1' }
          },
          {
            value: middleOrderRuns,
            itemStyle: { color: '#ec4899' }
          },
          {
            value: lowerOrderRuns,
            itemStyle: { color: '#10b981' }
          }
        ]
      },
      {
        name: 'Balls Faced',
        type: 'bar',
        barWidth: '40%',
        data: [
          {
            value: topOrderBalls,
            itemStyle: { color: '#94a3b8' }
          },
          {
            value: middleOrderBalls,
            itemStyle: { color: '#94a3b8' }
          },
          {
            value: lowerOrderBalls,
            itemStyle: { color: '#94a3b8' }
          }
        ]
      }
    ]
  }
  
  charts.value.positionImpact.setOption(option)
}

// Handle window resize
const handleResize = () => {
  Object.values(charts.value).forEach(chart => {
    if (chart) {
      chart.resize()
    }
  })
}

// Cleanup function
const cleanup = () => {
  Object.values(charts.value).forEach(chart => {
    if (chart) {
      chart.dispose()
    }
  })
  charts.value = {}
}

// Watch for changes
watch([() => props.match, activeInnings], () => {
  cleanup()
  initializeCharts()
}, { deep: true })

onMounted(() => {
  initializeCharts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  cleanup()
  window.removeEventListener('resize', handleResize)
})
</script> 

<style scoped>
.chart-container {
  height: 300px;
  width: 100%;
}
.stat-card {
  @apply bg-slate-800 rounded-lg p-6 border border-slate-700/50 transition-all;
}
.hover-card {
  @apply hover:border-indigo-500/20 hover:shadow-md;
}
.hover-card:hover {
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
}
.shadow-glow {
  box-shadow: 0 0 15px rgba(99, 102, 241, 0.15);
}
</style> 