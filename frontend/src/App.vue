<template>
  <v-app dark>
    <!-- Компактный хедер для мини-приложения -->
    <v-app-bar app flat color="#151226" elevation="0" class="border-bottom" height="48">
      <v-container class="py-0 px-3">
        <v-row align="center" no-gutters>
          <v-col cols="auto">
            <v-toolbar-title class="text-h6 font-weight-medium">
              <span class="white--text">Pomoika Vape Lab</span>
            </v-toolbar-title>
          </v-col>
          
          <v-col cols="auto" class="ml-auto">
            <v-btn icon small @click="refreshData" style="color:#BB86FC">
              <v-icon small>mdi-refresh</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-app-bar>

    <!-- Основной контент для мини-приложения -->
    <v-main style="background:#0d0b14; height: calc(100vh - 48px);">
      <v-container class="py-2 px-3" fluid>
        <v-fade-transition mode="out-in">
          <router-view></router-view>
        </v-fade-transition>
      </v-container>
    </v-main>

    <!-- Компактный подвал для мини-приложения -->
    <v-footer app flat color="#151226" dark padless height="32">
      <v-container class="py-1 px-3">
        <v-row>
          <v-col cols="12" class="text-center">
            <div class="text-caption" style="color:#9E8CFF">
              {{ new Date().getFullYear() }} — Pomoika Vape Lab
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data: () => ({
    darkMode: false
  }),
  methods: {
    refreshData() {
      // Обновляем данные через событие
      this.$root.$emit('refresh-data');
      // Показываем уведомление в Telegram
      if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.showAlert('Данные обновлены');
      }
    }
  },
  mounted() {
    // Инициализация Telegram WebApp
    if (window.Telegram && window.Telegram.WebApp) {
      // Настраиваем тему
      window.Telegram.WebApp.setHeaderColor('#151226');
      window.Telegram.WebApp.setBackgroundColor('#0d0b14');
    }
  }
}
</script>

<style>
.v-application {
  font-family: 'Space Grotesk', 'Poppins', 'Inter', 'Roboto', sans-serif;
}

.v-btn.text-h4 {
  text-transform: none !important;
  letter-spacing: normal !important;
}

.v-main {
  background: #0d0b14;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .2s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

.v-card {
  border-radius: 12px !important;
  box-shadow: 0 4px 20px rgba(124, 77, 255, 0.1) !important;
  border: 1px solid rgba(187, 134, 252, 0.2);
  background: #151226 !important;
}

.v-btn {
  letter-spacing: 0.5px;
  text-transform: none !important;
}

.v-footer {
  border-top: 1px solid rgba(187, 134, 252, 0.2);
}

.v-list {
  background: transparent !important;
}

.v-list-item {
  border-radius: 0 !important;
  margin: 2px 0;
}

.transparent {
  background-color: transparent !important;
}

.border-bottom {
  border-bottom: 1px solid rgba(187, 134, 252, 0.2);
}

.v-app-bar {
  background: #151226 !important;
}

.v-toolbar__title {
  font-weight: 300 !important;
}

/* Мобильная адаптация */
@media (max-width: 600px) {
  .v-toolbar__title {
    font-size: 1.2rem !important;
  }
  .v-btn {
    font-size: 0.9rem !important;
  }
}
</style> 