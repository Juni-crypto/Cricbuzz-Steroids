<!-- App.vue -->
<template>
  <div class="min-h-screen flex flex-col bg-slate-900">
    <!-- Header -->
    <header class="bg-gradient-to-r from-slate-800/80 to-slate-900/80 backdrop-blur-md border-b border-slate-700/50 sticky top-0 z-50 shadow-lg">
      <nav class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <router-link to="/" class="group">
            <span class="text-xl md:text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent hover:from-blue-300 hover:to-purple-400 transition-all duration-300">
              Chumaoruworks
            </span>
          </router-link>
          
          <!-- Desktop Navigation -->
          <div class="hidden md:flex items-center space-x-4 lg:space-x-8">
            <router-link 
              v-for="route in routes" 
              :key="route.path"
              :to="route.path"
              class="relative px-3 py-2 text-slate-300 hover:text-white transition-colors group"
            >
              <span class="relative z-10">{{ route.name }}</span>
              <span class="absolute inset-0 bg-gradient-to-r from-blue-500/0 to-purple-500/0 group-hover:from-blue-500/10 group-hover:to-purple-500/10 rounded-lg transition-all duration-300"></span>
            </router-link>
          </div>
          
          <!-- Mobile Menu Button -->
          <button 
            @click="isMobileMenuOpen = !isMobileMenuOpen" 
            class="md:hidden text-slate-300 hover:text-white focus:outline-none"
            aria-label="Toggle menu"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="!isMobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <!-- Mobile Navigation -->
        <div 
          v-if="isMobileMenuOpen" 
          class="md:hidden mt-4 py-2 border-t border-slate-700/50"
        >
          <router-link 
            v-for="route in routes" 
            :key="route.path"
            :to="route.path"
            class="block px-3 py-2 text-slate-300 hover:text-white hover:bg-slate-800/50 rounded-lg transition-colors"
            @click="isMobileMenuOpen = false"
          >
            {{ route.name }}
          </router-link>
        </div>
      </nav>
    </header>

    <!-- Main Content -->
    <main class="flex-grow relative">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <footer class="bg-gradient-to-r from-slate-800/80 to-slate-900/80 backdrop-blur-md border-t border-slate-700/50 mt-auto">
      <div class="container mx-auto px-4 py-4">
        <p class="text-center text-slate-400 text-xs sm:text-sm">
          © 2024 Chumaoruworks. All rights reserved.
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isMobileMenuOpen = ref(false);

const routes = [
  { path: '/matches', name: 'Matches' },
  { path: '/teams', name: 'Teams' },
  { path: '/players', name: 'Players' },
  { path: '/venues', name: 'Venues' },
  { path: '/compare', name: 'Compare' },
  { path: '/statistics', name: 'Statistics' }
]
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Ensure the main content takes up at least the full viewport height */
main {
  min-height: calc(100vh - 64px - 48px); /* viewport height - header - footer */
}

/* Fix any z-index issues */
.modal {
  z-index: 1000;
}

/* Ensure proper stacking context */
.backdrop-blur-md {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: theme('colors.slate.800');
}

::-webkit-scrollbar-thumb {
  background: theme('colors.slate.600');
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: theme('colors.slate.500');
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .container {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  main {
    min-height: calc(100vh - 56px - 40px); /* Adjusted for smaller header/footer on mobile */
  }
}

/* Ensure proper touch targets on mobile */
@media (max-width: 768px) {
  button, a {
    min-height: 44px; /* Minimum touch target size */
    min-width: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style> 