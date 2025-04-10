<template>
  <div class="space-y-8">
    <!-- Filters -->
    <div class="bg-gradient-to-r from-slate-800 to-slate-700 rounded-lg p-4 mb-6 shadow-lg">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-bold text-white">Match Highlights</h2>
      </div>
      
      <div class="flex flex-wrap gap-2">
        <button v-for="filter in filtersWithCounts" 
                :key="filter.value" 
                @click="activeFilter = filter.value"
                class="flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-200 border"
                :class="[
                  activeFilter === filter.value 
                  ? 'bg-indigo-700 border-indigo-600 text-white shadow-md' 
                  : 'bg-slate-700/50 border-slate-600/50 text-slate-300 hover:bg-slate-600/50'
                ]">
          <component :is="filter.icon" class="w-4 h-4" />
          <span>{{ filter.label }}</span>
          <span class="bg-slate-800/70 text-xs px-2 py-0.5 rounded-full">{{ filter.count }}</span>
        </button>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
    </div>

    <div v-else-if="filteredHighlights.length === 0" class="bg-gradient-to-br from-slate-800/80 to-slate-900 rounded-lg p-8 text-center shadow-lg border border-slate-700/50">
      <div class="w-20 h-20 mx-auto mb-4 rounded-full bg-slate-700/50 flex items-center justify-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h3 class="text-xl font-bold text-white mb-2">No highlights found</h3>
      <p class="text-slate-400 max-w-md mx-auto">There are no highlights available for the selected filter. Try selecting a different category or check back later.</p>
      <button 
        @click="activeFilter = 'all'" 
        class="mt-6 px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full transition-colors font-medium">
        View All Highlights
      </button>
    </div>

    <!-- Highlights List -->
    <transition-group v-else-if="filteredHighlights.length > 0" name="filter" tag="div" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 grid-masonry">
      <div v-for="(highlight, index) in filteredHighlights" 
           :key="highlight.id"
           :id="`highlight-${highlight.id}`"
           v-scroll-into-view="selectedHighlight && selectedHighlight.id === highlight.id"
           :style="{ 
             '--i': index, 
             gridColumn: selectedHighlight && selectedHighlight.id === highlight.id ? 'span 3' : 'span 1',
             gridRow: selectedHighlight && selectedHighlight.id === highlight.id ? 'span 2' : 'span 1'
           }"
           :class="getCardClasses(highlight)"
           @click="toggleHighlight(highlight)">
        <div class="relative p-5" :class="{ 'expanded-highlight': selectedHighlight && selectedHighlight.id === highlight.id }">
          <!-- Event Badge -->
          <div class="absolute top-0 right-0 -mt-2 -mr-2">
            <span class="px-3 py-1.5 text-xs font-bold rounded-full shadow-lg event-badge"
                  :class="[getEventClass(highlight.event), highlight.event === 'WICKET' ? 'pulse' : '']">
              {{ formatEvent(highlight.event) }}
            </span>
          </div>
          
          <!-- Over Badge -->
          <div class="absolute top-0 left-0 -mt-1 -ml-1">
            <span class="px-2 py-1 bg-slate-600 text-white text-xs font-medium rounded-lg shadow-md">
              Over {{ highlight.overNumber }}
            </span>
          </div>
          
          <!-- Match Context -->
          <div class="pt-6 pb-3">
            <div class="flex items-center space-x-3 mb-2">
              <div class="w-8 h-8 bg-indigo-500/30 rounded-full flex items-center justify-center">
                <span class="text-sm font-bold text-indigo-400">{{ highlight.batTeamName.substring(0, 1) }}</span>
              </div>
              <div>
                <div class="flex items-center space-x-2">
                  <p class="text-white font-medium">{{ highlight.batTeamName }}</p>
                  <div class="h-4 w-px bg-slate-600"></div>
                  <p class="text-sm text-slate-400">Ball {{ highlight.ballNbr }}</p>
                </div>
              </div>
            </div>
            
            <!-- Player Info -->
            <div class="bg-slate-800/50 rounded-lg p-2 mb-3 flex items-center justify-between">
              <div class="text-xs flex items-center">
                <span v-if="getBowlerName(highlight.commText) !== 'Unknown'" class="font-medium text-indigo-400">{{ getBowlerName(highlight.commText) }}</span>
                <span v-else class="font-medium text-indigo-400">Bowler</span>
                <span class="text-slate-400 mx-1">to</span>
                <span v-if="getBatsmanName(highlight.commText) !== 'Unknown'" class="font-medium text-indigo-400">{{ getBatsmanName(highlight.commText) }}</span>
                <span v-else class="font-medium text-indigo-400">Batsman</span>
              </div>
              <div v-if="highlight.event === 'FOUR' || highlight.event === 'SIX'" 
                   class="text-xs font-semibold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400">
                +{{ highlight.event === 'FOUR' ? '4' : '6' }} runs
              </div>
              <div v-else-if="highlight.event === 'WICKET'" 
                   class="text-xs font-semibold px-2 py-0.5 rounded bg-red-500/20 text-red-400">
                WICKET
              </div>
            </div>
            
            <!-- Commentary Text -->
            <div class="bg-gradient-to-r from-slate-800/50 to-transparent rounded-lg p-4">
              <p class="text-slate-300" :class="{ 'line-clamp-2': selectedHighlight && selectedHighlight.id !== highlight.id }">
                {{ formatCommText(highlight.commText, selectedHighlight && selectedHighlight.id !== highlight.id) }}
              </p>
            </div>
          </div>
          
          <!-- Bottom Info -->
          <div class="flex justify-between items-center mt-3 text-xs">
            <div class="text-slate-400">
              {{ formatTimestamp(highlight.timestamp) }}
            </div>
            <div class="flex items-center text-indigo-400 hover:text-indigo-300 transition-colors">
              <span>{{ selectedHighlight && selectedHighlight.id === highlight.id ? 'Collapse' : 'Expand' }}</span>
              <svg v-if="selectedHighlight && selectedHighlight.id !== highlight.id" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 13l-7 7-7-7m14-8l-7 7-7-7" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 11l7-7 7 7M5 19l7-7 7 7" />
              </svg>
            </div>
          </div>
          
          <!-- Special Effects -->
          <div v-if="highlight.event === 'FOUR' || highlight.event === 'SIX'" 
               class="absolute inset-0 bg-gradient-to-r from-indigo-500/5 to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300">
          </div>
          <div v-else-if="highlight.event === 'WICKET'" 
               class="absolute inset-0 bg-gradient-to-r from-red-500/5 to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300">
          </div>
          
          <!-- Expanded Content (Only visible when selected) -->
          <div v-if="selectedHighlight && selectedHighlight.id === highlight.id" class="mt-6 pt-6 border-t border-slate-600/50 expanded-content animate-fade-in">
            <!-- Players Involved Cards -->
            <div class="grid grid-cols-2 gap-4 mb-6">
              <div class="bg-gradient-to-br from-slate-800 to-slate-700 p-4 rounded-lg">
                <div class="flex items-center space-x-3 mb-3">
                  <div class="w-10 h-10 bg-indigo-500/20 rounded-full flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm text-slate-400">Batsman</p>
                    <p v-if="getBatsmanName(highlight.commText) !== 'Unknown'" class="text-lg font-bold text-white">{{ getBatsmanName(highlight.commText) }}</p>
                    <p v-else class="text-lg font-bold text-white">Batsman</p>
                  </div>
                </div>
              </div>
              
              <div class="bg-gradient-to-br from-slate-800 to-slate-700 p-4 rounded-lg">
                <div class="flex items-center space-x-3 mb-3">
                  <div class="w-10 h-10 bg-emerald-500/20 rounded-full flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm text-slate-400">Bowler</p>
                    <p v-if="getBowlerName(highlight.commText) !== 'Unknown'" class="text-lg font-bold text-white">{{ getBowlerName(highlight.commText) }}</p>
                    <p v-else class="text-lg font-bold text-white">Bowler</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Over Stats -->
            <div v-if="highlight.overSeparator" class="bg-gradient-to-br from-indigo-900/30 to-slate-800 p-5 rounded-lg space-y-5 mb-6">
              <div class="flex items-center justify-between">
                <h4 class="text-lg font-bold text-white flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  End of Over {{ Math.floor(highlight.overSeparator.overNum) }}
                </h4>
                <div class="px-3 py-1 bg-indigo-500/30 rounded-full">
                  <p class="text-lg font-bold text-indigo-400">{{ highlight.overSeparator.score }}/{{ highlight.overSeparator.wickets }}</p>
                </div>
              </div>
              
              <div class="grid grid-cols-3 gap-4">
                <div class="text-center p-3 bg-slate-800/50 rounded-lg">
                  <p class="text-sm text-slate-400">Runs in Over</p>
                  <p class="text-2xl font-bold text-white">{{ highlight.overSeparator.runs }}</p>
                </div>
                <div class="text-center p-3 bg-slate-800/50 rounded-lg">
                  <p class="text-sm text-slate-400">Over Summary</p>
                  <p class="text-xl font-medium text-white tracking-wider">{{ highlight.overSeparator.o_summary }}</p>
                </div>
                <div class="text-center p-3 bg-slate-800/50 rounded-lg">
                  <p class="text-sm text-slate-400">Bowler</p>
                  <p class="text-lg font-bold text-white">{{ highlight.overSeparator.bowlNames[0] }}</p>
                  <p class="text-xs text-slate-400">{{ highlight.overSeparator.bowlOvers }}-{{ highlight.overSeparator.bowlMaidens }}-{{ highlight.overSeparator.bowlRuns }}-{{ highlight.overSeparator.bowlWickets }}</p>
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-slate-800/80 p-4 rounded-lg">
                  <div class="flex justify-between items-center mb-2">
                    <div class="flex items-center space-x-2">
                      <div class="w-8 h-8 bg-indigo-500/20 rounded-full flex items-center justify-center">
                        <span class="text-xs font-bold text-indigo-400">{{highlight.overSeparator.batStrikerNames[0].substring(0, 1)}}</span>
                      </div>
                      <p class="font-medium text-white">{{ highlight.overSeparator.batStrikerNames[0] }}</p>
                    </div>
                    <p class="text-lg font-bold text-white">{{ highlight.overSeparator.batStrikerRuns }}
                      <span class="text-sm text-slate-400">({{ highlight.overSeparator.batStrikerBalls }})</span>
                    </p>
                  </div>
                  <div class="h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-indigo-600 to-blue-400" 
                        :style="{width: `${Math.min((highlight.overSeparator.batStrikerRuns / highlight.overSeparator.batStrikerBalls) * 100, 100)}%`}"></div>
                  </div>
                  <div class="flex justify-between mt-2">
                    <p class="text-xs text-slate-400">Strike Rate</p>
                    <p class="text-xs font-medium text-slate-300">
                      {{ ((highlight.overSeparator.batStrikerRuns / highlight.overSeparator.batStrikerBalls) * 100).toFixed(1) }}
                    </p>
                  </div>
                </div>
                
                <div class="bg-slate-800/80 p-4 rounded-lg">
                  <div class="flex justify-between items-center mb-2">
                    <div class="flex items-center space-x-2">
                      <div class="w-8 h-8 bg-indigo-500/20 rounded-full flex items-center justify-center">
                        <span class="text-xs font-bold text-indigo-400">{{highlight.overSeparator.batNonStrikerNames[0].substring(0, 1)}}</span>
                      </div>
                      <p class="font-medium text-white">{{ highlight.overSeparator.batNonStrikerNames[0] }}</p>
                    </div>
                    <p class="text-lg font-bold text-white">{{ highlight.overSeparator.batNonStrikerRuns }}
                      <span class="text-sm text-slate-400">({{ highlight.overSeparator.batNonStrikerBalls }})</span>
                    </p>
                  </div>
                  <div class="h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-indigo-600 to-blue-400" 
                        :style="{width: `${Math.min((highlight.overSeparator.batNonStrikerRuns / highlight.overSeparator.batNonStrikerBalls) * 100, 100)}%`}"></div>
                  </div>
                  <div class="flex justify-between mt-2">
                    <p class="text-xs text-slate-400">Strike Rate</p>
                    <p class="text-xs font-medium text-slate-300">
                      {{ ((highlight.overSeparator.batNonStrikerRuns / highlight.overSeparator.batNonStrikerBalls) * 100).toFixed(1) }}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Formatting Explanation -->
            <div v-if="highlight.commentaryFormats" class="bg-slate-800/50 rounded-lg p-4">
              <h4 class="text-sm font-semibold text-slate-300 mb-2">Special Formatting</h4>
              <div class="space-y-2">
                <div v-for="(format, formatType) in highlight.commentaryFormats" :key="formatType">
                  <div v-for="(value, index) in format.formatValue" :key="index" class="flex items-center space-x-2">
                    <div class="w-2 h-2 rounded-full bg-indigo-500"></div>
                    <p class="text-sm">
                      <span class="text-slate-400">{{ formatType }}:</span>
                      <span class="text-indigo-400 font-medium">{{ value }}</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition-group>

    <!-- Scroll to top button -->
    <div v-if="selectedHighlight" 
         class="fixed bottom-8 right-8 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full p-3 shadow-lg cursor-pointer transition-all duration-300 animate-scale-in z-50"
         @click.stop="scrollToTop">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, h, nextTick } from 'vue'

