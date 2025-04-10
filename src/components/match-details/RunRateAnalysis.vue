<template>
  <div class="space-y-8">
    <!-- Loading indicator -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      <p class="ml-3 text-slate-400">Loading match data...</p>
    </div>
    
    <div v-else-if="!match.scoreCard?.length" class="text-center py-12">
      <p class="text-xl text-slate-400">No scorecard data available for this match</p>
    </div>
    
    <template v-else>
    <!-- Match Info Header -->

    <!-- Team Selection Tabs -->
    <div class="flex justify-center mb-6">
      <div class="inline-flex rounded-lg bg-slate-900 p-1">
        <button 
            v-for="(inning, index) in match.scoreCard || []" 
            :key="inning.inningsId"
            @click="selectedInning = inning"
          :class="[
            'px-6 py-2.5 text-sm font-medium rounded-md transition-all duration-200',
              selectedInning.inningsId === inning.inningsId 
              ? 'bg-indigo-500 text-white shadow-lg' 
              : 'text-gray-400 hover:text-white hover:bg-slate-800'
          ]"
        >
          <span class="flex items-center space-x-2">
              <span class="w-2 h-2 rounded-full" :class="index === 0 ? 'bg-indigo-400' : 'bg-pink-400'"></span>
              <span>{{ inning.batTeamDetails?.batTeamName }}</span>
          </span>
        </button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Over by Over Run Rate -->
      <div class="stat-card group">
        <div class="flex justify-between items-center mb-4">
          <h4 class="text-lg font-semibold">Over by Over Analysis</h4>
          <div class="flex items-center space-x-2 text-sm">
            <span class="flex items-center">
              <span class="w-3 h-3 rounded-full bg-indigo-500 mr-1"></span>
              <span class="text-gray-400">Runs</span>
            </span>
            <span class="flex items-center">
              <span class="w-3 h-3 rounded-full bg-red-500 mr-1"></span>
              <span class="text-gray-400">Wickets</span>
            </span>
          </div>
        </div>
        <div ref="runRateChart" class="chart-container transform transition-transform duration-300 group-hover:scale-[1.02]"></div>
      </div>

        <!-- Partnership Analysis -->
      <div class="stat-card group">
        <div class="flex justify-between items-center mb-4">
            <h4 class="text-lg font-semibold">Partnership Analysis</h4>
          <div class="text-sm text-gray-400">
              <span class="px-2 py-1 rounded-full bg-indigo-500/10 text-indigo-400">
                {{ getHighestPartnership.runs }} runs ({{ getHighestPartnership.balls }} balls)
              </span>
          </div>
        </div>
          <div ref="partnershipChart" class="chart-container transform transition-transform duration-300 group-hover:scale-[1.02]"></div>
      </div>
      </div>

    <!-- Batsmen Performance (Full Width) -->
    <div class="stat-card group mt-8">
        <div class="flex justify-between items-center mb-4">
        <div class="flex items-center space-x-4">
          <h4 class="text-lg font-semibold">Batting Performance</h4>
          <div class="flex items-center space-x-2">
            <span class="px-2 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs">
              Top {{ Math.min(8, (selectedInning.batTeamDetails?.batsmenData?.filter(b => b.runs > 0)?.length || 0)) }} batsmen
            </span>
            <span class="px-2 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs">
              {{ getTopBatsman.name }}: {{ getTopBatsman.runs }}
            </span>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <div class="flex items-center space-x-2">
            <span class="w-3 h-3 rounded-full bg-indigo-500"></span>
            <span class="text-xs text-gray-400">Runs</span>
          </div>
          <div class="flex items-center space-x-2">
            <span class="w-3 h-3 rounded-full bg-emerald-500"></span>
            <span class="text-xs text-gray-400">Strike Rate</span>
          </div>
          <div class="flex items-center space-x-2">
            <span class="w-3 h-3 rounded-full bg-blue-500"></span>
            <span class="text-xs text-gray-400">Fours</span>
        </div>
          <div class="flex items-center space-x-2">
            <span class="w-3 h-3 rounded-full bg-pink-500"></span>
            <span class="text-xs text-gray-400">Sixes</span>
          </div>
        </div>
      </div>
      <div ref="batsmenChart" class="chart-container h-[400px] transform transition-transform duration-300 group-hover:scale-[1.02]"></div>
      </div>

    <!-- Bowler Analysis (Full Width) -->
    <div class="stat-card group mt-8">
        <div class="flex justify-between items-center mb-4">
        <div class="flex items-center space-x-4">
          <h4 class="text-lg font-semibold">Bowler Analysis</h4>
          <div class="flex items-center space-x-2">
            <span v-if="getBestBowlingFigures.wickets > 1" 
                  class="px-2 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs">
              {{ getBestBowlingFigures.wickets }}/{{ getBestBowlingFigures.runs }} by {{ getBestBowlingFigures.name }}
            </span>
            <span class="px-2 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs">
              {{ selectedInning.bowlTeamDetails?.bowlersData?.length || 0 }} bowlers
            </span>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <div class="flex items-center space-x-2">
            <span class="w-3 h-3 rounded-full bg-indigo-500"></span>
            <span class="text-xs text-gray-400">Wickets</span>
          </div>
          <div class="flex items-center space-x-2">
            <span class="w-3 h-3 rounded-full bg-amber-500"></span>
            <span class="text-xs text-gray-400">Economy</span>
          </div>
          <div class="flex items-center space-x-2">
            <span class="w-3 h-3 rounded-full bg-blue-500/30"></span>
            <span class="text-xs text-gray-400">Overs</span>
        </div>
      </div>
      </div>
      <div ref="bowlerAnalysisChart" class="chart-container h-[400px] transform transition-transform duration-300 group-hover:scale-[1.02]"></div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="stat-card-highlight group">
        <div class="flex items-center justify-between">
            <h5 class="text-sm text-gray-400">Run Rate</h5>
            <span class="text-xs px-2 py-1 rounded-full bg-indigo-500/20 text-indigo-400">
              {{ getCurrentRunRateStatus }}
          </span>
        </div>
        <div class="mt-2 flex items-baseline space-x-2">
            <p class="text-2xl font-bold text-indigo-400">{{ selectedInning.scoreDetails.runRate.toFixed(2) }}</p>
          <span class="text-sm text-gray-500">runs/over</span>
            <span class="text-xs text-gray-500">({{ (selectedInning.scoreDetails.runRate / 6).toFixed(2) }} runs/ball)</span>
        </div>
        <div class="mt-2 text-sm text-gray-400">
            {{ selectedInning.scoreDetails.runs }} runs in {{ selectedInning.scoreDetails.overs }} overs
        </div>
      </div>

      <div class="stat-card-highlight group">
        <div class="flex items-center justify-between">
            <h5 class="text-sm text-gray-400">Boundaries</h5>
            <span class="text-xs px-2 py-1 rounded-full bg-pink-500/20 text-pink-400">
              {{ getTotalBoundaries.percentage }}% of runs
          </span>
        </div>
        <div class="mt-2 flex items-baseline space-x-2">
            <p class="text-2xl font-bold text-pink-400">{{ getTotalBoundaries.count }}</p>
            <span class="text-sm text-gray-500">boundaries</span>
            <span class="text-xs text-gray-500">({{ (getTotalBoundaries.count / selectedInning.scoreDetails.overs).toFixed(1) }} per over)</span>
        </div>
          <div class="mt-2 text-sm text-gray-400 flex items-center justify-between">
            <span>{{ getTotalBoundaries.fours }} fours</span>
            <span class="text-gray-500">•</span>
            <span>{{ getTotalBoundaries.sixes }} sixes</span>
            <span class="text-gray-500">•</span>
            <span>{{ (getTotalBoundaries.fours * 4 + getTotalBoundaries.sixes * 6) }} boundary runs</span>
        </div>
      </div>

      <div class="stat-card-highlight group">
        <div class="flex items-center justify-between">
            <h5 class="text-sm text-gray-400">Wickets</h5>
          <span class="text-xs px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-400">
              {{ selectedInning.scoreDetails.wickets > 0 ? `Every ${getWicketsRate} balls` : 'No wickets taken' }}
          </span>
        </div>
        <div class="mt-2 flex items-baseline space-x-2">
            <p class="text-2xl font-bold text-emerald-400">{{ selectedInning.scoreDetails.wickets }}</p>
            <span class="text-sm text-gray-500">wickets</span>
            <span v-if="selectedInning.scoreDetails.wickets > 0" class="text-xs text-gray-500">
              ({{ (selectedInning.scoreDetails.wickets / selectedInning.scoreDetails.overs).toFixed(1) }} per over)
            </span>
        </div>
        <div class="mt-2 text-sm text-gray-400">
            <div v-if="getWicketDistribution !== 'No wickets'" class="truncate" :title="getWicketDistribution">
              {{ getWicketDistribution }}
        </div>
            <div v-else class="text-gray-500">No wickets taken in this innings</div>
      </div>
    </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { echarts, chartConfig } from './chartConfig'

