import Vue from 'vue'
import VueRouter from 'vue-router'
import PostList from '../views/PostList.vue'
import PostDetail from '../views/PostDetail.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'PostList',
    component: PostList
  },
  {
    path: '/post/:id',
    name: 'PostDetail',
    component: PostDetail,
    props: true
  }
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

export default router 