// Custom directive for smooth scrolling to expanded card
const vScrollIntoView = {
  updated(el, binding) {
    if (binding.value && binding.oldValue !== binding.value) {
      nextTick(() => {
        el.scrollIntoView({
          behavior: 'smooth',
          block: 'center'
        })
      })
    }
  }
}

const props = defineProps({
  match: {
    type: Object,
    required: true
  }
})

// Add the directive to the component
const directives = {
  'scroll-into-view': vScrollIntoView
}

// State
const activeFilter = ref('all')
const selectedHighlight = ref(null)
const isLoading = ref(true)

// Filters
const filters = [
  { 
    label: 'All Highlights', 
    value: 'all',
    icon: {
      render() {
        return h('svg', { 
          xmlns: 'http://www.w3.org/2000/svg', 
          class: 'w-4 h-4', 
          fill: 'none', 
          viewBox: '0 0 24 24', 
          stroke: 'currentColor'
        }, [
          h('path', {
            'stroke-linecap': 'round',
            'stroke-linejoin': 'round',
            'stroke-width': '2',
            d: 'M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z'
          })
        ])
      }
    }
  },
  { 
    label: 'Boundaries', 
    value: 'FOUR',
    icon: {
      render() {
        return h('svg', { 
          xmlns: 'http://www.w3.org/2000/svg', 
          class: 'w-4 h-4', 
          fill: 'none', 
          viewBox: '0 0 24 24', 
          stroke: 'currentColor'
        }, [
          h('path', {
            'stroke-linecap': 'round',
            'stroke-linejoin': 'round',
            'stroke-width': '2',
            d: 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6'
          })
        ])
      }
    }
  },
  { 
    label: 'Sixes', 
    value: 'SIX',
    icon: {
      render() {
        return h('svg', { 
          xmlns: 'http://www.w3.org/2000/svg', 
          class: 'w-4 h-4', 
          fill: 'none', 
          viewBox: '0 0 24 24', 
          stroke: 'currentColor'
        }, [
          h('path', {
            'stroke-linecap': 'round',
            'stroke-linejoin': 'round',
            'stroke-width': '2',
            d: 'M13 10V3L4 14h7v7l9-11h-7z'
          })
        ])
      }
    }
  },
  { 
    label: 'Wickets', 
    value: 'WICKET',
    icon: {
      render() {
        return h('svg', { 
          xmlns: 'http://www.w3.org/2000/svg', 
          class: 'w-4 h-4', 
          fill: 'none', 
          viewBox: '0 0 24 24', 
          stroke: 'currentColor'
        }, [
          h('path', {
            'stroke-linecap': 'round',
            'stroke-linejoin': 'round',
            'stroke-width': '2',
            d: 'M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636'
          })
        ])
      }
    }
  },
  { 
    label: 'End of Over', 
    value: 'over-break',
    icon: {
      render() {
        return h('svg', { 
          xmlns: 'http://www.w3.org/2000/svg', 
          class: 'w-4 h-4', 
          fill: 'none', 
          viewBox: '0 0 24 24', 
          stroke: 'currentColor'
        }, [
          h('path', {
            'stroke-linecap': 'round',
            'stroke-linejoin': 'round',
            'stroke-width': '2',
            d: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z'
          })
        ])
      }
    }
  }
]