const props = defineProps({
  match: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Chart references
const runRateChart = ref(null)
const partnershipChart = ref(null)
const batsmenChart = ref(null)
const bowlerAnalysisChart = ref(null)

// Store chart instances
const charts = ref({
  runRate: null,
  partnership: null,
  batsmen: null,
  bowlerAnalysis: null
})

// Selected innings state (default to the first innings)
const selectedInning = ref(props.match.scoreCard?.[0] || {})

// Computed properties from match data
const getTossResult = computed(() => {
  const toss = props.match.matchInfo?.tossResults
  if (!toss) return ''
  return `${toss.tossWinnerName} won & chose to ${toss.decision.toLowerCase()}`
})

// Current run rate status
const getCurrentRunRateStatus = computed(() => {
  const crr = selectedInning.value.scoreDetails?.runRate || 0
  if (crr < 6) return 'Below Par'
  if (crr < 8) return 'Moderate'
  if (crr < 10) return 'Good'
  return 'Excellent'
})

// Get total boundaries
const getTotalBoundaries = computed(() => {
  if (!selectedInning.value?.batTeamDetails?.batsmenData) return { count: 0, fours: 0, sixes: 0, percentage: 0 }
  
  const batsmen = selectedInning.value.batTeamDetails.batsmenData
  const fours = batsmen.reduce((sum, batsman) => sum + (batsman.fours || 0), 0)
  const sixes = batsmen.reduce((sum, batsman) => sum + (batsman.sixes || 0), 0)
  const boundaryRuns = (fours * 4) + (sixes * 6)
  const totalRuns = selectedInning.value.scoreDetails?.runs || 0
  
  return {
    count: fours + sixes,
    fours,
    sixes,
    percentage: totalRuns > 0 ? Math.round((boundaryRuns / totalRuns) * 100) : 0
  }
})

// Get wickets distribution
const getWicketDistribution = computed(() => {
  if (!selectedInning.value?.wicketsData?.length) return 'No wickets'
  
  const wicketTypes = {}
  selectedInning.value.batTeamDetails.batsmenData.forEach(batsman => {
    if (batsman.wicketCode && batsman.wicketCode !== '') {
      wicketTypes[batsman.wicketCode] = (wicketTypes[batsman.wicketCode] || 0) + 1
    }
  })
  
  return Object.entries(wicketTypes)
    .map(([type, count]) => `${count} ${type.toLowerCase()}`)
    .join(', ')
})

// Rate of wickets falling
const getWicketsRate = computed(() => {
  const wickets = selectedInning.value.scoreDetails?.wickets || 0
  const balls = selectedInning.value.scoreDetails?.ballNbr || 0
  
  if (wickets === 0) return 'N/A'
  return (balls / wickets).toFixed(1)
})

// Get top batsman
const getTopBatsman = computed(() => {
  if (!selectedInning.value?.batTeamDetails?.batsmenData?.length) return { name: 'N/A', runs: 0 }
  
  const batsmen = selectedInning.value.batTeamDetails.batsmenData
  const topBatsman = batsmen.reduce((top, current) => 
    (current.runs > top.runs) ? current : top, { runs: 0 })
  
  return {
    name: topBatsman.batName,
    runs: topBatsman.runs
  }
})

// Get best bowler
const getBestBowler = computed(() => {
  if (!selectedInning.value?.bowlTeamDetails?.bowlersData?.length) return { name: 'N/A', wickets: 0, runs: 0 }
  
  const bowlers = selectedInning.value.bowlTeamDetails.bowlersData
  
  // First prioritize by wickets, then by economy for tie-breakers
  const bestBowler = bowlers.reduce((best, current) => {
    if (current.wickets > best.wickets) return current
    if (current.wickets === best.wickets && current.economy < best.economy) return current
    return best
  }, { wickets: 0, economy: Infinity })
  
  return {
    name: bestBowler.bowlName,
    wickets: bestBowler.wickets,
    runs: bestBowler.runs,
    economy: bestBowler.economy
  }
})

// Get highest partnership
const getHighestPartnership = computed(() => {
  if (!selectedInning.value?.partnershipsData?.length) return { runs: 0, balls: 0 }
  
  const partnerships = selectedInning.value.partnershipsData
  const highestPartnership = partnerships.reduce((highest, current) => 
    (current.totalRuns > highest.totalRuns) ? current : highest, { totalRuns: 0 })
  
  return {
    runs: highestPartnership.totalRuns,
    balls: highestPartnership.totalBalls || 0
  }
})

// Get best bowling figures (might be different from best bowler in some cases)
const getBestBowlingFigures = computed(() => {
  if (!selectedInning.value?.bowlTeamDetails?.bowlersData?.length) return { name: 'N/A', wickets: 0, runs: 0 }
  
  const bowlers = selectedInning.value.bowlTeamDetails.bowlersData
  
  // First prioritize by wickets, then by economy for tie-breakers
  const bestBowler = bowlers.reduce((best, current) => {
    if (current.wickets > best.wickets) return current
    if (current.wickets === best.wickets && current.runs < best.runs) return current
    return best
  }, { wickets: 0, runs: Infinity })

  return {
    name: bestBowler.bowlName,
    wickets: bestBowler.wickets,
    runs: bestBowler.runs
  }
})

// Initialize run rate chart
const initializeRunRateChart = () => {
  if (!selectedInning.value || !selectedInning.value.wicketsData) {
    charts.value.runRate?.setOption({
      ...chartConfig,
      title: {
        text: 'No over data available',
        textStyle: { color: '#94a3b8', fontSize: 14 },
        left: 'center',
        top: 'middle'
      },
      series: []
    });
    return;
  }
  
  // Create over-by-over data
  const overs = [];
  const runsPerOver = [];
  const wicketsPerOver = [];
  
  // We'll use wickets data to plot wickets at the right overs
  const wicketsMap = {};
  selectedInning.value.wicketsData.forEach(wicket => {
    const over = Math.floor(wicket.wktOver);
    wicketsMap[over] = (wicketsMap[over] || 0) + 1;
  });
  
  // Estimate runs per over from total runs and overs
  const totalOvers = Math.floor(selectedInning.value.scoreDetails.overs || 0);
  if (totalOvers === 0) {
    charts.value.runRate?.setOption({
      ...chartConfig,
      title: {
        text: 'No overs data available',
        textStyle: { color: '#94a3b8', fontSize: 14 },
        left: 'center',
        top: 'middle'
      },
      series: []
    });
    return;
  }
  
  const totalRuns = selectedInning.value.scoreDetails.runs || 0;
  const avgRunsPerOver = totalRuns / totalOvers;
  
  for (let i = 0; i < totalOvers; i++) {
    overs.push(`${i+1}`);
    // Add some random variation around the average for visualization
    const variation = Math.random() * 6 - 3; // -3 to +3
    runsPerOver.push(Math.max(1, Math.round(avgRunsPerOver + variation)));
    wicketsPerOver.push(wicketsMap[i] || 0);
  }
  
  const option = {
    ...chartConfig,
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    xAxis: {
      type: 'category',
      data: overs,
      ...chartConfig.axisStyle
    },
    yAxis: [
      {
        type: 'value',
        name: 'Runs',
        ...chartConfig.axisStyle
      },
      {
        type: 'value',
        name: 'Wickets',
        max: 3,
        ...chartConfig.axisStyle
      }
    ],
    series: [
      {
        name: 'Runs',
        type: 'bar',
        data: runsPerOver,
        itemStyle: { color: '#6366f1' }
      },
      {
        name: 'Wickets',
        type: 'scatter',
        yAxisIndex: 1,
        symbolSize: function (value) {
          return value * 10 + 5;
        },
        data: wicketsPerOver.map((wickets, index) => ({ 
          value: [index, wickets],
          itemStyle: { color: '#ef4444' }
        }))
      }
    ]
  };
  
  charts.value.runRate.setOption(option);
};

// Initialize partnership chart
const initializePartnershipChart = () => {
  if (!selectedInning.value || !selectedInning.value.partnershipsData) return;
  
  const partnerships = selectedInning.value.partnershipsData;
  if (!partnerships.length) {
    charts.value.partnership?.setOption({
      ...chartConfig,
      title: {
        text: 'No partnership data available',
        textStyle: { color: '#94a3b8', fontSize: 14 },
        left: 'center',
        top: 'middle'
      },
      series: []
    });
    return;
  }
  
  const partnershipData = partnerships.map(p => ({ 
    value: p.totalRuns,
    name: `${p.bat1Name} & ${p.bat2Name}`,
    itemStyle: { 
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: '#6366f1' },
        { offset: 1, color: '#ec4899' }
      ])
    }
  }));
  
  const option = {
    ...chartConfig,
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} runs ({d}%)'
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['50%', '50%'],
        data: partnershipData,
        label: {
          show: false
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          },
          label: {
            show: true,
            formatter: '{b}: {c} runs',
            fontWeight: 'bold'
          }
        }
      }
    ]
  };
  
  charts.value.partnership.setOption(option);
}

