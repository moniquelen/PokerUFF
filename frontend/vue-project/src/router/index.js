import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import CreateSessionView from '../views/CreateSessionView.vue'
import SessionView from '../views/SessionView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/create',
      name: 'create-session',
      component: CreateSessionView
    },
    {
      path: '/session/:code',
      name: 'session',
      component: SessionView
    }
  ]
})

export default router