// Load data with a slight delay to show loading animation
onMounted(() => {
  setTimeout(() => {
    isLoading.value = false
  }, 800)
})

// Compute highlights with IDs
const highlights = computed(() => {
  if (!props.match || !props.match.matchHighlights) return []
  
  return props.match.matchHighlights.map((highlight, index) => ({
    ...highlight,
    id: `highlight-${index}`,
    overNumber: Math.floor(highlight.ballNbr / 6) + 1
  }))
})

// Filter highlights based on active filter
const filteredHighlights = computed(() => {
  if (activeFilter.value === 'all') {
    return highlights.value
  }
  
  return highlights.value.filter(highlight => {
    if (activeFilter.value === 'over-break') {
      return highlight.overSeparator
    }
    return highlight.event.includes(activeFilter.value)
  })
})

// Compute filters with counts
const filtersWithCounts = computed(() => {
  return filters.map(filter => {
    let count = 0
    
    if (filter.value === 'all') {
      count = highlights.value.length
    } else if (filter.value === 'over-break') {
      count = highlights.value.filter(h => h.overSeparator).length
    } else {
      count = highlights.value.filter(h => h.event.includes(filter.value)).length
    }
    
    return {
      ...filter,
      count
    }
  })
})

// Helper functions
function formatEvent(event) {
  // Prioritize certain events over 'over-break'
  if (['FOUR', 'SIX', 'WICKET'].includes(event)) {
    return event
  }
  
  // For over-break events
  return 'End of Over'
}