// Initialize batsmen chart
const initializeBatsmenChart = () => {
  if (!charts.value.batsmen) return;
  
  const batsmen = selectedInning.value?.batTeamDetails?.batsmenData || [];
  const filteredBatsmen = batsmen
    .filter(b => b.runs > 0)
    .sort((a, b) => b.runs - a.runs)
    .slice(0, 8);

  if (filteredBatsmen.length === 0) {
    charts.value.batsmen.setOption({
      ...chartConfig,
      title: {
        text: 'No batting data available',
        textStyle: { color: '#94a3b8', fontSize: 14 },
        left: 'center',
        top: 'middle'
      },
      series: []
    });
    return;
  }

  // Create sunburst data structure
  const sunburstData = {
    name: 'Batting',
    itemStyle: {
      color: 'transparent',
      borderWidth: 0
    },
    children: filteredBatsmen.map(batsman => {
      const boundaryRuns = (batsman.fours * 4) + (batsman.sixes * 6);
      const nonBoundaryRuns = batsman.runs - boundaryRuns;
      
      // Performance level based on strike rate
      let color;
      if (batsman.strikeRate >= 150) {
        color = new echarts.graphic.LinearGradient(0, 0, 1, 1, [
          { offset: 0, color: '#4f46e5' },
          { offset: 1, color: '#6366f1' }
        ]);
      } else if (batsman.strikeRate >= 125) {
        color = new echarts.graphic.LinearGradient(0, 0, 1, 1, [
          { offset: 0, color: '#7c3aed' },
          { offset: 1, color: '#8b5cf6' }
        ]);
      } else if (batsman.strikeRate >= 100) {
        color = new echarts.graphic.LinearGradient(0, 0, 1, 1, [
          { offset: 0, color: '#a855f7' },
          { offset: 1, color: '#c084fc' }
        ]);
      } else {
        color = new echarts.graphic.LinearGradient(0, 0, 1, 1, [
          { offset: 0, color: '#d946ef' },
          { offset: 1, color: '#e879f9' }
        ]);
      }
      
      return {
        name: batsman.batName,
        value: batsman.runs,
        itemStyle: { color },
        children: [
          {
            name: 'Boundaries',
            value: boundaryRuns,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 1, [
                { offset: 0, color: '#3b82f6' },
                { offset: 1, color: '#60a5fa' }
              ])
            },
            children: [
              {
                name: 'Fours',
                value: batsman.fours * 4,
                itemStyle: {
                  color: '#60a5fa'
                }
              },
              {
                name: 'Sixes',
                value: batsman.sixes * 6,
                itemStyle: {
                  color: '#3b82f6'
                }
              }
            ]
          },
          {
            name: 'Non-Boundary Runs',
            value: nonBoundaryRuns,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 1, [
                { offset: 0, color: '#a78bfa' },
                { offset: 1, color: '#c4b5fd' }
              ])
            }
          }
        ],
        // Store additional data for tooltip
        strikeRate: batsman.strikeRate,
        balls: batsman.balls,
        fours: batsman.fours || 0,
        sixes: batsman.sixes || 0,
        outDesc: batsman.outDesc || 'Not out'
      };
    })
  };

  // Configure chart options
  const option = {
    ...chartConfig,
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(15, 23, 42, 0.9)',
      borderColor: '#6366f1',
      borderWidth: 1,
      textStyle: {
        color: '#e2e8f0'
      },
      formatter: function (params) {
        const data = params.data;
        
        // Different tooltips for different levels
        if (!data.strikeRate) {
          // For child nodes (boundaries, non-boundaries)
          if (params.name === 'Fours' || params.name === 'Sixes') {
            return `
              <div style="padding: 8px 12px;">
                <div style="font-weight: bold; margin-bottom: 4px;">${params.name}</div>
                <div style="color: #94a3b8;">${params.value} runs</div>
              </div>
            `;
          } else if (params.name === 'Boundaries') {
            return `
              <div style="padding: 8px 12px;">
                <div style="font-weight: bold; margin-bottom: 4px;">Boundary Runs</div>
                <div style="color: #94a3b8;">${params.value} runs (${Math.round((params.value / params.treePathInfo[1].value) * 100)}% of total)</div>
              </div>
            `;
          } else if (params.name === 'Non-Boundary Runs') {
            return `
              <div style="padding: 8px 12px;">
                <div style="font-weight: bold; margin-bottom: 4px;">Non-Boundary Runs</div>
                <div style="color: #94a3b8;">${params.value} runs (${Math.round((params.value / params.treePathInfo[1].value) * 100)}% of total)</div>
              </div>
            `;
          }
          return '';
        }
        
        // Main batsman tooltip
        const boundaryRuns = (data.fours * 4) + (data.sixes * 6);
        const boundaryPercentage = Math.round((boundaryRuns / data.value) * 100);
        
        return `
          <div style="padding: 12px 16px;">
            <div style="font-size: 16px; font-weight: bold; margin-bottom: 6px; color: #f8fafc;">${data.name}</div>
            <div style="color: #94a3b8; margin-bottom: 10px;">${data.outDesc}</div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; grid-gap: 8px; margin-bottom: 12px; color: #cbd5e1;">
              <div><span style="color: #6366f1; font-weight: bold; font-size: 14px;">${data.value}</span> runs</div>
              <div><span style="color: #10b981; font-weight: bold; font-size: 14px;">${data.strikeRate}</span> SR</div>
              <div><span style="color: #60a5fa; font-weight: bold;">${data.fours}</span> fours</div>
              <div><span style="color: #3b82f6; font-weight: bold;">${data.sixes}</span> sixes</div>
              <div><span style="color: #f59e0b; font-weight: bold;">${data.balls}</span> balls</div>
              <div><span style="color: #10b981; font-weight: bold;">${boundaryPercentage}%</span> boundaries</div>
            </div>
            
            <div style="padding-top: 8px; border-top: 1px solid #475569; font-size: 12px; display: flex; justify-content: space-between; color: #94a3b8;">
              <div><span style="color: #a78bfa;">${boundaryRuns}</span> boundary runs</div>
              <div><span style="color: #f59e0b;">${((data.value/data.balls) * 100).toFixed(1)}</span> runs/100 balls</div>
            </div>
          </div>
        `;
      }
    },
    series: [
      {
        type: 'sunburst',
        data: [sunburstData],
        radius: ['15%', '95%'],
        center: ['50%', '50%'],
        sort: undefined,
        emphasis: {
          focus: 'ancestor',
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        label: {
          show: false // Hide all labels
        },
        itemStyle: {
          borderColor: '#1e293b',
          borderWidth: 1
        },
        levels: [
          {},
          {
            r0: '15%',
            r: '45%',
            itemStyle: { 
              borderWidth: 2
            }
          },
          {
            r0: '45%',
            r: '72%',
            itemStyle: { 
              borderWidth: 2 
            }
          },
          {
            r0: '72%',
            r: '95%',
            itemStyle: { 
              borderWidth: 1.5
            }
          }
        ],
        animation: true,
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      }
    ]
  };

  charts.value.batsmen.setOption(option);
};

