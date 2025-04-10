<!-- LiveMatches.vue -->
<template>
  <div class="min-h-screen bg-gradient-to-b from-[#0B1221] to-[#0A1A2F] text-white overflow-hidden">
    <!-- Hero Section -->
    <div class="hero-section">
      <!-- Background Elements -->
      <div class="hero-background">
        <div class="cricket-field">
          <div class="field-lines"></div>
          <div class="floating-balls"></div>
          <div class="field-glow"></div>
    </div>
      </div>

      <!-- Hero Content -->
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">
            <span class="text-gradient">Live Cricket</span>
            <span class="text-outline">Experience</span>
          </h1>
          <p class="hero-subtitle">Real-time cricket updates at your fingertips</p>
        </div>

        <!-- Enhanced Stats Grid -->
        <div class="stats-container">
          <div class="stats-grid">
            <div v-for="(stat, index) in stats" :key="index" class="stat-card" :style="{ '--delay': `${index * 0.1}s` }">
              <div class="stat-card-content">
                <div class="stat-value">{{ stat.value }}</div>
                <div class="stat-label">{{ stat.label }}</div>
                <div class="stat-decoration">
                  <div class="decoration-dot"></div>
                  <div class="decoration-line"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Team Credit -->
        <div class="team-credit">
          <div class="credit-badge">
            <span class="credit-text">Crafted with passion by</span>
            <span class="team-name">Chumaoruworks</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Completely Redesigned Live Matches Section -->
    <div class="matches-section">
      <div class="matches-container">
        <!-- Section Header -->
        <div class="section-header">
          <div class="header-left">
            <h2 class="section-title">Live Matches</h2>
            <p class="section-subtitle">Watch the action unfold in real-time</p>
          </div>
          <div class="header-right">
            <div class="live-indicator">
              <span class="live-dot"></span>
              <span class="live-text">LIVE NOW</span>
            </div>
          </div>
        </div>
        
        <!-- Stadium Background -->
        <div class="stadium-background">
          <div class="stadium-lights left"></div>
          <div class="stadium-lights right"></div>
          <div class="stadium-field"></div>
        </div>

        <!-- Live Matches Carousel -->
        <div class="matches-carousel">
          <div v-for="match in liveMatches" :key="match.matchInfo.matchId" class="match-card">
            <!-- Match Status Banner -->
            <div class="match-banner">
              <div class="series-info">{{ match.matchInfo.seriesName }}</div>
              <div class="match-stage">{{ match.matchInfo.matchDesc }}</div>
              <div class="match-status-pill">
                <span class="pulse-dot"></span>
                <span>LIVE</span>
              </div>
            </div>
            
            <!-- Teams Scoreboard -->
            <div class="scoreboard">
              <!-- Team 1 -->
              <div class="team-side">
                <div class="team-identity">
                  <div class="team-flag">
                    <img :src="getTeamImage(match.matchInfo.team1.imageId)" 
                         :alt="match.matchInfo.team1.teamName"
                         class="team-logo">
                  </div>
                  <div class="team-details">
                    <div class="team-name">{{ match.matchInfo.team1.teamName }}</div>
                    <div class="team-short">{{ match.matchInfo.team1.teamSName }}</div>
                  </div>
                </div>
                <div class="team-score">
                  <div class="score">
                    {{ match.matchScore?.team1Score?.inngs1?.runs || 0 }}
                    <span class="wickets">/{{ match.matchScore?.team1Score?.inngs1?.wickets || 0 }}</span>
                  </div>
                  <div class="overs">({{ match.matchScore?.team1Score?.inngs1?.overs || 0 }})</div>
                </div>
              </div>
              
              <!-- VS Divider -->
              <div class="vs-divider">
                <div class="vs-line"></div>
                <div class="vs-text">VS</div>
                <div class="vs-line"></div>
              </div>
              
              <!-- Team 2 -->
              <div class="team-side">
                <div class="team-identity">
                  <div class="team-flag">
                    <img :src="getTeamImage(match.matchInfo.team2.imageId)" 
                         :alt="match.matchInfo.team2.teamName"
                         class="team-logo">
                  </div>
                  <div class="team-details">
                    <div class="team-name">{{ match.matchInfo.team2.teamName }}</div>
                    <div class="team-short">{{ match.matchInfo.team2.teamSName }}</div>
                  </div>
                </div>
                <div class="team-score">
                  <div class="score">
                    {{ match.matchScore?.team2Score?.inngs1?.runs || 0 }}
                    <span class="wickets">/{{ match.matchScore?.team2Score?.inngs1?.wickets || 0 }}</span>
                  </div>
                  <div class="overs">({{ match.matchScore?.team2Score?.inngs1?.overs || 0 }})</div>
                </div>
              </div>
            </div>
            
            <!-- Match Info Footer -->
            <div class="match-footer">
              <div class="match-venue">
                <svg viewBox="0 0 24 24" class="venue-icon" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                <span>{{ match.matchInfo.venueInfo.ground }}, {{ match.matchInfo.venueInfo.city }}</span>
              </div>
              <div class="match-result-status">{{ match.matchInfo.status }}</div>
              <button class="watch-button">
                <span class="watch-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </span>
                <span>Watch</span>
              </button>
            </div>
          </div>
          
          <!-- No Matches State -->
          <div v-if="liveMatches.length === 0" class="no-matches-card">
            <div class="empty-state-content">
              <div class="empty-icon-container">
                <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" 
                        d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
                </svg>
                <div class="icon-shadow"></div>
              </div>
              <h3 class="empty-title">No Live Matches Right Now</h3>
              <p class="empty-description">Check back later for live cricket action. We'll notify you when matches begin!</p>
              <button class="notification-button">
                <span>Notify Me</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import liveData from '../sample-responses/live.json'
