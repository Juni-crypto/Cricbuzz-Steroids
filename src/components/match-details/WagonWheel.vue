<!-- WagonWheel.vue -->
<template>
  <div class="wagon-wheel">
    <div class="relative w-full h-[400px] bg-green-800 rounded-lg p-4">
      <!-- Cricket ground circle -->
      <div class="absolute inset-4 border-2 border-white rounded-full">
        <!-- 30 yard circle -->
        <div class="absolute inset-8 border-2 border-white/50 rounded-full"></div>
        
        <!-- Boundary sectors -->
        <template v-for="(sector, index) in sectors" :key="index">
          <div class="absolute top-1/2 left-1/2 h-[45%] w-0.5 bg-white/20 origin-bottom"
               :style="{ transform: `translate(-50%, -100%) rotate(${sector.angle}deg)` }">
          </div>
        </template>

        <!-- Shot lines -->
        <div v-for="(shot, index) in shots" :key="index"
             class="absolute top-1/2 left-1/2 h-[45%] origin-bottom group"
             :style="{ transform: `translate(-50%, -100%) rotate(${shot.angle}deg)` }">
          <div class="w-0.5 h-full"
               :class="getShotColor(shot.type)"
               :style="{ height: `${shot.distance}%` }">
            <div class="absolute -top-6 left-1/2 -translate-x-1/2 text-xs text-white opacity-0 group-hover:opacity-100">
              {{ shot.runs }} runs
            </div>
          </div>
        </div>
      </div>

      <!-- Pitch rectangle -->
      <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-64 bg-[#d4b886] border-2 border-white"></div>

      <!-- Legend -->
      <div class="absolute bottom-4 right-4 bg-slate-800/80 p-2 rounded-lg">
        <div class="flex items-center gap-2 text-sm">
          <span class="w-3 h-3 rounded-full bg-red-500"></span>
          <span class="text-white">Six</span>
        </div>
        <div class="flex items-center gap-2 text-sm">
          <span class="w-3 h-3 rounded-full bg-yellow-500"></span>
          <span class="text-white">Four</span>
        </div>
        <div class="flex items-center gap-2 text-sm">
          <span class="w-3 h-3 rounded-full bg-white"></span>
          <span class="text-white">Other</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  shots: {
    type: Array,
    default: () => []
  }
})

// Create 8 sectors for the ground
const sectors = computed(() => {
  return Array.from({ length: 8 }, (_, i) => ({
    angle: (i * 45)
  }))
})

const getShotColor = (type) => {
  switch (type) {
    case 'SIX':
      return 'bg-red-500'
    case 'FOUR':
      return 'bg-yellow-500'
    default:
      return 'bg-white'
  }
}
</script>

<style scoped>
.wagon-wheel {
  perspective: 800px;
}
</style> 