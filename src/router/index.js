import { createRouter, createWebHistory } from 'vue-router'
import LiveMatches from '../views/LiveMatches.vue'
import MatchDetails from '../views/MatchDetails.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: LiveMatches
    },
    {
      path: '/match/:id',
      name: 'match-details',
      component: MatchDetails,
      props: true
    },
    {
      path: '/matches',
      name: 'matches',
      component: () => import('../views/MatchesView.vue')
    },
    {
      path: '/teams',
      name: 'teams',
      component: () => import('../views/Teams.vue')
    },
    {
      path: '/team/:teamId',
      name: 'team-details',
      component: () => import('../views/TeamDetails.vue'),
      props: true
    },
    {
      path: '/players',
      name: 'players',
      component: () => import('../views/PlayerDetails.vue')
    },
    {
      path: '/player/:id',
      name: 'player-details',
      component: () => import('../views/PlayerDetailedView.vue'),
      props: true
    },
    {
      path: '/venues',
      name: 'venues',
      component: () => import('../views/VenuesView.vue')
    },
    {
      path: '/venue/:id',
      name: 'venue-details',
      component: () => import('../components/VenueDetails.vue'),
      props: true
    },
    {
      path: '/compare',
      name: 'player-comparison',
      component: () => import('../components/PlayerComparison.vue')
    },
    {
      path: '/statistics',
      name: 'statistics',
      component: () => import('../views/StatisticsView.vue')
    }
  ]
})

export default router 