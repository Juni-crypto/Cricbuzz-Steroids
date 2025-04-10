<template>
  <div class="space-y-8">
    <!-- Commentary Controls -->
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-4">
        <button v-for="filter in filters"
                :key="filter.value"
                @click="activeFilter = filter.value"
                class="px-3 py-1.5 text-sm font-medium rounded-full transition-colors"
                :class="[
                  activeFilter === filter.value
                    ? 'bg-indigo-500 text-white'
                    : 'text-slate-400 hover:text-slate-300'
                ]">
          {{ filter.label }}
        </button>
      </div>
      <div class="flex items-center space-x-2">
        <button @click="autoScroll = !autoScroll"
                class="px-3 py-1.5 text-sm font-medium rounded-full transition-colors"
                :class="autoScroll ? 'bg-emerald-500 text-white' : 'text-slate-400 hover:text-slate-300'">
          <span class="flex items-center space-x-1">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13l-3 3m0 0l-3-3m3 3V8m0 13a9 9 0 110-18 9 9 0 010 18z" />
            </svg>
            <span>Auto-scroll</span>
          </span>
        </button>
        <button @click="isFullScreen = !isFullScreen"
                class="p-1.5 text-slate-400 hover:text-slate-300 transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="isFullScreen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 9L4 4m0 0l5 5m-5-5v6m16-6l-5 5m5-5v6m-5 5l5 5m-5-5h6M4 20l5-5m-5 5v-6" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5v-4m0 4h-4m4 0l-5-5" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Commentary Feed -->
    <div ref="commentaryFeed"
         class="space-y-4 transition-all overflow-y-auto overflow-x-hidden scroll-smooth commentary-feed"
         :class="{ 'h-[calc(100vh-12rem)]': isFullScreen, 'h-[32rem]': !isFullScreen }"
         @scroll="handleScroll">
      <div v-for="(commentary, index) in filteredCommentary"
           :key="commentary.timestamp"
           class="p-4 rounded-lg transition-all transform"
           :class="getCommentaryClass(commentary)">
        <!-- Over Number -->
        <div class="flex items-center justify-between mb-2">
          <span v-if="commentary.ballNbr" class="text-sm font-medium px-2 py-0.5 rounded bg-slate-700">
            Over {{ (commentary.overNumber || (commentary.ballNbr/6).toFixed(1)) || '-' }}
          </span>
          <span class="text-sm text-slate-400">
            {{ formatTimestamp(commentary.timestamp) }}
          </span>
        </div>

        <!-- Commentary Content -->
        <div class="space-y-2">
          <p class="text-sm leading-relaxed break-words whitespace-pre-wrap max-w-full"
             :class="getTextClass(commentary)">
            {{ commentary.commText }}
          </p>

          <!-- Additional Info -->
          <div v-if="commentary.overSeparator"
               class="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-3 pt-3 border-t border-slate-700">
            <div class="text-center">
              <p class="text-sm text-slate-400 truncate">Score</p>
              <p class="text-lg font-semibold truncate">{{ commentary.overSeparator.score }}/{{ commentary.overSeparator.wickets }}</p>
            </div>
            <div class="text-center">
              <p class="text-sm text-slate-400 truncate">Batsman</p>
              <p class="text-lg font-semibold truncate">{{ commentary.overSeparator.batStrikerNames?.[0] }}</p>
              <p class="text-sm text-slate-400">{{ commentary.overSeparator.batStrikerRuns }}({{ commentary.overSeparator.batStrikerBalls }})</p>
            </div>
            <div class="text-center">
              <p class="text-sm text-slate-400 truncate">Over Summary</p>
              <p class="text-lg font-semibold truncate">{{ commentary.overSeparator.o_summary }}</p>
            </div>
            <div class="text-center">
              <p class="text-sm text-slate-400 truncate">Bowler</p>
              <p class="text-lg font-semibold truncate">{{ commentary.overSeparator.bowlNames?.[0] }}</p>
              <p class="text-sm text-slate-400">{{ commentary.overSeparator.bowlOvers }}-{{ commentary.overSeparator.bowlMaidens }}-{{ commentary.overSeparator.bowlRuns }}-{{ commentary.overSeparator.bowlWickets }}</p>
            </div>
          </div>

          <!-- Commentary Formats if any -->
          <div v-if="commentary.commentaryFormats?.bold" class="mt-2">
            <p v-for="(value, index) in commentary.commentaryFormats.bold.formatValue" 
               :key="index"
               class="text-sm font-bold text-slate-300">
              {{ value }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading"
         class="flex items-center justify-center py-4">
      <svg class="w-6 h-6 animate-spin text-indigo-500" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'

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

// State
const activeFilter = ref('all')
const autoScroll = ref(true)
const isFullScreen = ref(false)
const isLoading = computed(() => props.loading)
const commentaryFeed = ref(null)

// Filters - Updated to match actual events in the JSON
const filters = [
  { label: 'All', value: 'all' },
  { label: 'Wickets', value: 'WICKET' },
  { label: 'Boundaries', value: 'BOUNDARY' },
  { label: 'Milestones', value: 'FIFTY' }
]

// Helper Methods
const formatTimestamp = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('en-US', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: false 
  })
}

