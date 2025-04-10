import * as echarts from 'echarts/core'
import { 
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import { 
  LineChart,
  BarChart,
  PieChart,
  RadarChart,
  ScatterChart,
  SunburstChart,
  SankeyChart,
  TreemapChart,
  GaugeChart
} from 'echarts/charts'
import { UniversalTransition } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'

// Register ECharts components
echarts.use([
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  LineChart,
  BarChart,
  PieChart,
  RadarChart,
  ScatterChart,
  SunburstChart,
  SankeyChart,
  TreemapChart,
  GaugeChart,
  CanvasRenderer,
  UniversalTransition
])

// Common chart configuration
export const chartConfig = {
  backgroundColor: 'transparent',
  textStyle: {
    color: '#94a3b8'
  },
  axisStyle: {
    axisLine: {
      lineStyle: {
        color: '#334155'
      }
    },
    axisTick: {
      lineStyle: {
        color: '#334155'
      }
    },
    splitLine: {
      lineStyle: {
        color: '#334155'
      }
    },
    axisLabel: {
      color: '#94a3b8'
    }
  },
  tooltip: {
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    borderColor: '#6366f1'
  }
}

// Helper functions
export const generateRandomData = (count, min, max) => {
  return Array.from({ length: count }, () => 
    Math.floor(Math.random() * (max - min + 1)) + min
  )
}

export const calculateRoleDistribution = (players) => {
  return players.reduce((acc, player) => {
    if (!player.substitute) {
      acc[player.role] = (acc[player.role] || 0) + 1
    }
    return acc
  }, {})
}

export const generatePlayerRatings = () => {
  return Array.from({ length: 5 }, () => Math.floor(Math.random() * 5) + 5)
}

export const formatCommentary = (text) => {
  return text.replace(/B0\$(.*?)B0\$/g, '<span class="font-bold"  >$1</span>')
}

export { echarts } 