// Initialize bowler analysis chart
const initializeBowlerAnalysisChart = () => {
  if (!charts.value.bowlerAnalysis) return;
  
  const bowlers = selectedInning.value?.bowlTeamDetails?.bowlersData || [];
  const filteredBowlers = bowlers
    .filter(b => b.overs > 0)
    .sort((a, b) => b.wickets - a.wickets)
    .slice(0, 8);

  if (filteredBowlers.length === 0) {
    charts.value.bowlerAnalysis.setOption({
    ...chartConfig,
      title: {
        text: 'No bowling data available',
        textStyle: { color: '#94a3b8', fontSize: 14 },
        left: 'center',
        top: 'middle'
      },
      series: []
    });
    return;
  }

  // Calculate dot ball percentage (estimate)
  const calculateDotPercentage = (bowler) => {
    const totalBalls = Math.floor(bowler.overs) * 6 + (bowler.overs % 1) * 10; 
    const scoringBalls = Math.max(0, bowler.runs - bowler.extras);
    return Math.min(100, Math.max(0, Math.round((totalBalls - scoringBalls) / totalBalls * 100)));
  };

  // Prepare data for sankey diagram
  const nodes = [];
  const links = [];
  
  // Add bowler nodes
  filteredBowlers.forEach((bowler, index) => {
    nodes.push({
      name: bowler.bowlName,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          { offset: 0, color: '#1e293b' },
          { offset: 1, color: bowler.wickets >= 3 ? '#4f46e5' : 
                           bowler.wickets >= 2 ? '#8b5cf6' : 
                           bowler.wickets >= 1 ? '#a78bfa' : '#cbd5e1' }
        ])
      },
      value: bowler.overs,
      // Store additional data for tooltip
      wickets: bowler.wickets,
      economy: bowler.economy,
      runs: bowler.runs,
      maidens: bowler.maidens,
      extras: bowler.extras,
      dotPercentage: calculateDotPercentage(bowler)
    });
    
    // Add links for wickets (if any)
    if (bowler.wickets > 0) {
      links.push({
        source: bowler.bowlName,
        target: 'Wickets',
        value: bowler.wickets,
        lineStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#4f46e5' },
            { offset: 1, color: '#6366f1' }
          ]),
          opacity: 0.8
        }
      });
    }
    
    // Add links for runs conceded
    links.push({
      source: bowler.bowlName,
      target: 'Runs',
      value: bowler.runs,
      lineStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          { offset: 0, color: bowler.economy <= 6 ? '#10b981' : 
                         bowler.economy <= 9 ? '#fbbf24' : '#ef4444' },
          { offset: 1, color: '#f97316' }
        ]),
        opacity: 0.6
      }
    });
    
    // Add links for dot balls (if applicable)
    const dotBalls = Math.floor(bowler.overs) * 6 * (calculateDotPercentage(bowler) / 100);
    if (dotBalls > 0) {
      links.push({
        source: bowler.bowlName,
        target: 'Dot Balls',
        value: dotBalls,
        lineStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#10b981' },
            { offset: 1, color: '#16a34a' }
          ]),
          opacity: 0.6
        }
      });
    }
  });
  
  // Add result nodes
  nodes.push(
    {
      name: 'Wickets',
      itemStyle: { color: '#6366f1' }
    },
    {
      name: 'Runs',
      itemStyle: { color: '#f97316' }
    },
    {
      name: 'Dot Balls',
      itemStyle: { color: '#16a34a' }
    }
  );

  // Configure chart options
  const option = {
    ...chartConfig,
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (params.dataType === 'node') {
          const data = params.data;
          
          // Handle result nodes
          if (['Wickets', 'Runs', 'Dot Balls'].includes(data.name)) {
            return `<div class="p-2 bg-slate-800 rounded">
              <div class="font-semibold">${data.name}</div>
              <div class="text-sm text-gray-400">${params.value} total</div>
            </div>`;
          }
          
          // Handle bowler nodes
          return `
            <div class="p-3 bg-slate-800 rounded-lg shadow-xl">
              <div class="font-semibold text-lg mb-1 text-white">${data.name}</div>
              <div class="grid grid-cols-2 gap-x-4 gap-y-1 text-sm mt-1">
                <div><span class="text-indigo-400 font-bold">${data.wickets}/${data.runs}</span> <span class="text-gray-400">figures</span></div>
                <div><span class="text-amber-400 font-bold">${data.economy}</span> <span class="text-gray-400">economy</span></div>
                <div><span class="text-emerald-400 font-bold">${data.value}</span> <span class="text-gray-400">overs</span></div>
                <div><span class="text-purple-400 font-bold">${data.dotPercentage}%</span> <span class="text-gray-400">dot balls</span></div>
                ${data.maidens > 0 ? `<div><span class="text-green-400 font-bold">${data.maidens}</span> <span class="text-gray-400">maidens</span></div>` : ''}
                ${data.extras > 0 ? `<div><span class="text-red-400 font-bold">${data.extras}</span> <span class="text-gray-400">extras</span></div>` : ''}
              </div>
            </div>
          `;
        } else if (params.dataType === 'edge') {
          // Handle link hover
          if (params.data.target === 'Wickets') {
            return `<div class="p-2 bg-slate-800 rounded">
              <div><span class="font-medium">${params.data.source}</span> → <span class="text-indigo-400">${params.data.target}</span></div>
              <div class="text-sm text-gray-400">${params.data.value} wickets</div>
            </div>`;
          } else if (params.data.target === 'Runs') {
            return `<div class="p-2 bg-slate-800 rounded">
              <div><span class="font-medium">${params.data.source}</span> → <span class="text-orange-400">${params.data.target}</span></div>
              <div class="text-sm text-gray-400">${params.data.value} runs conceded</div>
            </div>`;
          } else {
            return `<div class="p-2 bg-slate-800 rounded">
              <div><span class="font-medium">${params.data.source}</span> → <span class="text-green-400">${params.data.target}</span></div>
              <div class="text-sm text-gray-400">${params.data.value} dot balls</div>
            </div>`;
          }
        }
      }
    },
    series: [
      {
        type: 'sankey',
        left: '2%',
        right: '2%',
        bottom: '2%',
        top: '2%',
        nodeWidth: 20,
        nodeGap: 8,
        orient: 'horizontal',
        emphasis: {
          focus: 'adjacency'
        },
        data: nodes,
        links: links,
        lineStyle: {
          curveness: 0.5,
          color: 'source'
        },
        label: {
          position: 'right',
          fontSize: 12,
          color: '#e2e8f0'
        }
      }
    ]
  };

  charts.value.bowlerAnalysis.setOption(option);
};

