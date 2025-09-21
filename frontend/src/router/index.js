import { createRouter, createWebHistory } from 'vue-router'
import TaskPage from "@/pages/TaskPage.vue"
import AboutPage from "@/pages/AboutPage.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path:'/tasks',component:TaskPage},
    {path:'/about',component:AboutPage}
  ],
})

export default router
