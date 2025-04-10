<template>
  <div class="space-y-8">
    <!-- Team Tabs -->
    <div class="flex space-x-4 border-b border-slate-700">
      <button v-for="(tab, index) in innings" 
              :key="index"
              @click="activeInnings = index"
              class="px-4 py-2 transition-colors relative"
              :class="activeInnings === index ? 'text-indigo-400 border-b-2 border-indigo-400' : 'text-slate-400 hover:text-slate-300'">
        {{ getTeamName(tab.batTeamDetails.batTeamName) }}
      </button>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Partnership Timeline -->
      <div class="stat-card">
        <h4 class="text-lg font-semibold mb-4">Partnership Timeline</h4>
        <div ref="partnershipTimelineChart" class="chart-container"></div>
      </div>

      <!-- Partnership Distribution -->
      <div class="stat-card">
        <h4 class="text-lg font-semibold mb-4">Partnership Distribution</h4>
        <div ref="partnershipChart" class="chart-container"></div>
      </div>

      <!-- Partnership Runs Flow -->
      <div class="stat-card">
        <h4 class="text-lg font-semibold mb-4">Partnership Runs Flow</h4>
        <div ref="partnershipRunsChart" class="chart-container"></div>
      </div>

      <!-- Partnership Summary -->
      <div class="stat-card">
        <h4 class="text-lg font-semibold mb-4">Partnership Summary</h4>
        <div class="space-y-4">
          <div v-for="(partnership, index) in currentPartnerships" :key="index"
               class="flex items-center justify-between p-3 bg-dark-800/50 rounded-lg">
            <div>
              <p class="font-medium">{{ getPartnershipPlayers(partnership) }}</p>
              <p class="text-sm text-gray-400">{{ getWicketNumber(index + 1) }} wicket</p>
            </div>
            <div class="text-right">
              <p class="font-bold text-lg">{{ partnership.totalRuns }} runs</p>
              <p class="text-sm text-gray-400">{{ partnership.totalBalls }} balls</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { echarts, chartConfig } from './chartConfig'

const props = defineProps({
  match: {
    type: Object,
    required: true
  }
})

// Active innings
const activeInnings = ref(0)

// Chart references
const partnershipTimelineChart = ref(null)
const partnershipChart = ref(null)
const partnershipRunsChart = ref(null)

// Store chart instances
const charts = ref({
  partnershipTimeline: null,
  partnership: null,
  partnershipRuns: null
})

// Get innings data
const innings = computed(() => {
  return props.match.scoreCard || []
})

// Get current partnerships data
const currentPartnerships = computed(() => {
  if (!innings.value || innings.value.length === 0 || activeInnings.value >= innings.value.length) {
    return []
  }
  return innings.value[activeInnings.value].partnershipsData || []
})

// Helper functions
const getTeamName = (teamName) => {
  return teamName || 'Team'
}

const getPartnershipPlayers = (partnership) => {
  return `${partnership.bat1Name || 'Player 1'} & ${partnership.bat2Name || 'Player 2'}`
}

const getWicketNumber = (index) => {
  return `${index}${getSuffix(index)}`
}

const getSuffix = (num) => {
  const lastDigit = num % 10
  const lastTwoDigits = num % 100
  
  if (lastTwoDigits >= 11 && lastTwoDigits <= 13) {
    return 'th'
  }
  
  switch (lastDigit) {
    case 1: return 'st'
    case 2: return 'nd'
    case 3: return 'rd'
    default: return 'th'
  }
}

// Initialize charts
const initializeCharts = () => {
  if (partnershipTimelineChart.value) {
    charts.value.partnershipTimeline = echarts.init(partnershipTimelineChart.value)
    initializePartnershipTimelineChart()
  }
  if (partnershipChart.value) {
    charts.value.partnership = echarts.init(partnershipChart.value)
    initializePartnershipChart()
  }
  if (partnershipRunsChart.value) {
    charts.value.partnershipRuns = echarts.init(partnershipRunsChart.value)
    initializePartnershipRunsChart()
  }
}