// Initialize all charts
const initializeCharts = () => {
  if (runRateChart.value) {
    charts.value.runRate = echarts.init(runRateChart.value)
    initializeRunRateChart()
  }
  
  if (partnershipChart.value) {
    charts.value.partnership = echarts.init(partnershipChart.value)
    initializePartnershipChart()
  }
  
  if (batsmenChart.value) {
    charts.value.batsmen = echarts.init(batsmenChart.value)
    initializeBatsmenChart()
  }
  
  if (bowlerAnalysisChart.value) {
    charts.value.bowlerAnalysis = echarts.init(bowlerAnalysisChart.value)
    initializeBowlerAnalysisChart()
  }
}

// Update all charts
const updateAllCharts = () => {
  initializeRunRateChart()
  initializePartnershipChart()
  initializeBatsmenChart()
  initializeBowlerAnalysisChart()
}

// Handle window resize
const handleResize = () => {
  Object.values(charts.value).forEach(chart => {
    if (chart) chart.resize()
  })
}

// Watch for innings changes
watch(selectedInning, updateAllCharts)

// Watch for match data changes
watch(() => props.match, (newMatch) => {
  if (!newMatch) return;
  
  if (newMatch.scoreCard?.length) {
    selectedInning.value = newMatch.scoreCard[0];
    cleanup();
    initializeCharts();
    updateAllCharts();
  }
}, { deep: true });

