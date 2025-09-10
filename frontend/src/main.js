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
// В продакшене по умолчанию НЕ используем origin страницы (например, Telegram WebApp),
// поэтому требуем явный VUE_APP_API_BASE_URL; в деве — localhost:8000
const defaultProdBase = '' // оставляем относительный путь только если фронт и бэк на одном домене
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