// Chart initialization functions
const initializePartnershipTimelineChart = () => {
  if (!currentPartnerships.value.length) return

  const partnerships = currentPartnerships.value
  const wickets = partnerships.map((_, index) => `${index + 1}${getSuffix(index + 1)}`)
  const runsData = partnerships.map(p => p.totalRuns)
  const ballsData = partnerships.map(p => p.totalBalls)

  const option = {
    ...chartConfig,
    legend: {
      data: ['Runs', 'Balls'],
      textStyle: { color: '#94a3b8' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: wickets,
      ...chartConfig.axisStyle
    },
    yAxis: [
      {
        type: 'value',
        name: 'Runs',
        position: 'left',
        ...chartConfig.axisStyle
      },
      {
        type: 'value',
        name: 'Balls',
        position: 'right',
        ...chartConfig.axisStyle,
        splitLine: { show: false }
      }
    ],
    series: [
      {
        name: 'Runs',
        type: 'bar',
        data: runsData,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#6366f1' },
            { offset: 1, color: '#4338ca' }
          ])
        }
      },
      {
        name: 'Balls',
        type: 'line',
        yAxisIndex: 1,
        data: ballsData,
        lineStyle: { width: 3 },
        itemStyle: { color: '#ec4899' },
        symbol: 'circle',
        symbolSize: 8
      }
    ]
  }
  charts.value.partnershipTimeline.setOption(option)
}

const initializePartnershipChart = () => {
  if (!currentPartnerships.value.length) return

  const partnerships = currentPartnerships.value
  const pieData = partnerships.map((p, index) => ({
    value: p.totalRuns,
    name: `${index + 1}${getSuffix(index + 1)} Wicket`,
    itemStyle: { 
      color: getChartColor(index) 
    }
  }))

  const option = {
    ...chartConfig,
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: { color: '#94a3b8' }
    },
    series: [
      {
        name: 'Partnership',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#1e293b',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
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
        data: pieData
      }
    ]
  }
  charts.value.partnership.setOption(option)
}

const initializePartnershipRunsChart = () => {
  if (!currentPartnerships.value.length) return

  const partnerships = currentPartnerships.value
  const wickets = partnerships.map((_, index) => `${index + 1}${getSuffix(index + 1)}`)
  
  // Mock data for run types - in real implementation you would extract this data from the match
  const singlesData = partnerships.map(() => Math.floor(Math.random() * 15) + 5)
  const doublesData = partnerships.map(() => Math.floor(Math.random() * 8) + 2)
  const boundariesData = partnerships.map(p => Math.min(Math.floor(p.totalRuns * 0.4), p.totalRuns))
  const extrasData = partnerships.map(() => Math.floor(Math.random() * 5))
  
  // Ensure data consistency
  partnerships.forEach((p, i) => {
    const total = singlesData[i] + doublesData[i] * 2 + boundariesData[i] + extrasData[i]
    if (total > p.totalRuns) {
      // Adjust to match actual total
      const diff = total - p.totalRuns
      singlesData[i] = Math.max(0, singlesData[i] - diff)
    }
  })

  const option = {
    ...chartConfig,
    legend: {
      data: ['Singles', 'Doubles', 'Boundaries', 'Extras'],
      textStyle: { color: '#94a3b8' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: wickets,
      ...chartConfig.axisStyle
    },
    yAxis: {
      type: 'value',
      name: 'Runs',
      ...chartConfig.axisStyle
    },
    series: [
      {
        name: 'Singles',
        type: 'bar',
        stack: 'total',
        emphasis: { focus: 'series' },
        data: singlesData,
        itemStyle: { color: '#6366f1' }
      },
      {
        name: 'Doubles',
        type: 'bar',
        stack: 'total',
        emphasis: { focus: 'series' },
        data: doublesData,
        itemStyle: { color: '#ec4899' }
      },
      {
        name: 'Boundaries',
        type: 'bar',
        stack: 'total',
        emphasis: { focus: 'series' },
        data: boundariesData,
        itemStyle: { color: '#10b981' }
      },
      {
        name: 'Extras',
        type: 'bar',
        stack: 'total',
        emphasis: { focus: 'series' },
        data: extrasData,
        itemStyle: { color: '#f59e0b' }
      }
    ]
  }
  charts.value.partnershipRuns.setOption(option)
}

// Color utility function
const getChartColor = (index) => {
  const colors = ['#6366f1', '#ec4899', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4', '#f97316', '#14b8a6']
  return colors[index % colors.length]
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
  window.removeEventListener('resize', handleResize)
}

// Watch for match data changes or active innings changes
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
})
</script>

<style scoped>
.chart-container {
  height: 300px;
  width: 100%;
}
.stat-card {
  @apply bg-slate-800 rounded-lg p-6;
}
</style> 