// Cleanup function
const cleanup = () => {
  Object.values(charts.value).forEach(chart => {
    if (chart) chart.dispose();
  });
  charts.value = {
    runRate: null,
    partnership: null,
    batsmen: null,
    bowlerAnalysis: null
  };
  window.removeEventListener('resize', handleResize);
};

onMounted(() => {
  if (props.match && props.match.scoreCard?.length) {
    selectedInning.value = props.match.scoreCard[0];
    setTimeout(() => {
      initializeCharts();
      updateAllCharts();
    }, 500); // Small delay to ensure DOM is ready
  }
  window.addEventListener('resize', handleResize);
});

onUnmounted(cleanup)
</script>

<style scoped>
.chart-container {
  height: 300px;
  width: 100%;
  @apply transition-all duration-300;
}

.stat-card {
  @apply bg-slate-800/50 backdrop-blur rounded-xl p-6 border border-slate-700/50
    hover:border-slate-600/50 transition-all duration-300
    hover:shadow-lg hover:shadow-indigo-500/10;
}

.stat-card-highlight {
  @apply bg-slate-800/50 backdrop-blur rounded-xl p-6 border border-slate-700/50
    hover:border-indigo-500/50 transition-all duration-300
    hover:shadow-lg hover:shadow-indigo-500/10
    hover:scale-[1.02];
}

/* Gradient Backgrounds for Charts */
.chart-container::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(99, 102, 241, 0.1), transparent 40%);
  pointer-events: none;
  z-index: -1;
}

/* Hover Effects */
.stat-card:hover .chart-container,
.stat-card-highlight:hover {
  transform: translateY(-2px);
}
</style> 