<template>
  <div class="space-y-8">
    <!-- Loading indicator -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      <p class="ml-3 text-slate-400">Loading match data...</p>
    </div>
    
    <div v-else-if="!matchData" class="text-center py-12">
      <p class="text-xl text-slate-400">No match data available</p>
    </div>
    
    <div v-else>
      <!-- Match Header -->
      <div class="bg-slate-800 rounded-lg shadow-lg p-6 mb-8">
        <div class="flex justify-between items-center">
          <div>
            <div class="flex items-center">
              <span class="rounded-md px-3 py-1 text-sm font-medium bg-indigo-500/20 text-indigo-400 mr-3">{{ matchData.matchHeader.matchDescription }}</span>
              <h2 class="text-lg text-gray-300">{{ matchData.matchHeader.seriesDesc }}</h2>
            </div>
            <h1 class="text-2xl font-bold text-white mt-2">{{ matchData.batTeam.teamScore }}/{{ matchData.batTeam.teamWkts }} <span class="text-indigo-400">({{ matchData.overs }} overs)</span></h1>
            <p class="text-sm text-gray-400 mt-1">{{ matchData.status }}</p>
          </div>
          <div class="text-right">
            <div class="text-xl font-bold">
              <span class="text-emerald-500">CRR: {{ matchData.currentRunRate.toFixed(2) }}</span>
              <span v-if="matchData.requiredRunRate > 0" class="ml-2 text-pink-500">RRR: {{ matchData.requiredRunRate.toFixed(2) }}</span>
            </div>
            <p v-if="matchData.target" class="text-sm text-gray-400 mt-1">Target: {{ matchData.target }} runs</p>
          </div>
        </div>
        
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
          <div class="stat-card-highlight">
            <div class="flex items-center justify-between">
              <h3 class="text-sm text-gray-400">Current Batsmen</h3>
              <span class="text-xs px-2 py-1 rounded-full bg-indigo-500/20 text-indigo-400">At Crease</span>
            </div>
            <div class="grid grid-cols-2 gap-4 mt-2">
              <div>
                <p class="text-white font-semibold mt-1">{{ matchData.batsmanStriker.batName }} <span class="text-indigo-400">*</span></p>
                <p class="text-sm text-gray-400">{{ matchData.batsmanStriker.batRuns }}({{ matchData.batsmanStriker.batBalls }}) <span class="text-emerald-400">SR: {{ matchData.batsmanStriker.batStrikeRate }}</span></p>
                <p class="text-xs text-gray-500">{{ matchData.batsmanStriker.batFours }} fours, {{ matchData.batsmanStriker.batSixes }} sixes</p>
              </div>
              <div>
                <p class="text-white font-semibold mt-1">{{ matchData.batsmanNonStriker.batName }}</p>
                <p class="text-sm text-gray-400">{{ matchData.batsmanNonStriker.batRuns }}({{ matchData.batsmanNonStriker.batBalls }}) <span class="text-emerald-400">SR: {{ matchData.batsmanNonStriker.batStrikeRate }}</span></p>
                <p class="text-xs text-gray-500">{{ matchData.batsmanNonStriker.batFours }} fours, {{ matchData.batsmanNonStriker.batSixes }} sixes</p>
              </div>
            </div>
          </div>
          
          <div class="stat-card-highlight">
            <div class="flex items-center justify-between">
              <h3 class="text-sm text-gray-400">Current Bowlers</h3>
              <span class="text-xs px-2 py-1 rounded-full bg-pink-500/20 text-pink-400">Bowling</span>
            </div>
            <div class="grid grid-cols-2 gap-4 mt-2">
              <div>
                <p class="text-white font-semibold mt-1">{{ matchData.bowlerStriker.bowlName }} <span class="text-pink-400">*</span></p>
                <p class="text-sm text-gray-400">{{ matchData.bowlerStriker.bowlWkts }}/{{ matchData.bowlerStriker.bowlRuns }} ({{ matchData.bowlerStriker.bowlOvs }})</p>
                <p class="text-xs text-gray-500">Econ: {{ matchData.bowlerStriker.bowlEcon }}</p>
              </div>
              <div>
                <p class="text-white font-semibold mt-1">{{ matchData.bowlerNonStriker.bowlName }}</p>
                <p class="text-sm text-gray-400">{{ matchData.bowlerNonStriker.bowlWkts }}/{{ matchData.bowlerNonStriker.bowlRuns }} ({{ matchData.bowlerNonStriker.bowlOvs }})</p>
                <p class="text-xs text-gray-500">Econ: {{ matchData.bowlerNonStriker.bowlEcon }}</p>
              </div>
            </div>
          </div>
          
          <div class="stat-card-highlight">
            <div class="flex items-center justify-between">
              <h3 class="text-sm text-gray-400">Recent Performance</h3>
              <span class="text-xs px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-400">Last Few Overs</span>
            </div>
            <div class="space-y-2 mt-2">
              <div v-for="(perf, idx) in matchData.latestPerformance" :key="idx" 
                   class="flex justify-between items-center p-2 rounded bg-slate-700/30">
                <span class="text-white">{{ perf.label }}</span>
                <div>
                  <span class="text-indigo-400 font-medium">{{ perf.runs }} runs</span>
                  <span class="text-gray-400 mx-1">•</span>
                  <span class="text-red-400 font-medium">{{ perf.wkts }} wickets</span>
                </div>
              </div>
              <div class="flex justify-between items-center p-2 rounded bg-indigo-900/30">
                <span class="text-white">Partnership</span>
                <div>
                  <span class="text-indigo-400 font-medium">{{ matchData.partnerShip.runs }} runs</span>
                  <span class="text-gray-400 mx-1">•</span>
                  <span class="text-emerald-400 font-medium">{{ matchData.partnerShip.balls }} balls</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Main Analytics Dashboard -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Over by Over Progress -->
        <div class="stat-card">
          <h3 class="text-lg font-semibold mb-4">Over by Over Analysis</h3>
          <div ref="overAnalysisChart" class="chart-container h-[400px]"></div>
        </div>
        
        <!-- Run Rate Comparison -->
        <div class="stat-card">
          <h3 class="text-lg font-semibold mb-4">Current Run Rate</h3>
          <div ref="runRateChart" class="chart-container h-[400px]"></div>
        </div>
      </div>
      
      <!-- Batsmen & Bowler Quick Stats -->
      <div class="stat-card mt-8">
        <h3 class="text-lg font-semibold mb-4">Batting & Bowling Analysis</h3>
        <div ref="playerComparisonChart" class="chart-container h-[500px]"></div>
      </div>
      
      <!-- Overs Breakdown -->
      <div class="mt-8">
        <h3 class="text-lg font-semibold mb-4">Ball-by-Ball Breakdown</h3>
        
        <div class="bg-slate-800 rounded-lg shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl">
          <div class="p-4 border-b border-slate-700 flex flex-col lg:flex-row justify-between items-center gap-3">
            <div class="flex items-center space-x-3">
              <span class="text-indigo-400 font-semibold">Recent Overs</span>
              <span class="text-sm px-2 py-1 rounded-full bg-slate-700 text-gray-300 whitespace-nowrap">{{ matchData.recentOvsStats }}</span>
            </div>
            <div class="space-x-4 flex">
              <span class="text-sm px-2 py-1 rounded-full bg-indigo-500/20 text-indigo-400">CRR: {{ matchData.currentRunRate }}</span>
              <span v-if="matchData.requiredRunRate > 0" class="text-sm px-2 py-1 rounded-full bg-pink-500/20 text-pink-400">Required RR: {{ matchData.requiredRunRate }}</span>
              <span v-if="matchData.lastWicket" class="text-sm px-2 py-1 rounded-full bg-red-500/20 text-red-400 truncate max-w-[250px]">Last Wicket: {{ matchData.lastWicket.split(" - ")[0] }}</span>
            </div>
          </div>
          
          <div class="p-4">
            <div class="space-y-4 max-h-[400px] overflow-y-auto custom-scrollbar">
              <div v-for="(over, index) in matchData.overSepList.overSep" :key="index" 
                   class="p-4 bg-slate-900 rounded-lg hover:bg-indigo-900/20 transition-colors duration-200">
                <div class="flex justify-between items-center mb-2">
                  <div class="flex items-center">
                    <span class="text-white font-semibold mr-2">Over {{ Math.floor(over.overNum) }}</span>
                    <span class="bg-indigo-500/20 text-indigo-400 text-xs px-2 py-1 rounded-full">{{ getOverRunRate(over) }} RPO</span>
                  </div>
                  <div class="flex items-center space-x-3">
                    <span class="text-xs px-2 py-1 rounded-full" :class="getRunsClass(over.runs)">{{ over.runs }} runs</span>
                    <span class="text-xs px-2 py-1 rounded-full" :class="getWicketsClass(over.o_summary)">
                      {{ getWickets(over.o_summary) }} {{ getWickets(over.o_summary) === 1 ? 'wicket' : 'wickets' }}
                    </span>
                  </div>
                </div>
                
                <div class="flex flex-wrap md:flex-nowrap justify-between items-center mb-3 gap-2">
                  <div class="bg-slate-800/60 px-3 py-2 rounded-lg flex items-center gap-2">
                    <span class="text-sm text-gray-400">Bowler:</span>
                    <span class="text-white">{{ over.ovrBowlNames[0] }}</span>
                    <span class="text-xs ml-2 bg-slate-700 px-2 py-0.5 rounded-full text-gray-300">
                      {{ getRunsPerOver(over) }} RPO
                    </span>
                  </div>
                  <div class="bg-slate-800/60 px-3 py-2 rounded-lg flex items-center gap-2">
                    <span class="text-sm text-gray-400">Score:</span>
                    <span class="text-white">{{ over.score }}/{{ over.wickets }}</span>
                    <span class="text-xs ml-2 bg-slate-700 px-2 py-0.5 rounded-full text-gray-300">
                      {{ (over.score / Math.floor(over.overNum)).toFixed(2) }} RPO (match)
                    </span>
                  </div>
                </div>
                
                <div class="mb-3 p-3 bg-slate-800/30 rounded-lg">
                  <div class="flex flex-wrap gap-2">
                    <div v-for="(event, eventIndex) in over.overSummary.trim().split(' ')" :key="eventIndex"
                        class="w-8 h-8 flex items-center justify-center rounded-full text-sm font-medium" 
                        :class="getBallClass(event)">
                      {{ event }}
                    </div>
                  </div>
                  
                  <div class="mt-3 grid grid-cols-1 md:grid-cols-3 gap-2">
                    <div class="bg-slate-800/50 px-3 py-2 rounded-lg">
                      <div class="text-xs text-gray-400 mb-1">Boundaries</div>
                      <div class="flex items-center justify-between">
                        <span class="text-blue-400 font-medium">{{ getBoundaries(over.o_summary, 4) }} fours</span>
                        <span class="text-purple-400 font-medium">{{ getBoundaries(over.o_summary, 6) }} sixes</span>
                      </div>
                    </div>
                    <div class="bg-slate-800/50 px-3 py-2 rounded-lg">
                      <div class="text-xs text-gray-400 mb-1">Extras</div>
                      <div class="flex items-center justify-between">
                        <span class="text-amber-400 font-medium">{{ getExtras(over.o_summary, 'Wd') }} wides</span>
                        <span class="text-amber-400 font-medium">{{ getExtras(over.o_summary, 'Nb') }} no balls</span>
                      </div>
                    </div>
                    <div class="bg-slate-800/50 px-3 py-2 rounded-lg">
                      <div class="text-xs text-gray-400 mb-1">Dot Balls</div>
                      <div class="flex items-center justify-between">
                        <span class="text-white font-medium">{{ getDots(over.o_summary) }} dots</span>
                        <span class="text-gray-400 font-medium">
                          {{ ((getDots(over.o_summary) / over.o_summary.trim().split(' ').length) * 100).toFixed(0) }}%
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div class="bg-slate-800/40 px-3 py-2 rounded-lg">
                    <div class="text-sm text-gray-400 mb-1">Batsmen</div>
                    <div class="text-white">
                      {{ over.ovrBatNames.join(', ') }}
                    </div>
                  </div>
                  
                  <div v-if="index > 0" class="bg-indigo-900/30 px-3 py-2 rounded-lg">
                    <div class="text-sm text-gray-400 mb-1">Compared to Previous Over</div>
                    <div class="flex items-center justify-between">
                      <span class="text-xs px-2 py-0.5 rounded-full" 
                            :class="getComparisonClass(over.runs - matchData.overSepList.overSep[index-1].runs)">
                        {{ getComparisonPrefix(over.runs - matchData.overSepList.overSep[index-1].runs) }}
                        {{ Math.abs(over.runs - matchData.overSepList.overSep[index-1].runs) }} runs
                      </span>
                      <span class="text-xs px-2 py-0.5 rounded-full" 
                            :class="getComparisonClass(-(getWickets(over.o_summary) - getWickets(matchData.overSepList.overSep[index-1].o_summary)))">
                        {{ getComparisonPrefix(-(getWickets(over.o_summary) - getWickets(matchData.overSepList.overSep[index-1].o_summary))) }}
                        {{ Math.abs(getWickets(over.o_summary) - getWickets(matchData.overSepList.overSep[index-1].o_summary)) }} wickets
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue'
import { echarts, chartConfig } from './chartConfig'

