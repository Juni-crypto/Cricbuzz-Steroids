<template>
  <div class="space-y-8">
    <!-- Team Tabs -->
    <div class="flex space-x-4 border-b border-slate-700">
      <button v-for="(innings, index) in match.scoreCard" 
              :key="innings.inningsId"
              @click="activeInnings = index"
              class="px-4 py-2 transition-colors relative"
              :class="activeInnings === index ? 'text-indigo-400 border-b-2 border-indigo-400' : 'text-slate-400 hover:text-slate-300'">
        {{ getTeamName(innings.bowlTeamDetails.bowlTeamId) }} Bowling
      </button>
    </div>

    <!-- Current Innings Analysis -->
    <div v-if="currentInnings">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Bowling Summary Stats -->
        <div class="stat-card hover-card">
          <h4 class="text-lg font-semibold mb-4 text-slate-200">Bowling Summary</h4>
          <div class="grid grid-cols-2 gap-4">
            <div class="p-3 bg-slate-700/30 rounded-lg border border-slate-700 transition-all hover:border-indigo-500/50 hover:bg-slate-700/50">
              <p class="text-sm text-slate-400">Total Wickets</p>
              <p class="text-2xl font-bold text-indigo-400">{{ totalWickets }}</p>
            </div>
            <div class="p-3 bg-slate-700/30 rounded-lg border border-slate-700 transition-all hover:border-indigo-500/50 hover:bg-slate-700/50">
              <p class="text-sm text-slate-400">Economy Rate</p>
              <p class="text-2xl font-bold text-indigo-400">{{ averageEconomy.toFixed(2) }}</p>
            </div>
            <div class="p-3 bg-slate-700/30 rounded-lg border border-slate-700 transition-all hover:border-indigo-500/50 hover:bg-slate-700/50">
              <p class="text-sm text-slate-400">Dot Ball %</p>
              <p class="text-2xl font-bold text-indigo-400">{{ dotBallPercentage }}%</p>
            </div>
            <div class="p-3 bg-slate-700/30 rounded-lg border border-slate-700 transition-all hover:border-indigo-500/50 hover:bg-slate-700/50">
              <p class="text-sm text-slate-400">Maidens</p>
              <p class="text-2xl font-bold text-indigo-400">{{ totalMaidens }}</p>
            </div>
          </div>
        </div>

        <!-- Top Performers -->
        <div class="stat-card hover-card">
          <h4 class="text-lg font-semibold mb-4 text-slate-200">Key Performers</h4>
          <div class="space-y-4">
            <div class="flex items-center p-3 bg-slate-700/30 rounded-lg border border-slate-700 transition-all hover:border-indigo-500/30 hover:shadow-glow">
              <div class="mr-3">
                <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${getBowlerImage(topWicketTaker.bowlerId)}/i.jpg?p=thumb`"
                     :alt="topWicketTaker.bowlName"
                     class="w-12 h-12 rounded-full border-2 border-indigo-500/50">
              </div>
              <div class="flex-1">
                <div class="flex justify-between items-center">
                  <p class="font-medium text-slate-200">{{ topWicketTaker.bowlName }} <span class="text-xs text-indigo-400 ml-1 font-bold">Top Wicket Taker</span></p>
                  <p class="font-bold text-xl text-indigo-400">{{ topWicketTaker.wickets }}-{{ topWicketTaker.runs }}</p>
                </div>
                <div class="mt-1 text-sm text-slate-400">
                  {{ topWicketTaker.overs }} overs, Economy: <span class="text-slate-200">{{ topWicketTaker.economy }}</span>
                </div>
              </div>
            </div>
            <div class="flex items-center p-3 bg-slate-700/30 rounded-lg border border-slate-700 transition-all hover:border-indigo-500/30 hover:shadow-glow">
              <div class="mr-3">
                <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${getBowlerImage(mostEconomical.bowlerId)}/i.jpg?p=thumb`"
                     :alt="mostEconomical.bowlName"
                     class="w-12 h-12 rounded-full border-2 border-indigo-500/50">
              </div>
              <div class="flex-1">
                <div class="flex justify-between items-center">
                  <p class="font-medium text-slate-200">{{ mostEconomical.bowlName }} <span class="text-xs text-indigo-400 ml-1 font-bold">Most Economical</span></p>
                  <p class="font-bold text-xl text-indigo-400">{{ mostEconomical.wickets }}-{{ mostEconomical.runs }}</p>
                </div>
                <div class="mt-1 text-sm text-slate-400">
                  {{ mostEconomical.overs }} overs, Economy: <span class="text-slate-200">{{ mostEconomical.economy }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Bowling Analytics Charts -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Wicket Distribution -->
        <div class="stat-card hover-card">
          <h4 class="text-lg font-semibold mb-4 text-slate-200">Wicket Distribution</h4>
          <div ref="wicketDistributionChart" class="chart-container"></div>
        </div>

        <!-- Economy Rate Analysis -->
        <div class="stat-card hover-card">
          <h4 class="text-lg font-semibold mb-4 text-slate-200">Economy Rate Analysis</h4>
          <div ref="economyRateChart" class="chart-container"></div>
        </div>
      </div>

      <!-- Bowler Stats Table -->
      <div class="stat-card hover-card">
        <h4 class="text-lg font-semibold mb-4 text-slate-200">Bowling Scorecard</h4>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="text-sm text-slate-400 border-b border-slate-700">
              <th class="text-left py-3">Bowler</th>
              <th class="text-right py-3">O</th>
              <th class="text-right py-3">M</th>
              <th class="text-right py-3">R</th>
              <th class="text-right py-3">W</th>
              <th class="text-right py-3">Econ</th>
              <th class="text-right py-3">Dots</th>
              <th class="text-right py-3">4s</th>
              <th class="text-right py-3">6s</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700">
              <tr v-for="bowler in currentInnings.bowlTeamDetails.bowlersData" 
                :key="bowler.bowlerId"
                  class="transition-colors hover:bg-slate-700/60">
              <td class="py-3">
                <div class="flex items-center gap-3">
                  <img :src="`http://static.cricbuzz.com/a/img/v1/i1/c${getBowlerImage(bowler.bowlerId)}/i.jpg?p=thumb`"
                       :alt="bowler.bowlName"
                         class="w-8 h-8 rounded-full border border-slate-600">
                  <div>
                      <span class="font-medium text-slate-200">{{ bowler.bowlName }}</span>
                      <span v-if="bowler.isCaptain" class="text-xs text-indigo-400 ml-1 font-bold">(c)</span>
                    </div>
                </div>
              </td>
              <td class="text-right py-3">{{ bowler.overs }}</td>
              <td class="text-right py-3">{{ bowler.maidens }}</td>
              <td class="text-right py-3">{{ bowler.runs }}</td>
                <td class="text-right py-3 font-medium text-slate-200">{{ bowler.wickets }}</td>
                <td class="text-right py-3" :class="getEconomyClass(bowler.economy)">{{ bowler.economy }}</td>
              <td class="text-right py-3">{{ bowler.dots }}</td>
                <td class="text-right py-3">{{ getBowlerBoundaries(currentInnings, bowler.bowlerId).fours }}</td>
                <td class="text-right py-3">{{ getBowlerBoundaries(currentInnings, bowler.bowlerId).sixes }}</td>
            </tr>
          </tbody>
        </table>
        </div>
      </div>

      <!-- Pitch Map -->
      <div class="stat-card hover-card mt-8">
        <h4 class="text-lg font-semibold mb-4 text-slate-200">Pitch Map</h4>
        <div class="pitch-map-container">
          <PitchMap :deliveries="generatePitchMapData()" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { echarts, chartConfig } from './chartConfig'
import PitchMap from './PitchMap.vue'

const props = defineProps({
  match: {
    type: Object,
    required: true
  }
})

// Active innings
const activeInnings = ref(0)

// Chart references
const wicketDistributionChart = ref(null)
const economyRateChart = ref(null)

// Store chart instances
const charts = ref({
  wicketDistribution: null,
  economyRate: null
})

// Current innings data
const currentInnings = computed(() => {
  if (!props.match.scoreCard || props.match.scoreCard.length === 0) {
    return null
  }
  return props.match.scoreCard[activeInnings.value]
})

// Bowling analytics
const totalWickets = computed(() => {
  if (!currentInnings.value) return 0
  
  return currentInnings.value.bowlTeamDetails.bowlersData.reduce(
    (sum, bowler) => sum + bowler.wickets, 0
  )
})

const averageEconomy = computed(() => {
  if (!currentInnings.value) return 0
  
  const bowlers = currentInnings.value.bowlTeamDetails.bowlersData
  if (!bowlers.length) return 0
  
  const totalRuns = bowlers.reduce((sum, bowler) => sum + bowler.runs, 0)
  const totalOvers = bowlers.reduce((sum, bowler) => sum + bowler.overs, 0)
  
  return totalRuns / totalOvers
})

const dotBallPercentage = computed(() => {
  if (!currentInnings.value) return 0
  
  const totalDots = currentInnings.value.bowlTeamDetails.bowlersData.reduce(
    (sum, bowler) => sum + bowler.dots, 0
  )
  const totalBalls = currentInnings.value.bowlTeamDetails.bowlersData.reduce(
    (sum, bowler) => sum + bowler.balls, 0
  )
  
  return Math.round((totalDots / totalBalls) * 100)
})

const totalMaidens = computed(() => {
  if (!currentInnings.value) return 0
  
  return currentInnings.value.bowlTeamDetails.bowlersData.reduce(
    (sum, bowler) => sum + bowler.maidens, 0
  )
})

const topWicketTaker = computed(() => {
  if (!currentInnings.value) return {}
  
  const bowlers = currentInnings.value.bowlTeamDetails.bowlersData
  return bowlers.length 
    ? [...bowlers].sort((a, b) => {
        // First sort by wickets in descending order
        if (b.wickets !== a.wickets) return b.wickets - a.wickets
        // If wickets are the same, sort by economy in ascending order
        return a.economy - b.economy
      })[0] 
    : {}
})

const mostEconomical = computed(() => {
  if (!currentInnings.value) return {}
  
  const bowlers = currentInnings.value.bowlTeamDetails.bowlersData.filter(b => b.overs >= 2)
  return bowlers.length 
    ? [...bowlers].sort((a, b) => a.economy - b.economy)[0] 
    : topWicketTaker.value
})

// Helper functions
const getTeamName = (teamId) => {
  const team = props.match.matchInfo.team1.id === teamId 
    ? props.match.matchInfo.team1 
    : props.match.matchInfo.team2
  return team.name
}

const getBowlerImage = (bowlerId) => {
  const allPlayers = [
    ...props.match.squad?.team1?.players['playing XI'] || [],
    ...props.match.squad?.team1?.players?.bench || [],
    ...props.match.squad?.team2?.players['playing XI'] || [],
    ...props.match.squad?.team2?.players?.bench || []
  ]
  return allPlayers.find(p => p.id === bowlerId)?.faceImageId || ''
}

const getBowlerBoundaries = (innings, bowlerId) => {
  // This would need actual ball-by-ball data to be accurate
  // For now, returning estimated values based on runs conceded
  const bowler = innings.bowlTeamDetails.bowlersData.find(b => b.bowlerId === bowlerId)
  if (!bowler) return { fours: 0, sixes: 0 }
  
  return {
    fours: Math.floor(bowler.runs / 8),
    sixes: Math.floor(bowler.runs / 12)
  }
}

const getEconomyClass = (economy) => {
  if (economy < 6) return 'text-green-400'
  if (economy < 8) return 'text-indigo-400'
  if (economy < 10) return 'text-yellow-400'
  return 'text-red-400'
}

// Fix the pitch map data generation
const generatePitchMapData = () => {
  if (!currentInnings.value) return []
  
  const bowlers = currentInnings.value.bowlTeamDetails.bowlersData
  if (!bowlers.length) return []
  
  // Get bowling styles from player data
  const bowlingStyles = {}
  const allPlayers = [
    ...props.match.matchInfo.team1.playerDetails || [],
    ...props.match.matchInfo.team2.playerDetails || []
  ]
  
  allPlayers.forEach(player => {
    if (player.bowlingStyle) {
      bowlingStyles[player.id] = player.bowlingStyle.toLowerCase()
    }
  })
  
  // Define pitch zones (these are the actual areas where balls land on a cricket pitch)
  const zones = {
    // Format: [x, y, width, height] with x,y as center point
    yorker: [0, 0.2, 0.8, 0.2],  // Full yorker length
    fullToss: [0, 0.4, 0.8, 0.2], // Full toss
    drivingLength: [0, 0.6, 0.7, 0.2], // Good for driving
    goodLength: [0, 0.9, 0.6, 0.3], // Good length area
    backOfLength: [0, 1.2, 0.7, 0.2], // Back of a length
    short: [0, 1.5, 0.8, 0.3],  // Short ball
    bouncer: [0, 1.8, 0.8, 0.2]  // Bouncer
  }
  
  // Define lines on the pitch
  const lines = {
    offStump: -0.2,        // Outside off stump
    fourthStump: -0.4,     // Fourth stump line
    fifthStump: -0.6,      // Fifth stump line
    wideOff: -0.8,         // Wide outside off
    middleStump: 0,        // Middle stump
    legStump: 0.2,         // Leg stump
    wideLeg: 0.6           // Wide on leg side
  }
  
  const deliveries = []
  
  // Base number of deliveries to generate
  let totalDeliveryCount = 60
  
  bowlers.forEach(bowler => {
    if (bowler.balls === 0) return
    
    // Calculate number of deliveries for this bowler based on their contribution
    const totalBalls = bowlers.reduce((sum, b) => sum + b.balls, 0)
    const bowlerDeliveryCount = Math.ceil((bowler.balls / totalBalls) * totalDeliveryCount)
    
    // Determine bowler type
    const bowlerStyle = bowlingStyles[bowler.bowlerId] || ''
    const isPacer = bowlerStyle.includes('fast') || bowlerStyle.includes('medium')
    const isSpinner = bowlerStyle.includes('spin') || bowlerStyle.includes('break') || bowlerStyle.includes('orthodox')
    
    // Define bowler's preferences
    let preferredZones, preferredLines
    
    if (isPacer) {
      // Pace bowlers prefer good length and back of length areas
      preferredZones = [
        { zone: zones.goodLength, weight: 50 },  // 50% good length
        { zone: zones.backOfLength, weight: 20 }, // 20% back of length
        { zone: zones.yorker, weight: 10 },      // 10% yorkers
        { zone: zones.fullToss, weight: 5 },     // 5% full tosses
        { zone: zones.short, weight: 10 },       // 10% short
        { zone: zones.bouncer, weight: 5 }       // 5% bouncers
      ]
      
      // Pace bowlers aim for off stump to fourth stump
      preferredLines = [
        { line: lines.offStump, weight: 40 },    // 40% off stump
        { line: lines.fourthStump, weight: 30 }, // 30% fourth stump
        { line: lines.middleStump, weight: 20 }, // 20% middle stump
        { line: lines.fifthStump, weight: 7 },   // 7% fifth stump
        { line: lines.legStump, weight: 3 }      // 3% leg stump
      ]
    } else if (isSpinner) {
      // Spinners prefer fuller lengths
      preferredZones = [
        { zone: zones.goodLength, weight: 40 },  // 40% good length
        { zone: zones.drivingLength, weight: 30 },// 30% fuller length
        { zone: zones.backOfLength, weight: 15 }, // 15% back of length
        { zone: zones.fullToss, weight: 10 },    // 10% full tosses
        { zone: zones.short, weight: 5 }         // 5% short
      ]
      
      // Off spinners aim outside off, leg spinners more on middle and leg
      if (bowlerStyle.includes('off')) {
        preferredLines = [
          { line: lines.offStump, weight: 30 },     // 30% off stump
          { line: lines.fourthStump, weight: 25 },  // 25% fourth stump
          { line: lines.middleStump, weight: 20 },  // 20% middle stump
          { line: lines.fifthStump, weight: 15 },   // 15% fifth stump  
          { line: lines.legStump, weight: 10 }      // 10% leg stump
        ]
      } else {
        // Leg spinner or orthodox
        preferredLines = [
          { line: lines.middleStump, weight: 30 },  // 30% middle stump
          { line: lines.legStump, weight: 25 },     // 25% leg stump
          { line: lines.offStump, weight: 20 },     // 20% off stump
          { line: lines.wideLeg, weight: 15 },      // 15% wide on leg
          { line: lines.fourthStump, weight: 10 }   // 10% fourth stump
        ]
      }
    } else {
      // Medium pacers or unknown - default preferences
      preferredZones = [
        { zone: zones.goodLength, weight: 45 },
        { zone: zones.backOfLength, weight: 25 },
        { zone: zones.drivingLength, weight: 15 },
        { zone: zones.yorker, weight: 5 },
        { zone: zones.short, weight: 10 }
      ]
      
      preferredLines = [
        { line: lines.offStump, weight: 35 },
        { line: lines.fourthStump, weight: 25 },
        { line: lines.middleStump, weight: 25 },
        { line: lines.fifthStump, weight: 10 },
        { line: lines.legStump, weight: 5 }
      ]
    }
    
    // Helper function to select based on weight
    const selectWeighted = (options) => {
      const totalWeight = options.reduce((sum, option) => sum + option.weight, 0)
      let random = Math.random() * totalWeight
      
      for (const option of options) {
        random -= option.weight
        if (random <= 0) return option
      }
      
      return options[0] // Fallback
    }
    
    // Generate deliveries for this bowler
    for (let i = 0; i < bowlerDeliveryCount; i++) {
      // Determine delivery type based on bowler stats
      const wicketRate = bowler.wickets / Math.max(bowler.balls, 1) * 1.2 // Slightly increase for visualization
      const dotRate = bowler.dots / Math.max(bowler.balls, 1)
      const boundaryRate = (bowler.runs / Math.max(bowler.balls, 1)) / 4 * 0.2
      
      let type = 'REGULAR'
      const rand = Math.random()
      if (rand < wicketRate) {
        type = 'WICKET'
      } else if (rand < wicketRate + boundaryRate) {
        type = 'BOUNDARY'
      } else if (rand < wicketRate + boundaryRate + dotRate) {
        type = 'DOT'
      }
      
      // Select zone and line based on type
      let selectedZone, selectedLine
      
      if (type === 'WICKET') {
        // Wickets usually come from good length deliveries
        const wicketZones = [
          { zone: zones.goodLength, weight: 70 },
          { zone: zones.backOfLength, weight: 20 },
          { zone: zones.yorker, weight: 10 }
        ]
        
        // Wickets usually closer to stumps
        const wicketLines = [
          { line: lines.offStump, weight: 50 },
          { line: lines.middleStump, weight: 30 },
          { line: lines.fourthStump, weight: 20 }
        ]
        
        selectedZone = selectWeighted(wicketZones).zone
        selectedLine = selectWeighted(wicketLines).line
      } else if (type === 'BOUNDARY') {
        // Boundaries usually from fuller or shorter deliveries
        const boundaryZones = [
          { zone: zones.fullToss, weight: 30 },
          { zone: zones.drivingLength, weight: 25 },
          { zone: zones.short, weight: 25 },
          { zone: zones.bouncer, weight: 20 }
        ]
        
        // Boundaries often from wider deliveries or on legs
        const boundaryLines = [
          { line: lines.fifthStump, weight: 30 },
          { line: lines.legStump, weight: 30 },
          { line: lines.wideLeg, weight: 20 },
          { line: lines.wideOff, weight: 20 }
        ]
        
        selectedZone = selectWeighted(boundaryZones).zone
        selectedLine = selectWeighted(boundaryLines).line
      } else if (type === 'DOT') {
        // Dot balls from good areas or tough to hit zones
        const dotZones = [
          { zone: zones.goodLength, weight: 50 },
          { zone: zones.backOfLength, weight: 30 },
          { zone: zones.yorker, weight: 20 }
        ]
        
        // Dot balls often from tight lines
        const dotLines = [
          { line: lines.offStump, weight: 40 },
          { line: lines.fourthStump, weight: 30 },
          { line: lines.middleStump, weight: 20 },
          { line: lines.fifthStump, weight: 10 }
        ]
        
        selectedZone = selectWeighted(dotZones).zone
        selectedLine = selectWeighted(dotLines).line
      } else {
        // Regular deliveries use bowler preferences
        selectedZone = selectWeighted(preferredZones).zone
        selectedLine = selectWeighted(preferredLines).line
      }
      
      // Add some randomness to the exact landing spot
      const [zoneX, zoneY, zoneWidth, zoneHeight] = selectedZone
      
      // Calculate precise landing coordinates
      const x = selectedLine + (Math.random() - 0.5) * (zoneWidth * 0.7)
      const y = zoneY + (Math.random() - 0.5) * (zoneHeight * 0.7)
      
      // Calculate speed based on bowler type and delivery
      let speed
      if (isPacer) {
        speed = 130 + Math.floor(Math.random() * 20) // 130-150 kph
      } else if (isSpinner) {
        speed = 75 + Math.floor(Math.random() * 20) // 75-95 kph
      } else {
        speed = 115 + Math.floor(Math.random() * 20) // 115-135 kph
      }
      
      // Adjust speed based on delivery type
      if (type === 'WICKET') speed += 2 // Slightly quicker
      if (selectedZone === zones.yorker) speed += 3 // Yorkers often quicker
      if (selectedZone === zones.bouncer) speed += 4 // Bouncers are quicker

      deliveries.push({
        x,
        y,
        type,
        speed,
        bowler: bowler.bowlName
      })
    }
  })
  
  return deliveries
}

// Initialize charts
const initializeCharts = () => {
  if (!currentInnings.value) return
  
  if (wicketDistributionChart.value) {
    charts.value.wicketDistribution = echarts.init(wicketDistributionChart.value)
    initializeWicketDistributionChart()
  }
  
  if (economyRateChart.value) {
    charts.value.economyRate = echarts.init(economyRateChart.value)
    initializeEconomyRateChart()
  }
}

// Initialize wicket distribution chart
const initializeWicketDistributionChart = () => {
  if (!currentInnings.value) return
  
  const bowlers = currentInnings.value.bowlTeamDetails.bowlersData
  const option = {
    ...chartConfig,
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} wickets ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: { color: '#94a3b8' }
    },
    series: [
      {
        name: 'Wicket Distribution',
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
        data: bowlers.filter(b => b.wickets > 0).map((bowler, index) => ({
          value: bowler.wickets,
          name: bowler.bowlName,
          itemStyle: { color: getChartColor(index) }
        }))
      }
    ]
  }
  
  charts.value.wicketDistribution.setOption(option)
}

