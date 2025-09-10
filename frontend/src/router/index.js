import Vue from 'vue'
import VueRouter from 'vue-router'
import PostList from '../views/PostList.vue'
import PostDetail from '../views/PostDetail.vue'
import AdminLogin from '../views/AdminLogin.vue'
import AdminLayout from '../views/AdminLayout.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AdminPosts from '../views/AdminPosts.vue'
import AdminUsers from '../views/AdminUsers.vue'

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
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: AdminLogin
  },
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: AdminDashboard
      },
      {
        path: 'posts',
        name: 'AdminPosts',
        component: AdminPosts
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: AdminUsers
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

// Навигационная защита
router.beforeEach((to, from, next) => {
  const isAdmin = localStorage.getItem('is_admin') === 'true'
  const adminUser = localStorage.getItem('admin_user')
  const adminToken = localStorage.getItem('admin_token')
  
  // Проверяем, что все необходимые данные для авторизации есть
  const isFullyAuthorized = isAdmin && adminUser && adminToken
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isFullyAuthorized) {
      // Очищаем неполные данные авторизации
      localStorage.removeItem('admin_user')
      localStorage.removeItem('is_admin')
      localStorage.removeItem('admin_token')
      next('/admin/login')
    } else {
      // Дополнительная проверка прав пользователя
      try {
        const user = JSON.parse(adminUser)
        if (!user.is_staff) {
          localStorage.clear()
          next('/admin/login')
        } else {
          next()
        }
      } catch (error) {
        localStorage.clear()
        next('/admin/login')
      }
    }
  } else if (to.path === '/admin/login' && isFullyAuthorized) {
    next('/admin')
  } else {
    next()
  }
})

export default router 