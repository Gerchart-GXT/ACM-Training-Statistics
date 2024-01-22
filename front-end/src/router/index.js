import { createRouter, createWebHistory } from 'vue-router'
import OverviewView from "@/views/OverviewView"
import CodeforcesSubView from "@/views/codeforces/CodeforcesSubView"
import CodeforcesMemberView from "@/views/codeforces/CodeforcesMemberView"
import NotFoundView from "@/views/NotFoundView"
import MembersView from "@/views/MembersView"

const routes = [
  {
    path: '/',
    name: 'Overview',
    component: OverviewView
  },
  {
    path: '/overview/',
    name: 'Overview',
    component: OverviewView
  },
  {
    path: '/codeforces/:userName/:verdict',
    name: 'CodeforcesSub',
    component: CodeforcesSubView
  },
  {
    path: '/codeforces/',
    name: 'CodeforcesMember',
    component: CodeforcesMemberView
  },
  {
    path: '/members/',
    name: 'Members',
    component: MembersView
  },
  {
    path: '/404/',
    name: 'NotFound',
    component: NotFoundView
  },
  {
    path: '/:catchAll(.*)',
    redirect: "/404/"
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
