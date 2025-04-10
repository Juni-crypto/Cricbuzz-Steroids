<!-- LiveMatches.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
    <!-- Hero Section -->
    <div class="relative h-[300px] sm:h-[400px] md:h-[500px] overflow-hidden">
      <!-- Animated Background -->
      <div class="absolute inset-0">
        <!-- Grid Pattern -->
        <div class="absolute inset-0 bg-[linear-gradient(to_right,#4f46e520_1px,transparent_1px),linear-gradient(to_bottom,#4f46e520_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_110%)]"></div>
        
        <!-- Animated Gradient Orbs -->
        <div class="absolute top-0 -left-4 w-48 sm:w-72 h-48 sm:h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
        <div class="absolute top-0 -right-4 w-48 sm:w-72 h-48 sm:h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
        <div class="absolute -bottom-8 left-20 w-48 sm:w-72 h-48 sm:h-72 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      <!-- Animated Particles -->
      <div class="absolute inset-0 pointer-events-none">
        <div v-for="n in 20" :key="n" class="particle" :style="{
          top: `${Math.random() * 100}%`,
          left: `${Math.random() * 100}%`,
          animationDelay: `${Math.random() * 5}s`
        }"></div>
      </div>
      
      <!-- Content -->
      <div class="relative h-full flex items-center justify-center px-4 sm:px-6">
        <div class="max-w-4xl mx-auto text-center">
          <!-- Main Title with Split Design -->
          <div class="relative">
            <h1 class="text-4xl sm:text-6xl md:text-8xl font-bold tracking-tight mb-4 sm:mb-6">
              <span class="inline-block transform hover:scale-105 transition-transform cursor-default">
                <span class="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent animate-gradient">
                  Live
                </span>
              </span>
              <span class="inline-block transform hover:scale-105 transition-transform cursor-default ml-2 sm:ml-4">
                <span class="bg-gradient-to-r from-purple-500 to-indigo-500 bg-clip-text text-transparent animate-gradient">
                  Cricket
                </span>
              </span>
            </h1>
            
            <!-- Decorative Line -->
            <div class="w-24 sm:w-32 h-1 bg-gradient-to-r from-blue-500 to-purple-500 mx-auto rounded-full"></div>
          </div>

          <!-- Subtitle with Enhanced Typography -->
          <p class="mt-4 sm:mt-8 text-base sm:text-lg md:text-xl text-slate-300 max-w-2xl mx-auto font-light leading-relaxed px-2">
            Experience cricket like never before with real-time updates and immersive match tracking
          </p>

          <!-- Quick Stats -->
          <div class="mt-6 sm:mt-12 grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-8 max-w-3xl mx-auto px-2">
            <div class="p-3 sm:p-4 rounded-xl bg-slate-800/50 backdrop-blur-sm border border-blue-500/20 hover:border-blue-500/40 transition-colors">
              <div class="text-2xl sm:text-3xl font-bold text-blue-400">{{ liveMatches.length }}</div>
              <div class="text-xs sm:text-sm text-slate-400 mt-1">Live Matches</div>
            </div>
            <div class="p-3 sm:p-4 rounded-xl bg-slate-800/50 backdrop-blur-sm border border-purple-500/20 hover:border-purple-500/40 transition-colors">
              <div class="text-2xl sm:text-3xl font-bold text-purple-400">{{ totalTeams }}</div>
              <div class="text-xs sm:text-sm text-slate-400 mt-1">Active Teams</div>
            </div>
            <div class="p-3 sm:p-4 rounded-xl bg-slate-800/50 backdrop-blur-sm border border-indigo-500/20 hover:border-indigo-500/40 transition-colors">
              <div class="text-2xl sm:text-3xl font-bold text-indigo-400">{{ totalVenues }}</div>
              <div class="text-xs sm:text-sm text-slate-400 mt-1">Venues</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Live Matches Grid -->
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
      <div class="max-w-7xl mx-auto">
        <div :class="[
          'grid gap-4 sm:gap-8',
          liveMatches.length === 1 ? 'grid-cols-1 max-w-2xl mx-auto' :
          liveMatches.length === 2 ? 'grid-cols-1 md:grid-cols-2 max-w-7xl mx-auto' :
          'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3'
        ]">
          <div v-for="match in liveMatches" :key="match.matchInfo.matchId" 
               :class="[
                 'group relative',
                 liveMatches.length === 2 ? 'md:col-span-1' : ''
               ]">
            <!-- Card Container with 3D Transform -->
            <div class="relative rounded-2xl transition-all duration-500 transform perspective-1000 hover:rotate-y-5 hover:scale-105">
              <!-- Card Background -->
              <div class="absolute inset-0 rounded-2xl bg-gradient-to-br from-slate-800 to-slate-900 shadow-xl"></div>
              
              <!-- Live Indicator Border -->
              <div class="absolute -inset-[1px] rounded-2xl bg-gradient-to-r from-blue-500/50 to-purple-500/50 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
              
              <!-- Glass Effect -->
              <div class="absolute inset-0 rounded-2xl backdrop-blur-sm bg-slate-800/40"></div>
              
              <!-- Content -->
              <router-link 
                :to="{ name: 'match-details', params: { id: match.matchInfo.matchId }}"
                class="relative block p-4 sm:p-6"
              >
                <!-- Match Header -->
                <div class="flex items-start justify-between mb-4 sm:mb-6">
                  <div class="space-y-1">
                    <div class="flex items-center gap-2">
                      <span class="flex h-2 w-2 rounded-full bg-blue-500 animate-ping"></span>
                      <span class="text-xs font-medium text-blue-400">LIVE</span>
                    </div>
                    <h3 class="text-xs sm:text-sm font-medium text-slate-300">{{ match.matchInfo.seriesName }}</h3>
                  </div>
                  <span class="text-xs text-slate-500">{{ match.matchInfo.matchDesc }}</span>
                </div>

                <!-- Teams Score Card -->
                <div class="space-y-3 sm:space-y-4">
                  <div v-for="(team, idx) in ['team1', 'team2']" :key="team" 
                       class="relative p-3 sm:p-4 rounded-xl bg-slate-700/50 backdrop-blur-md transition-transform duration-300 hover:scale-105">
                    <div class="flex items-center justify-between">
                      <!-- Team Info -->
                      <div class="flex items-center gap-2 sm:gap-3">
                        <div class="w-8 h-8 sm:w-12 sm:h-12 rounded-full bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center border border-blue-500/20">
                          <span class="text-xs sm:text-sm font-bold text-blue-400">{{ match.matchInfo[team].teamSName }}</span>
                        </div>
                        <span class="text-sm sm:text-base font-medium text-slate-200 truncate max-w-[100px] sm:max-w-[150px]">{{ match.matchInfo[team].teamName }}</span>
                      </div>
                      
                      <!-- Score -->
                      <div class="text-right">
                        <div class="text-lg sm:text-xl font-bold text-white">
                          {{ match.matchScore?.[`${team}Score`]?.inngs1?.runs || 0 }}/{{ match.matchScore?.[`${team}Score`]?.inngs1?.wickets || 0 }}
                        </div>
                        <div class="text-xs sm:text-sm text-slate-400">
                          ({{ match.matchScore?.[`${team}Score`]?.inngs1?.overs || 0 }})
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Match Info Footer -->
                <div class="mt-4 sm:mt-6 pt-3 sm:pt-4 border-t border-slate-700">
                  <p class="text-xs sm:text-sm font-medium text-blue-400">
                    {{ match.matchInfo.status }}
                  </p>
                  <div class="mt-1 sm:mt-2 flex items-center gap-1 sm:gap-2 text-xs text-slate-500">
                    <span class="material-icons-outlined text-xs sm:text-sm">location_on</span>
                    <span class="truncate">{{ match.matchInfo.venueInfo.ground }}, {{ match.matchInfo.venueInfo.city }}</span>
                  </div>
                </div>
              </router-link>
            </div>
          </div>
        </div>

        <!-- No Live Matches Message -->
        <div v-if="liveMatches.length === 0" class="text-center py-8 sm:py-12">
          <div class="inline-block p-6 sm:p-8 rounded-2xl bg-slate-800/50 backdrop-blur-sm border border-blue-500/20">
            <span class="material-icons-outlined text-4xl sm:text-6xl text-blue-400 mb-3 sm:mb-4">sports_cricket</span>
            <h3 class="text-lg sm:text-xl font-medium text-slate-300 mb-2">No Live Matches</h3>
            <p class="text-sm text-slate-500">There are currently no live cricket matches. Check back later!</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import liveData from '../sample-responses/live.json'

