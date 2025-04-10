<!-- PitchMap.vue -->
<template>
  <div class="pitch-map">
    <!-- Filters -->
    <div class="mb-4 flex flex-col sm:flex-row gap-4 justify-between bg-slate-800/50 p-3 rounded-lg border border-slate-700">
      <!-- Bowler filter -->
      <div class="flex-1">
        <label class="block text-sm text-slate-300 mb-1">Bowler</label>
        <select v-model="selectedBowler" class="w-full bg-slate-700 border border-slate-600 rounded-md p-2 text-slate-200 text-sm">
          <option value="all">All Bowlers</option>
          <option v-for="bowler in uniqueBowlers" :key="bowler" :value="bowler">{{ bowler }}</option>
        </select>
      </div>
      
      <!-- Delivery type filter -->
      <div class="flex-1">
        <label class="block text-sm text-slate-300 mb-1">Delivery Type</label>
        <div class="flex flex-wrap gap-2">
          <button 
            v-for="type in deliveryTypes" 
            :key="type.value"
            @click="toggleDeliveryType(type.value)"
            class="px-3 py-1 text-xs rounded-full transition-colors border flex items-center gap-1"
            :class="selectedDeliveryTypes.includes(type.value) ? 
              'bg-opacity-70 border-opacity-70 ' + type.activeClass : 
              'bg-slate-700 border-slate-600 text-slate-400'"
          >
            <span class="w-2 h-2 rounded-full" :class="type.dotClass"></span>
            {{ type.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Pitch map display -->
    <div class="relative w-full h-[400px] bg-green-800 rounded-lg p-4">
      <!-- Pitch area -->
      <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-24 h-96 bg-[#d4b886] border-2 border-white">
        <!-- Crease lines -->
        <div class="absolute top-8 left-0 right-0 h-0.5 bg-white"></div>
        <div class="absolute bottom-8 left-0 right-0 h-0.5 bg-white"></div>
        <div class="absolute top-8 bottom-8 left-1/2 w-0.5 bg-white"></div>
      </div>

      <!-- Ball landing spots -->
      <div v-for="(delivery, index) in filteredDeliveries" :key="index"
           class="absolute w-3 h-3 rounded-full transform -translate-x-1/2 -translate-y-1/2 transition-opacity hover:opacity-80"
           :class="[getBallColor(delivery.type), 'group']"
           :style="{ left: `${delivery.displayX}%`, top: `${delivery.displayY}%` }">
        <!-- Tooltip -->
        <div class="absolute -top-8 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-xs px-2 py-1 rounded invisible group-hover:visible whitespace-nowrap z-10">
          {{ delivery.bowler }}: {{ delivery.speed }}kmph
        </div>
      </div>

      <!-- Legend -->
      <div class="absolute bottom-4 right-4 bg-slate-800/80 p-2 rounded-lg">
        <div class="flex items-center gap-2 text-sm">
          <span class="w-3 h-3 rounded-full bg-red-500"></span>
          <span class="text-white">Wicket</span>
        </div>
        <div class="flex items-center gap-2 text-sm">
          <span class="w-3 h-3 rounded-full bg-yellow-500"></span>
          <span class="text-white">Boundary</span>
        </div>
        <div class="flex items-center gap-2 text-sm">
          <span class="w-3 h-3 rounded-full bg-blue-500"></span>
          <span class="text-white">Dot Ball</span>
        </div>
        <div class="flex items-center gap-2 text-sm">
          <span class="w-3 h-3 rounded-full bg-white"></span>
          <span class="text-white">Regular</span>
        </div>
      </div>
      
      <!-- Filter applied notice -->
      <div v-if="isFiltered" class="absolute top-4 left-4 bg-indigo-500/80 text-white text-xs px-2 py-1 rounded-md">
        Filters Applied
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  deliveries: {
    type: Array,
    default: () => []
  }
})

// Filter states
const selectedBowler = ref('all')
const selectedDeliveryTypes = ref(['WICKET', 'BOUNDARY', 'DOT', 'REGULAR'])

// Calculated values
const uniqueBowlers = computed(() => {
  return [...new Set(props.deliveries.map(d => d.bowler))].sort()
})

const deliveryTypes = [
  { label: 'Wickets', value: 'WICKET', activeClass: 'bg-red-500 border-red-300', dotClass: 'bg-red-500' },
  { label: 'Boundaries', value: 'BOUNDARY', activeClass: 'bg-yellow-500 border-yellow-300', dotClass: 'bg-yellow-500' },
  { label: 'Dot Balls', value: 'DOT', activeClass: 'bg-blue-500 border-blue-300', dotClass: 'bg-blue-500' },
  { label: 'Regular', value: 'REGULAR', activeClass: 'bg-white border-gray-300', dotClass: 'bg-white' }
]

// Toggle delivery type selection
const toggleDeliveryType = (type) => {
  if (selectedDeliveryTypes.value.includes(type)) {
    // Don't allow deselecting the last type
    if (selectedDeliveryTypes.value.length > 1) {
      selectedDeliveryTypes.value = selectedDeliveryTypes.value.filter(t => t !== type)
    }
  } else {
    selectedDeliveryTypes.value.push(type)
  }
}

// Calculate if filters are applied
const isFiltered = computed(() => {
  return selectedBowler.value !== 'all' || selectedDeliveryTypes.value.length !== deliveryTypes.length
})

// Calculate display coordinates for the balls on the pitch and apply filters
const filteredDeliveries = computed(() => {
  return props.deliveries
    .filter(delivery => {
      // Apply bowler filter
      const bowlerMatch = selectedBowler.value === 'all' || delivery.bowler === selectedBowler.value
      
      // Apply delivery type filter
      const typeMatch = selectedDeliveryTypes.value.includes(delivery.type)
      
      return bowlerMatch && typeMatch
    })
    .map(delivery => {
      // Convert the x and y coordinates (-1 to 1) to percentages for the pitch display
      // Horizontal: Map from -1...1 to 35%...65% (centered on the pitch)
      // Vertical: Map from 0...2 to 20%...80% (length of the pitch)
      const displayX = 50 + (delivery.x * 15); // Center is 50%, scale by 15% in each direction
      const displayY = 20 + (delivery.y * 30); // Top is 20%, bottom is 80%, scale accordingly
      
      return {
        ...delivery,
        displayX,
        displayY
      };
    });
})

const getBallColor = (type) => {
  switch (type) {
    case 'WICKET':
      return 'bg-red-500'
    case 'BOUNDARY':
      return 'bg-yellow-500'
    case 'DOT':
      return 'bg-blue-500'
    default:
      return 'bg-white'
  }
}
</script>

<style scoped>
.pitch-map {
  perspective: 800px;
}
/* Add hover effect for the balls */
.rounded-full {
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
  z-index: 1;
}
/* Filter button transitions */
button {
  transition: all 0.2s ease;
}
button:hover {
  transform: translateY(-1px);
}
</style> 