function getEventClass(event) {
  if (event === 'FOUR') {
    return 'bg-indigo-600 text-white'
  } else if (event === 'SIX') {
    return 'bg-purple-600 text-white'
  } else if (event === 'WICKET') {
    return 'bg-red-600 text-white'
  } else {
    return 'bg-slate-600 text-white'
  }
}

function formatCommText(text, truncate = true) {
  if (!text) return ''
  
  // Clean the text by removing formatting markers
  let clean = text
    .replace(/\[.*?\]/g, '') // Remove content within square brackets
    .replace(/\{.*?\}/g, '') // Remove content within curly braces
    .trim()
  
  // Truncate if needed
  if (truncate && clean.length > 120) {
    return clean.substring(0, 120) + '...'
  }
  
  return clean
}

function getBowlerName(commText) {
  if (!commText) return 'Unknown'
  
  // Look for common patterns in cricket commentary
  const bowlerPatterns = [
    /^([A-Za-z\s\-'\.]+) to /i,            // "Bowler to Batsman"
    /^([A-Za-z\s\-'\.]+),/i,               // "Bowler, ..."
    /bowled by ([A-Za-z\s\-'\.]+)/i,       // "bowled by Bowler"
    /bowler: ([A-Za-z\s\-'\.]+)/i          // "Bowler: Name"
  ]
  
  for (const pattern of bowlerPatterns) {
    const match = commText.match(pattern)
    if (match && match[1]) {
      return match[1].trim()
    }
  }
  
  // If we couldn't match using patterns, look for capitalized names at the beginning
  const firstWordMatch = commText.match(/^([A-Z][a-z]+(\s[A-Z][a-z]+)?)/)
  if (firstWordMatch && firstWordMatch[1]) {
    return firstWordMatch[1].trim()
  }
  
  return 'Unknown'
}

function getBatsmanName(commText) {
  if (!commText) return 'Unknown'
  
  // Look for common patterns in cricket commentary
  const batsmanPatterns = [
    /to ([A-Za-z\s\-'\.]+),/i,              // "Bowler to Batsman,"
    /to ([A-Za-z\s\-'\.]+)\./i,              // "Bowler to Batsman."
    /batsman: ([A-Za-z\s\-'\.]+)/i,         // "Batsman: Name"
    /([A-Za-z\s\-'\.]+) is out/i,           // "Batsman is out"
    /([A-Za-z\s\-'\.]+) tries to/i          // "Batsman tries to"
  ]
  
  for (const pattern of batsmanPatterns) {
    const match = commText.match(pattern)
    if (match && match[1]) {
      return match[1].trim()
    }
  }
  
  // If we got the bowler's name and there's "to" in the text, try to get the text after "to"
  const bowlerToBatsman = commText.match(/^[A-Za-z\s\-'\.]+\sto\s([A-Za-z\s\-'\.]+)/)
  if (bowlerToBatsman && bowlerToBatsman[1]) {
    // Clean up and return just the name part
    return bowlerToBatsman[1].split(/[,.\s]/)[0].trim()
  }
  
  return 'Unknown'
}

function formatTimestamp(timestamp) {
  if (!timestamp) return ''
  
  const date = new Date(timestamp)
  
  const time = date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  })
  
  const day = date.toLocaleDateString('en-US', {
    day: 'numeric',
    month: 'short'
  })
  
  return `${time} · ${day}`
}

// Keyboard event handler
const handleKeydown = (event) => {
  if (event.key === 'Escape' && selectedHighlight.value) {
    selectedHighlight.value = null
  }
}

// Lifecycle
onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
  setTimeout(() => {
    isLoading.value = false
  }, 800)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})

// Toggle highlight with improved scrolling behavior
const toggleHighlight = (highlight) => {
  // If clicking the same highlight, toggle it off
  if (selectedHighlight.value && selectedHighlight.value.id === highlight.id) {
    selectedHighlight.value = null
  } else {
    // Set the new highlight with a deep clone to ensure reactivity
    selectedHighlight.value = JSON.parse(JSON.stringify(highlight))
  }
}

// Add class when a card is expanded
const getCardClasses = (highlight) => {
  const isExpanded = selectedHighlight.value && selectedHighlight.value.id === highlight.id;
  
  return {
    'bg-gradient-to-br': true,
    'from-slate-700 to-slate-800': !isExpanded,
    'from-slate-600 to-slate-700': isExpanded,
    'hover:from-slate-600 hover:to-slate-700': true,
    'rounded-lg': true,
    'overflow-hidden': true,
    'shadow-md': !isExpanded,
    'shadow-xl': isExpanded,
    'transition-all': true,
    'duration-500': true,
    'cursor-pointer': true,
    'card-enter-active': true,
    'expanded-card': isExpanded,
    'z-30': isExpanded
  }
}

// Scroll to top function
const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}
</script>

<style scoped>
@import './styles.css';

.hide-scrollbar {
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.hide-scrollbar::-webkit-scrollbar {
  display: none;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.highlight-card {
  @apply bg-gradient-to-br from-slate-800/80 to-slate-900 border border-slate-700 
         transition-all duration-300 shadow-md;
  min-height: 220px;
}

.highlight-card:hover {
  @apply border-indigo-500/70 shadow-lg shadow-indigo-900/20;
}

.stat-card {
  @apply bg-slate-800/50 rounded-lg p-3 border border-slate-700;
}

.filter-enter-active,
.filter-leave-active {
  transition: all 0.3s ease;
}
.filter-enter-from,
.filter-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.card-enter-active {
  transition: all 0.3s ease;
  transition-delay: calc(var(--i) * 0.05s);
}
.card-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.animate-scale-in {
  animation: scale-in 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}

@keyframes scale-in {
  0% {
    opacity: 0;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* Badge hover animations */
.event-badge {
  transition: all 0.2s ease;
}
.event-badge:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Loading animation */
.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Pulse animation for wicket badge */
.pulse {
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(220, 38, 38, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(220, 38, 38, 0);
  }
}

.getEventClass-FOUR {
  @apply bg-indigo-500 text-white;
}

.getEventClass-SIX {
  @apply bg-purple-600 text-white;
}

.getEventClass-WICKET {
  @apply bg-red-600 text-white;
}

.getEventClass-over-break {
  @apply bg-emerald-600 text-white;
}

/* Expanded content animations */
.expanded-content {
  animation: expandContent 0.4s ease-out forwards;
  transform-origin: top center;
  opacity: 0;
}

@keyframes expandContent {
  0% {
    opacity: 0;
    max-height: 0;
    transform: translateY(-20px);
  }
  100% {
    opacity: 1;
    max-height: 1000px;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(-10px) scale(0.98);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Masonry grid adjustments */
@media (min-width: 768px) {
  .grid-masonry {
    grid-auto-flow: dense;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    grid-auto-rows: minmax(200px, auto);
    gap: 1rem;
  }
  
  .expanded-card {
    z-index: 20;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
    transform: translateZ(0);
    grid-row: span 2;
    grid-column: span 3;
  }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}
</style> 