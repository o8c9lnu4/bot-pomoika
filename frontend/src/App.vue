<template>
  <v-app>
    <!-- Главное меню -->
    <v-app-bar app flat color="white" elevation="0" class="border-bottom">
      <v-container class="py-0">
        <v-row align="center" no-gutters>
          <v-col cols="auto">
            <v-toolbar-title class="text-h4 font-weight-light">
              <v-btn text to="/" class="text-h4 font-weight-light pa-0 black--text">
                БЛОГ
              </v-btn>
            </v-toolbar-title>
          </v-col>
          
          <v-col cols="auto" class="ml-auto">
            <v-btn text to="/" class="text-capitalize mx-2 black--text">
              Главная
            </v-btn>
            <v-btn text class="text-capitalize mx-2 black--text">
              Архив
            </v-btn>
            <v-btn text class="text-capitalize mx-2 black--text">
              О блоге
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-app-bar>

    <!-- Основной контент -->
    <v-main class="white">
      <v-container class="py-0" fluid>
        <v-row no-gutters>
          <!-- Боковое меню -->
          <v-col cols="12" md="3" lg="2" class="hidden-sm-and-down">
            <v-card flat class="transparent">
              <v-list rounded class="mt-4">
                <v-list-item-group color="black">
                  <v-list-item to="/">
                    <v-list-item-content>
                      <v-list-item-title class="black--text">Главная</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title class="black--text">Архив</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title class="black--text">Категории</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </v-card>
          </v-col>

          <!-- Основной контент -->
          <v-col cols="12" md="9" lg="10" class="grey lighten-5">
            <v-fade-transition mode="out-in">
              <router-view></router-view>
            </v-fade-transition>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <!-- Подвал -->
    <v-footer app flat color="black" dark padless>
      <v-container>
        <v-row class="py-4">
          <v-col cols="12" class="text-center">
            <div class="text-body-2">
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
  font-family: 'Inter', 'Roboto', sans-serif;
}

.v-btn.text-h4 {
  text-transform: none !important;
  letter-spacing: normal !important;
}

.v-main {
  background: #fafafa;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .2s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

.v-card {
  border-radius: 0 !important;
  box-shadow: none !important;
  border: 1px solid #e0e0e0;
}

.v-btn {
  letter-spacing: 0.5px;
  text-transform: none !important;
}

.v-footer {
  border-top: 1px solid #333;
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
  border-bottom: 1px solid #e0e0e0;
}

.v-app-bar {
  background: white !important;
}

.v-toolbar__title {
  font-weight: 300 !important;
}
</style> 