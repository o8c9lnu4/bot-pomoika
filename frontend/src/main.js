import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import axios from 'axios'
import Toast from 'vue-toastification'
import 'vuetify/dist/vuetify.min.css'
import 'vue-toastification/dist/index.css'

Vue.config.productionTip = false

// Настройка axios
const isProduction = process.env.NODE_ENV === 'production'
const envApiBase = process.env.VUE_APP_API_BASE_URL
// В продакшене используем URL хостинга, в деве — localhost:8000
const defaultProdBase = 'https://bot-pomoika.onrender.com/' // ЗАМЕНИТЕ НА ВАШ ДОМЕН
const defaultDevBase = 'http://localhost:8000'
axios.defaults.baseURL = envApiBase || (isProduction ? defaultProdBase : defaultDevBase)
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

// Настройка toast уведомлений
Vue.use(Toast, {
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false
})

// Добавляем глобальный метод для toast
Vue.prototype.$toast = Vue.$toast

// Interceptor для проверки авторизации
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Если получили 401, очищаем данные авторизации и перенаправляем на логин
      localStorage.removeItem('admin_user')
      localStorage.removeItem('is_admin')
      localStorage.removeItem('admin_token')
      
      if (window.location.hash.includes('/admin')) {
        window.location.href = '/#/admin/login'
      }
    }
    return Promise.reject(error)
  }
)

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app') 