import VanillaTilt from 'vanilla-tilt'

const liveMatches = ref([])
const stats = ref([
  { value: '0', label: 'Live Matches' },
  { value: '0', label: 'Active Teams' }
])

// Get team image URL
const getTeamImage = (imageId) => {
  if (!imageId) return ''
  return 'http://static.cricbuzz.com/a/img/v1/i1/c' + imageId + '/i.jpg?p=thumb'
}

// Initialize Tilt.js
onMounted(() => {
  VanillaTilt.init(document.querySelectorAll("[data-tilt]"), {
    max: 15,
    speed: 400,
    glare: true,
    "max-glare": 0.2,
    scale: 1.05
  })
  
  // Process match data
  processMatchData()
})

// Process match data
const processMatchData = () => {
  const matches = []
  liveData.typeMatches.forEach(type => {
    type.seriesMatches.forEach(series => {
      if (series.seriesAdWrapper?.matches) {
        matches.push(...series.seriesAdWrapper.matches)
      }
    })
  })
  liveMatches.value = matches

  // Update stats
  stats.value[0].value = matches.length
  const teams = new Set()
  matches.forEach(match => {
    teams.add(match.matchInfo.team1.teamId)
    teams.add(match.matchInfo.team2.teamId)
  })
  stats.value[1].value = teams.size
}
</script>

