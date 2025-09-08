<template>
  <v-app dark>
    <!-- Главное меню -->
    <v-app-bar app flat color="#151226" elevation="0" class="border-bottom">
      <v-container class="py-0">
        <v-row align="center" no-gutters>
          <v-col cols="auto">
            <v-toolbar-title class="text-h4 font-weight-light">
              <v-btn text to="/" class="text-h4 font-weight-light pa-0 white--text">
                БЛОГ
              </v-btn>
            </v-toolbar-title>
          </v-col>
          
          <v-col cols="auto" class="ml-auto hidden-xs-only">
            <v-btn text to="/" class="text-capitalize mx-2" style="color:#BB86FC">
              Главная
            </v-btn>
            <v-btn text class="text-capitalize mx-2" style="color:#BB86FC">
              Архив
            </v-btn>
            <v-btn text class="text-capitalize mx-2" style="color:#BB86FC">
              О блоге
            </v-btn>
          </v-col>

          <!-- Мобильное меню -->
          <v-col cols="auto" class="ml-auto hidden-sm-and-up">
            <v-menu offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" style="color:#BB86FC">
                  <v-icon>mdi-menu</v-icon>
                </v-btn>
              </template>
              <v-list color="#151226">
                <v-list-item to="/">
                  <v-list-item-title style="color:#BB86FC">Главная</v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title style="color:#BB86FC">Архив</v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title style="color:#BB86FC">О блоге</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-col>
        </v-row>
      </v-container>
    </v-app-bar>

    <!-- Основной контент -->
    <v-main style="background:#0d0b14;">
      <v-container class="py-0" fluid>
        <v-row no-gutters>
          <!-- Боковое меню -->
          <v-col cols="12" md="3" lg="2" class="hidden-sm-and-down">
            <v-card flat class="transparent">
              <v-list rounded class="mt-4">
                <v-list-item-group color="#BB86FC">
                  <v-list-item to="/">
                    <v-list-item-content>
                      <v-list-item-title style="color:#BB86FC">Главная</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title style="color:#BB86FC">Архив</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title style="color:#BB86FC">Категории</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </v-card>
          </v-col>

          <!-- Основной контент -->
          <v-col cols="12" md="9" lg="10" style="background:#0d0b14;">
            <v-fade-transition mode="out-in">
              <router-view></router-view>
            </v-fade-transition>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <!-- Подвал -->
    <v-footer app flat color="#151226" dark padless>
      <v-container>
        <v-row class="py-4">
          <v-col cols="12" class="text-center">
            <div class="text-body-2" style="color:#9E8CFF">
              {{ new Date().getFullYear() }} — Блог
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
  })
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