const liveMatches = ref([])

// Extract matches from the data
const extractMatches = (data) => {
  const matches = []
  data.typeMatches.forEach(type => {
    type.seriesMatches.forEach(series => {
      if (series.seriesAdWrapper && series.seriesAdWrapper.matches) {
        matches.push(...series.seriesAdWrapper.matches)
      }
    })
  })
  return matches
}

// Compute total teams and venues
const totalTeams = computed(() => {
  const teams = new Set()
  liveMatches.value.forEach(match => {
    teams.add(match.matchInfo.team1.teamId)
    teams.add(match.matchInfo.team2.teamId)
  })
  return teams.size
})

const totalVenues = computed(() => {
  const venues = new Set()
  liveMatches.value.forEach(match => {
    venues.add(match.matchInfo.venueInfo.ground)
  })
  return venues.size
})

// Process match data
const processMatchData = () => {
  liveMatches.value = extractMatches(liveData)
}

// Call processMatchData when component is mounted
onMounted(() => {
  processMatchData()
})
</script>

<style scoped>
.perspective {
  perspective: 2000px;
}

.perspective-1000 {
  perspective: 1000px;
}

.rotate-y-5 {
  transform: rotateY(5deg);
}

.particle {
  position: absolute;
  width: 3px;
  height: 3px;
  background: linear-gradient(to right, #3b82f6, #8b5cf6);
  border-radius: 50%;
  animation: float-random 15s infinite;
  opacity: 0.6;
}

@keyframes float-random {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.6;
  }
  25% {
    transform: translate(100px, -50px) scale(1.2);
    opacity: 0.8;
  }
  50% {
    transform: translate(-50px, 100px) scale(0.8);
    opacity: 0.4;
  }
  75% {
    transform: translate(-100px, -50px) scale(1.2);
    opacity: 0.8;
  }
}

/* Gradient text animation */
.animate-gradient {
  background-size: 200% 200%;
  animation: gradient 8s ease infinite;
}

@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* Blob animation */
@keyframes blob {
  0% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  100% {
    transform: translate(0px, 0px) scale(1);
  }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

/* Add smooth transition for backdrop-filter */
.backdrop-blur-sm {
  transition: all 0.3s ease;
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .particle {
    width: 2px;
    height: 2px;
  }
}
</style> 