const getCommentaryClass = (commentary) => {
  const baseClasses = 'border'
  if (commentary.event === 'WICKET') return `${baseClasses} bg-red-500/10 border-red-500/20`
  if (['FOUR', 'SIX'].includes(commentary.event)) return `${baseClasses} bg-indigo-500/10 border-indigo-500/20`
  if (['FIFTY', 'HUNDRED'].includes(commentary.event)) return `${baseClasses} bg-emerald-500/10 border-emerald-500/20`
  return 'bg-slate-800/50'
}

const getTextClass = (commentary) => {
  if (commentary.event === 'WICKET') return 'text-red-400'
  if (['FOUR', 'SIX'].includes(commentary.event)) return 'text-indigo-400'
  if (['FIFTY', 'HUNDRED'].includes(commentary.event)) return 'text-emerald-400'
  return 'text-slate-300'
}

// Computed
const commentary = computed(() => {
  if (!props.match?.commentary?.commentaryList) return []
  return [...props.match.commentary.commentaryList].reverse()
})

const filteredCommentary = computed(() => {
  if (activeFilter.value === 'all') {
    return commentary.value
  }
  if (activeFilter.value === 'BOUNDARY') {
    return commentary.value.filter(c => ['FOUR', 'SIX'].includes(c.event))
  }
  return commentary.value.filter(c => c.event === activeFilter.value)
})

// Methods
const handleScroll = () => {
  if (!commentaryFeed.value) return
  
  const { scrollTop, scrollHeight, clientHeight } = commentaryFeed.value
  const atBottom = scrollHeight - scrollTop === clientHeight
  
  if (!atBottom) {
    autoScroll.value = false
  }
}

const scrollToBottom = () => {
  if (!commentaryFeed.value || !autoScroll.value) return
  
  const feed = commentaryFeed.value
  const targetScroll = feed.scrollHeight - feed.clientHeight
  
  feed.scrollTo({
    top: targetScroll,
    behavior: 'smooth'
  })
}

// Watch for new commentary
watch(commentary, () => {
  if (autoScroll.value) {
    nextTick(scrollToBottom)
  }
}, { deep: true })

// Lifecycle
onMounted(() => {
  scrollToBottom()
})
</script>

<style scoped>
.scroll-smooth {
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch; /* For iOS devices */
}

.commentary-feed {
  scrollbar-width: thin;
  scrollbar-color: theme('colors.slate.600') theme('colors.slate.800');
  will-change: transform; /* Optimize performance */
  backface-visibility: hidden; /* Reduce visual artifacts */
}

.commentary-feed::-webkit-scrollbar {
  width: 6px;
}

.commentary-feed::-webkit-scrollbar-track {
  background: theme('colors.slate.800');
}

.commentary-feed::-webkit-scrollbar-thumb {
  background-color: theme('colors.slate.600');
  border-radius: 3px;
}

/* Add transition for new items */
.commentary-feed > div {
  transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out;
}

/* Optimize animations */
@media (prefers-reduced-motion: no-preference) {
  .commentary-feed {
    scroll-behavior: smooth;
  }
}

/* Improve touch scrolling on mobile */
@supports (-webkit-overflow-scrolling: touch) {
  .commentary-feed {
    -webkit-overflow-scrolling: touch;
  }
}
</style> 