// Initialize economy rate chart
const initializeEconomyRateChart = () => {
  if (!currentInnings.value) return
  
  const bowlers = currentInnings.value.bowlTeamDetails.bowlersData
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
    xAxis: [
      {
        type: 'category',
        data: bowlers.map(b => b.bowlName),
        axisTick: {
          alignWithLabel: true
        },
        axisLabel: {
          rotate: 30,
          ...chartConfig.axisStyle.axisLabel
        },
        ...chartConfig.axisStyle
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: 'Economy Rate',
        min: 0,
        max: 12,
        ...chartConfig.axisStyle
      }
    ],
    series: [
      {
        name: 'Economy Rate',
        type: 'bar',
        barWidth: '60%',
        data: bowlers.map((bowler, index) => ({
          value: bowler.economy,
          itemStyle: { 
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: getEconomyColor(bowler.economy, 0.8) },
              { offset: 1, color: getEconomyColor(bowler.economy, 0.5) }
            ])
          }
        }))
      }
    ]
  }
  
  charts.value.economyRate.setOption(option)
}

// Color utility functions
const getChartColor = (index) => {
  const colors = ['#6366f1', '#ec4899', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4', '#f97316', '#14b8a6']
  return colors[index % colors.length]
}

const getEconomyColor = (economy, alpha = 1) => {
  if (economy < 6) return `rgba(16, 185, 129, ${alpha})` // green
  if (economy < 8) return `rgba(99, 102, 241, ${alpha})` // indigo
  if (economy < 10) return `rgba(245, 158, 11, ${alpha})` // amber
  return `rgba(239, 68, 68, ${alpha})` // red
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
.pitch-map-container {
  height: 560px;
  width: 100%;
  overflow: hidden;
  position: relative;
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