export default {
  name: 'MatchOversAnalysis',
  props: {
    match: {
      type: Object,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  
  setup(props) {
    const matchData = ref(null)
    const overAnalysisChart = ref(null)
    const runRateChart = ref(null)
    const playerComparisonChart = ref(null)
    
    // Chart instances
    let overAnalysisChartInstance = null
    let runRateChartInstance = null
    let playerComparisonChartInstance = null
    
    // Process match data
    const processMatchData = () => {
      if (!props.match?.overs) return null
      return props.match.overs
    }
    
    // Helper function to format date
    const formatDate = (timestamp) => {
      if (!timestamp) return ''
      const date = new Date(timestamp)
      return date.toLocaleDateString('en-US', { 
        day: 'numeric', 
        month: 'short', 
        year: 'numeric' 
      })
    }
    
    // Helper to get class for ball event
    const getBallClass = (event) => {
      if (event === 'W') return 'bg-red-500 text-white font-bold'
      if (event === '4') return 'bg-blue-500 text-white font-bold'
      if (event === '6') return 'bg-purple-500 text-white font-bold'
      if (event === '0') return 'bg-slate-700 text-gray-300'
      if (event.includes('Wd') || event.includes('Nb')) return 'bg-amber-500 text-white'
      return 'bg-slate-600 text-white'
    }

    // Analysis helper functions
    const getWickets = (overSummary) => {
      if (!overSummary) return 0
      return (overSummary.match(/W/g) || []).length
    }

    const getBoundaries = (overSummary, boundaryType) => {
      if (!overSummary) return 0
      const regex = new RegExp(`\\b${boundaryType}\\b`, 'g')
      return (overSummary.match(regex) || []).length
    }

    const getExtras = (overSummary, extraType) => {
      if (!overSummary) return 0
      const regex = new RegExp(extraType, 'g')
      return (overSummary.match(regex) || []).length
    }

    const getDots = (overSummary) => {
      if (!overSummary) return 0
      return (overSummary.match(/\b0\b/g) || []).length
    }

    const getOverRunRate = (over) => {
      return over.runs.toFixed(1)
    }

    const getRunsPerOver = (over) => {
      return over.runs.toFixed(1)
    }

    const getRunsClass = (runs) => {
      if (runs >= 15) return 'bg-emerald-500/20 text-emerald-400'
      if (runs >= 10) return 'bg-indigo-500/20 text-indigo-400'
      if (runs >= 6) return 'bg-blue-500/20 text-blue-400'
      return 'bg-slate-700 text-gray-300'
    }

    const getWicketsClass = (overSummary) => {
      const wickets = getWickets(overSummary)
      if (wickets >= 2) return 'bg-red-500/20 text-red-400'
      if (wickets === 1) return 'bg-pink-500/20 text-pink-400'
      return 'bg-slate-700 text-gray-300'
    }

    const getComparisonClass = (diff) => {
      if (diff > 0) return 'bg-emerald-500/20 text-emerald-400'
      if (diff < 0) return 'bg-red-500/20 text-red-400'
      return 'bg-slate-700 text-gray-300'
    }

    const getComparisonPrefix = (diff) => {
      if (diff > 0) return '+'
      if (diff < 0) return '-'
      return ''
    }

    // Initialize Over Analysis Chart
    const initOverAnalysisChart = () => {
      if (!overAnalysisChart.value || !matchData.value) return
      
      overAnalysisChartInstance = echarts.init(overAnalysisChart.value)
      
      const overs = matchData.value.overSummaryList.slice().reverse()
      const xAxisData = overs.map(over => Math.floor(over.overNum))
      const runsData = overs.map(over => over.runs)
      const wicketsData = overs.map(over => {
        return over.o_summary.includes('W') ? 
          over.o_summary.split(' ').filter(ball => ball === 'W').length : 0
      })
      const scoreData = overs.map(over => over.score)
      
      const option = {
        ...chartConfig,
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: function(params) {
            const overIndex = params[0].dataIndex
            const over = overs[overIndex]
            return `
              <div class="font-semibold text-white">Over ${Math.floor(over.overNum)}</div>
              <div class="mt-1">
                <div class="flex justify-between">
                  <span class="text-gray-300">Runs:</span>
                  <span class="text-indigo-300 font-bold ml-4">${over.runs}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-300">Score:</span>
                  <span class="text-white ml-4">${over.score}/${over.wickets}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-300">Bowler:</span>
                  <span class="text-white ml-4">${over.bowlNames[0]}</span>
                </div>
                <div class="mt-1">
                  <span class="text-gray-300">Ball-by-ball:</span>
                  <div class="text-white mt-1">${over.o_summary}</div>
                </div>
              </div>
            `
          }
        },
        xAxis: {
          type: 'category',
          data: xAxisData,
          name: 'Over',
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
            max: 2,
            ...chartConfig.axisStyle
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
                { offset: 1, color: '#4f46e5' }
              ])
            }
          },
          {
            name: 'Wickets',
            type: 'scatter',
            yAxisIndex: 1,
            data: wicketsData.map((wickets, index) => [index, wickets]),
            symbolSize: 15,
            itemStyle: {
              color: '#ef4444'
            }
          },
          {
            name: 'Score Progression',
            type: 'line',
            smooth: true,
            data: scoreData,
            symbol: 'circle',
            symbolSize: 6,
            lineStyle: {
              color: '#10b981',
              width: 2
            },
            itemStyle: {
              color: '#10b981'
            }
          }
        ],
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        }
      }
      
      overAnalysisChartInstance.setOption(option)
      
      window.addEventListener('resize', () => {
        overAnalysisChartInstance?.resize()
      })
    }
    
    // Initialize Run Rate Chart
    const initRunRateChart = () => {
      if (!runRateChart.value || !matchData.value) return
      
      runRateChartInstance = echarts.init(runRateChart.value)
      
      const gaugeData = [
        {
          value: matchData.value.currentRunRate,
          name: 'Current Run Rate',
          title: {
            offsetCenter: ['0%', '-30%']
          },
          detail: {
            valueAnimation: true,
            offsetCenter: ['0%', '0%']
          }
        }
      ]
      
      // Add required run rate if available
      if (matchData.value.requiredRunRate > 0) {
        gaugeData.push({
          value: matchData.value.requiredRunRate,
          name: 'Required Run Rate',
          title: {
            offsetCenter: ['0%', '30%']
          },
          detail: {
            valueAnimation: true,
            offsetCenter: ['0%', '60%']
          }
        })
      }
      
      const option = {
        ...chartConfig,
        series: [
          {
            type: 'gauge',
            startAngle: 90,
            endAngle: -270,
            pointer: {
              show: false
            },
            progress: {
              show: true,
              overlap: false,
              roundCap: true,
              clip: false,
              itemStyle: {
                borderWidth: 1,
                borderColor: '#464646'
              }
            },
            axisLine: {
              lineStyle: {
                width: 20
              }
            },
            splitLine: {
              show: false,
              distance: 0,
              length: 10
            },
            axisTick: {
              show: false
            },
            axisLabel: {
              show: false,
              distance: 50
            },
            data: gaugeData,
            title: {
              fontSize: 14,
              color: '#94a3b8'
            },
            detail: {
              width: 50,
              height: 14,
              fontSize: 28,
              color: '#fff',
              borderColor: 'auto',
              borderRadius: 3,
              formatter: '{value}',
              valueAnimation: true
            }
          }
        ]
      }
      
      runRateChartInstance.setOption(option)
      
      window.addEventListener('resize', () => {
        runRateChartInstance?.resize()
      })
    }
    
    // Initialize Player Comparison Chart
    const initPlayerComparisonChart = () => {
      if (!playerComparisonChart.value || !matchData.value) return
      
      playerComparisonChartInstance = echarts.init(playerComparisonChart.value)
      
      // Prepare batsmen data
      const strikerBatsman = matchData.value.batsmanStriker
      const nonStrikerBatsman = matchData.value.batsmanNonStriker
      
      // Prepare bowler data
      const strikerBowler = matchData.value.bowlerStriker
      const nonStrikerBowler = matchData.value.bowlerNonStriker
      
      const option = {
        ...chartConfig,
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['Batsmen', 'Bowlers'],
          textStyle: {
            color: '#94a3b8'
          }
        },
        grid: [
          { left: '3%', right: '55%', bottom: '3%', top: '22%', containLabel: true },
          { left: '55%', right: '3%', bottom: '3%', top: '22%', containLabel: true }
        ],
        xAxis: [
          {
            type: 'value',
            gridIndex: 0,
            name: 'Runs/Balls',
            axisLabel: { show: true },
            ...chartConfig.axisStyle
          },
          {
            type: 'value',
            gridIndex: 1,
            name: 'Wickets/Economy',
            ...chartConfig.axisStyle
          }
        ],
        yAxis: [
          {
            type: 'category',
            gridIndex: 0,
            data: [strikerBatsman.batName, nonStrikerBatsman.batName],
            ...chartConfig.axisStyle
          },
          {
            type: 'category',
            gridIndex: 1,
            data: [strikerBowler.bowlName, nonStrikerBowler.bowlName],
            ...chartConfig.axisStyle
          }
        ],
        series: [
          {
            name: 'Runs',
            type: 'bar',
            xAxisIndex: 0,
            yAxisIndex: 0,
            data: [strikerBatsman.batRuns, nonStrikerBatsman.batRuns],
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#4f46e5' },
                { offset: 1, color: '#6366f1' }
              ])
            },
            label: {
              show: true,
              position: 'right',
              formatter: '{c} runs',
              color: '#fff'
            },
            stack: 'batsmen'
          },
          {
            name: 'Balls',
            type: 'bar',
            xAxisIndex: 0,
            yAxisIndex: 0,
            data: [strikerBatsman.batBalls, nonStrikerBatsman.batBalls],
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#0ea5e9' },
                { offset: 1, color: '#38bdf8' }
              ]),
              opacity: 0.5
            },
            label: {
              show: true,
              position: 'right',
              formatter: '{c} balls',
              color: '#94a3b8'
            },
            stack: 'batsmen'
          },
          {
            name: 'Wickets',
            type: 'bar',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: [strikerBowler.bowlWkts, nonStrikerBowler.bowlWkts],
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#ef4444' },
                { offset: 1, color: '#f87171' }
              ])
            },
            label: {
              show: true,
              position: 'right',
              formatter: '{c} wickets',
              color: '#fff'
            }
          },
          {
            name: 'Economy',
            type: 'bar',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: [strikerBowler.bowlEcon, nonStrikerBowler.bowlEcon],
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#f59e0b' },
                { offset: 1, color: '#fbbf24' }
              ]),
              opacity: 0.7
            },
            label: {
              show: true,
              position: 'right',
              formatter: '{c} econ',
              color: '#94a3b8'
            }
          }
        ]
      }
      
      playerComparisonChartInstance.setOption(option)
      
      window.addEventListener('resize', () => {
        playerComparisonChartInstance?.resize()
      })
    }
    
    // Watch for props changes
    watch(() => props.match, () => {
      matchData.value = processMatchData()
      if (matchData.value) {
        initOverAnalysisChart()
        initRunRateChart()
        initPlayerComparisonChart()
      }
    }, { immediate: true })
    
    onMounted(() => {
      matchData.value = processMatchData()
      if (matchData.value) {
        initOverAnalysisChart()
        initRunRateChart()
        initPlayerComparisonChart()
      }
    })
    
    return {
      matchData,
      overAnalysisChart,
      runRateChart,
      playerComparisonChart,
      formatDate,
      getBallClass,
      getWickets,
      getBoundaries,
      getExtras,
      getDots,
      getOverRunRate,
      getRunsPerOver,
      getRunsClass,
      getWicketsClass,
      getComparisonClass,
      getComparisonPrefix
    }
  }
}
</script>

<style scoped>
.stat-card {
  @apply bg-slate-800 rounded-lg shadow-lg p-6 hover:shadow-xl transition-all duration-300;
}

.stat-card-highlight {
  @apply bg-slate-800/75 rounded-lg p-4 transition-all duration-300 hover:bg-slate-700/75;
}

.chart-container {
  width: 100%;
  min-height: 300px;
}

.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #4f46e5 #1e293b;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #1e293b;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #4f46e5;
  border-radius: 20px;
}
</style> 