<style scoped>
/* Base Styles */
:root {
  --primary-gradient: linear-gradient(135deg, #3B82F6, #8B5CF6);
  --secondary-gradient: linear-gradient(135deg, #1E40AF, #5B21B6);
}

/* Hero Section */
.hero-section {
  @apply relative min-h-[80vh] flex items-center justify-center overflow-hidden;
  @apply before:absolute before:inset-0 before:bg-gradient-to-b before:from-transparent before:to-[#0A1A2F];
}

.hero-background {
  @apply absolute inset-0;
}

.cricket-field {
  @apply absolute inset-0;
}

.field-lines {
  @apply absolute inset-0;
  background-image: 
    linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px),
    linear-gradient(0deg, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: field-pulse 4s infinite ease-in-out;
}

.field-glow {
  @apply absolute inset-0;
  background: radial-gradient(circle at center, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
  animation: glow-pulse 4s infinite ease-in-out;
}

.floating-balls {
  @apply absolute inset-0;
  background-image: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 100px 100px;
  animation: float 15s infinite ease-in-out;
}

/* Hero Content */
.hero-content {
  @apply relative z-10 text-center px-4 w-full max-w-7xl mx-auto;
  animation: fadeIn 1s ease-out forwards;
}

.hero-title {
  @apply text-4xl sm:text-5xl md:text-7xl font-bold mb-4 sm:mb-6;
  @apply transform transition-transform duration-300 hover:scale-105;
}

.text-gradient {
  @apply text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400;
  background-size: 200% auto;
  animation: gradient 8s linear infinite;
}

.text-outline {
  @apply text-transparent;
  -webkit-text-stroke: 2px #3B82F6;
  text-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
}

.hero-subtitle {
  @apply text-lg sm:text-xl md:text-2xl text-gray-400 max-w-2xl mx-auto mb-8 sm:mb-12;
  @apply transform transition-all duration-300 hover:text-blue-400;
}

/* Enhanced Stats Container */
.stats-container {
  @apply w-full max-w-4xl mx-auto mb-8 sm:mb-12;
}

.stats-grid {
  @apply grid grid-cols-1 sm:grid-cols-2 gap-6;
  @apply justify-items-center;
}

.stat-card {
  @apply relative w-full max-w-xs;
  @apply transform transition-all duration-500;
  animation: slide-up 0.5s ease-out forwards;
  opacity: 0;
  animation-delay: var(--delay);
}

.stat-card-content {
  @apply relative bg-[#151F32]/80 backdrop-blur-md rounded-2xl p-8;
  @apply flex flex-col items-center gap-2;
  @apply border border-white/5;
  @apply shadow-lg shadow-black/10;
  @apply transform transition-all duration-500 hover:scale-105 hover:bg-[#151F32]/90;
}

.stat-value {
  @apply text-4xl sm:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400;
  @apply transform transition-transform duration-300;
}

.stat-label {
  @apply text-lg text-gray-400;
  @apply transform transition-all duration-300;
}

.stat-decoration {
  @apply absolute bottom-0 left-0 w-full h-1;
  @apply overflow-hidden;
}

.decoration-dot {
  @apply absolute bottom-0 left-0 w-2 h-2 rounded-full bg-blue-500;
  animation: dot-move 3s infinite linear;
}

.decoration-line {
  @apply absolute bottom-0 left-0 w-full h-1;
  background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent);
  animation: line-move 3s infinite linear;
}

.stat-card:hover .stat-value {
  @apply scale-110;
}

.stat-card:hover .stat-label {
  @apply text-blue-400;
}

/* New Animations */
@keyframes dot-move {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100vw); }
}

@keyframes line-move {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100vw); }
}

/* Team Credit */
.team-credit {
  @apply mt-6 sm:mt-8;
}

.credit-badge {
  @apply inline-flex flex-col items-center gap-1;
  @apply transform transition-transform duration-300 hover:scale-105;
}

.credit-text {
  @apply text-xs sm:text-sm text-gray-400;
  @apply transform transition-all duration-300 hover:text-blue-400;
}

.team-name {
  @apply text-base sm:text-lg font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400;
  animation: gradient 8s linear infinite;
  @apply transform transition-transform duration-300 hover:scale-110;
}

/* Animations */
@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes field-pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 0.8; }
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.1); }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Mobile Optimizations */
@media (max-width: 640px) {
  .hero-section {
    @apply min-h-[70vh];
  }

  .hero-content {
    margin-top: 15px;
    @apply px-4;
  }

  .stats-grid {
    @apply gap-4;
  }

  .stat-card {
    @apply w-full max-w-[280px] p-4;
  }

  .stat-value {
  font-size: 2.5rem;
  line-height: 1.15;
  }
}

/* Dark Mode Optimizations */
@media (prefers-color-scheme: dark) {
  .stat-card {
    @apply shadow-lg shadow-black/20;
  }
}

/* Hover Effects */
@media (hover: hover) {
  .stat-card:hover {
    @apply shadow-xl shadow-blue-500/10;
  }
}

/* Completely Redesigned Live Matches Section */
.matches-section {
  @apply py-20 relative overflow-hidden;
  background: linear-gradient(to bottom, #0A1A2F, #061224);
}

.matches-container {
  @apply container mx-auto px-4 relative z-10;
}

.section-header {
  @apply flex flex-col md:flex-row items-start md:items-center justify-between mb-10;
}

.header-left {
  @apply mb-4 md:mb-0;
}

.section-title {
  @apply text-4xl font-bold mb-2;
  background: linear-gradient(to right, #3B82F6, #8B5CF6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.section-subtitle {
  @apply text-lg text-gray-400;
}

.header-right {
  @apply flex items-center;
}

.live-indicator {
  @apply flex items-center gap-2 px-4 py-2 rounded-full;
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.live-dot {
  @apply w-3 h-3 rounded-full bg-red-500;
  animation: pulse 1.5s infinite ease-in-out;
}

.live-text {
  @apply text-red-400 font-medium;
}

/* Stadium Background */
.stadium-background {
  @apply absolute inset-0 overflow-hidden opacity-20;
}

.stadium-lights {
  @apply absolute w-40 h-40 rounded-full;
  filter: blur(50px);
}

.stadium-lights.left {
  @apply top-0 left-1/4;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.5), transparent 70%);
}

.stadium-lights.right {
  @apply bottom-0 right-1/4;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.5), transparent 70%);
}

