import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import axios from 'axios'
import 'vuetify/dist/vuetify.min.css'

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

// Проверяем, что мы не на странице админки
const isAdminPage = window.location.pathname.startsWith('/admin/')
if (!isAdminPage && document.getElementById('app')) {
  new Vue({
    router,
    vuetify,
    render: h => h(App)
  }).$mount('#app')
} 