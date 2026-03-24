import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './style.css'
import HomePage from './pages/HomePage.vue'
import PostedPage from './pages/PostedPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: HomePage
    },
    {
      path: '/posted/:id',
      component: PostedPage
    }
  ]
})

createApp(App).use(router).mount('#app')