.stadium-field {
  @apply absolute inset-0;
  background-image: 
    radial-gradient(circle at center, rgba(255,255,255,0.05) 0%, transparent 70%),
    linear-gradient(0deg, rgba(255,255,255,0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size: 100% 100%, 20px 20px, 20px 20px;
  background-position: center, center, center;
}

/* Live Matches Carousel */
.matches-carousel {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6;
}

.match-card {
  @apply bg-[#151F32]/80 backdrop-blur-md rounded-2xl overflow-hidden;
  @apply flex flex-col;
  @apply transform transition-all duration-300 hover:scale-105;
  @apply border border-white/5;
  @apply shadow-xl;
}

/* Match Banner */
.match-banner {
  @apply p-4 flex items-center justify-between;
  @apply bg-gradient-to-r from-blue-600/30 to-purple-600/30;
  @apply border-b border-white/5;
}

.series-info {
  @apply text-sm font-medium text-white truncate max-w-[150px];
}

.match-stage {
  @apply text-xs text-gray-300;
}

.match-status-pill {
  @apply flex items-center gap-1 px-3 py-1 rounded-full bg-red-500/20 text-xs font-medium text-red-400;
  @apply border border-red-500/30;
}

.pulse-dot {
  @apply w-2 h-2 rounded-full bg-red-500;
  animation: pulse 1.5s infinite;
}

/* Teams Scoreboard */
.scoreboard {
  @apply p-6 flex flex-col gap-4;
}

.team-side {
  @apply flex items-center justify-between;
}

.team-identity {
  @apply flex items-center gap-3;
}

.team-flag {
  @apply w-10 h-10 rounded-lg overflow-hidden;
  @apply bg-gradient-to-br from-blue-500 to-purple-500;
  @apply border border-white/10;
  @apply shadow-lg shadow-blue-500/10;
}

.team-logo {
  @apply w-full h-full object-cover;
}

.team-details {
  @apply flex flex-col;
}

.team-name {
  @apply text-sm font-medium text-white;
}

.team-short {
  @apply text-xs text-gray-400;
}

.team-score {
  @apply text-right;
}

.score {
  @apply text-xl font-bold text-white;
}

.wickets {
  @apply text-gray-400;
}

.overs {
  @apply text-xs text-gray-400 mt-1;
}

/* VS Divider */
.vs-divider {
  @apply flex items-center gap-3 py-2;
}

.vs-line {
  @apply flex-grow h-px bg-gray-700/50;
}

.vs-text {
  @apply text-xs font-bold text-gray-500;
}

/* Match Footer */


.match-venue {
  @apply flex items-center gap-2 text-xs text-gray-400;
}

.venue-icon {
  @apply w-4 h-4;
}

.match-result-status {
  @apply text-sm font-medium text-blue-400;
}

.watch-button {
  @apply mt-2 flex items-center justify-center gap-2 w-full py-2 px-4 rounded-lg;
  @apply bg-gradient-to-r from-blue-600 to-blue-500;
  @apply text-white text-sm font-medium;
  @apply transform transition-all duration-300 hover:from-blue-500 hover:to-blue-600;
  @apply shadow-lg shadow-blue-500/20;
}

.watch-icon {
  @apply w-4 h-4;
}

/* No Matches State */
.no-matches-card {
  @apply col-span-full;
  @apply bg-[#151F32]/80 backdrop-blur-md rounded-2xl;
  @apply p-8;
  @apply border border-white/5;
  @apply shadow-xl;
}

.empty-state-content {
  @apply flex flex-col items-center text-center;
}

.empty-icon-container {
  @apply relative mb-6;
}

.empty-icon {
  @apply w-24 h-24 text-blue-500/80;
  animation: float 3s infinite ease-in-out;
}

.icon-shadow {
  @apply absolute bottom-0 left-1/2 w-16 h-2 -translate-x-1/2 rounded-full;
  background: radial-gradient(ellipse, rgba(59, 130, 246, 0.3), transparent 70%);
  animation: shadow-pulse 3s infinite ease-in-out;
}

.empty-title {
  @apply text-2xl font-bold mb-2;
  background: linear-gradient(to right, #3B82F6, #8B5CF6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.empty-description {
  @apply text-gray-400 max-w-md mx-auto mb-6;
}

.notification-button {
  @apply py-3 px-6 rounded-lg;
  @apply bg-gradient-to-r from-blue-600 to-purple-600;
  @apply text-white font-medium;
  @apply transform transition-all duration-300 hover:from-blue-500 hover:to-purple-500;
  @apply shadow-lg shadow-blue-500/20;
}

/* Animations */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

@keyframes shadow-pulse {
  0%, 100% { opacity: 0.3; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.1); }
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .section-title {
    @apply text-3xl;
  }
  
  .match-banner {
    @apply flex-col items-start gap-2;
  }
  
  .series-info {
    @apply max-w-full;
  }
  
  .match-status-pill {
    @apply self-end;
  }
}

/* Footer */


.copyright {
  @apply text-sm text-gray-500;
}
</style> 