<template>
  <div class="space-y-8">
    <!-- Officials Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Umpires -->
      <div class="stat-card">
        <h4 class="text-lg font-semibold mb-4 flex items-center space-x-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span>On-field Umpires</span>
        </h4>
        <div class="space-y-4">
          <div v-for="umpire in match.matchInfo.officials.umpires"
               :key="umpire.id"
               class="flex items-start space-x-3">
            <img :src="umpire.avatar || '/default-avatar.png'"
                 :alt="umpire.name"
                 class="w-10 h-10 rounded-full bg-slate-700">
            <div>
              <h5 class="font-medium">{{ umpire.name }}</h5>
              <p class="text-sm text-slate-400">{{ umpire.experience }} Years Experience</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Third Umpire -->
      <div class="stat-card">
        <h4 class="text-lg font-semibold mb-4 flex items-center space-x-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          <span>Third Umpire</span>
        </h4>
        <div class="flex items-start space-x-3">
          <img :src="match.matchInfo.officials.thirdUmpire.avatar || '/default-avatar.png'"
               :alt="match.matchInfo.officials.thirdUmpire.name"
               class="w-10 h-10 rounded-full bg-slate-700">
          <div>
            <h5 class="font-medium">{{ match.matchInfo.officials.thirdUmpire.name }}</h5>
            <p class="text-sm text-slate-400">{{ match.matchInfo.officials.thirdUmpire.experience }} Years Experience</p>
          </div>
        </div>
      </div>

      <!-- Match Referee -->
      <div class="stat-card">
        <h4 class="text-lg font-semibold mb-4 flex items-center space-x-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          <span>Match Referee</span>
        </h4>
        <div class="flex items-start space-x-3">
          <img :src="match.matchInfo.officials.matchReferee.avatar || '/default-avatar.png'"
               :alt="match.matchInfo.officials.matchReferee.name"
               class="w-10 h-10 rounded-full bg-slate-700">
          <div>
            <h5 class="font-medium">{{ match.matchInfo.officials.matchReferee.name }}</h5>
            <p class="text-sm text-slate-400">{{ match.matchInfo.officials.matchReferee.experience }} Years Experience</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Officials Stats -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Experience Chart -->
      <div class="stat-card">
        <h4 class="text-lg font-semibold mb-4">Officials Experience</h4>
        <div ref="experienceChart" class="h-64"></div>
      </div>

      <!-- Match History -->
      <div class="stat-card">
        <h4 class="text-lg font-semibold mb-4">Recent Matches</h4>
        <div class="space-y-4">
          <div v-for="match in recentMatches"
               :key="match.id"
               class="flex items-center justify-between p-3 rounded-lg bg-slate-800/50">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 rounded-lg bg-slate-700 flex items-center justify-center text-sm font-medium">
                {{ match.date }}
              </div>
              <div>
                <h6 class="font-medium">{{ match.teams }}</h6>
                <p class="text-sm text-slate-400">{{ match.venue }}</p>
              </div>
            </div>
            <span class="text-sm px-2 py-1 rounded-full"
                  :class="match.rating >= 4 ? 'bg-emerald-400/10 text-emerald-400' : 'bg-amber-400/10 text-amber-400'">
              {{ match.rating }}/5
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { echarts, chartConfig } from './chartConfig'

const props = defineProps({
  match: {
    type: Object,
    required: true
  }
})

const experienceChart = ref(null)
let chart = null

// Mock data for recent matches
const recentMatches = ref([
  {
    id: 1,
    date: '15 Mar',
    teams: 'IND vs AUS',
    venue: 'MCG',
    rating: 4.5
  },
  {
    id: 2,
    date: '12 Mar',
    teams: 'ENG vs SA',
    venue: 'Lords',
    rating: 4.2
  },
  {
    id: 3,
    date: '08 Mar',
    teams: 'NZ vs PAK',
    venue: 'Eden Park',
    rating: 3.8
  }
])

// Initialize experience chart
const initializeChart = () => {
  if (experienceChart.value) {
    chart = echarts.init(experienceChart.value)
    
    const officials = [
      ...props.match.matchInfo.officials.umpires,
      props.match.matchInfo.officials.thirdUmpire,
      props.match.matchInfo.officials.matchReferee
    ]

    const option = {
      ...chartConfig,
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: officials.map(o => o.name),
        axisLabel: {
          interval: 0,
          rotate: 45
        },
        ...chartConfig.axisStyle
      },
      yAxis: {
        type: 'value',
        name: 'Years',
        ...chartConfig.axisStyle
      },
      series: [
        {
          type: 'bar',
          data: officials.map(o => ({
            value: o.experience,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#6366f1' },
                { offset: 1, color: '#4338ca' }
              ])
            }
          }))
        }
      ]
    }
    chart.setOption(option)
  }
}

// Handle window resize
const handleResize = () => {
  if (chart) {
    chart.resize()
  }
}

onMounted(() => {
  initializeChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (chart) {
    chart.dispose()
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
@import './styles.css';
</style> 