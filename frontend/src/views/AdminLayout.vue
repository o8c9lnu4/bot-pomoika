<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant="miniVariant"
      :clipped="clipped"
      fixed
      app
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      :clipped-left="clipped"
      fixed
      app
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-btn
        icon
        @click.stop="miniVariant = !miniVariant"
      >
        <v-icon>mdi-{{ `chevron-${miniVariant ? 'right' : 'left'}` }}</v-icon>
      </v-btn>
      <v-btn
        icon
        @click.stop="clipped = !clipped"
      >
        <v-icon>mdi-application</v-icon>
      </v-btn>
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-account-circle</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>{{ currentUser.username }}</v-list-item-title>
              <v-list-item-subtitle>{{ currentUser.email }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="logout">
            <v-list-item-icon>
              <v-icon>mdi-logout</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Выйти</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <v-footer :absolute="!fixed" app>
      <span>&copy; {{ new Date().getFullYear() }} Pomoika Vape Lab Admin</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'AdminLayout',
  data() {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      currentUser: {
        username: '',
        email: ''
      },
      items: [
        {
          icon: 'mdi-view-dashboard',
          title: 'Панель управления',
          to: '/admin'
        },
        {
          icon: 'mdi-post',
          title: 'Посты',
          to: '/admin/posts'
        },
        {
          icon: 'mdi-account-group',
          title: 'Пользователи',
          to: '/admin/users'
        }
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'Админка'
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('admin_user')
      localStorage.removeItem('is_admin')
      localStorage.removeItem('admin_token')
      this.$router.push('/admin/login')
    },
    loadUserData() {
      const userData = localStorage.getItem('admin_user')
      if (userData) {
        try {
          this.currentUser = JSON.parse(userData)
        } catch (error) {
          console.error('Ошибка загрузки данных пользователя:', error)
          this.logout()
        }
      }
    }
  },
  mounted() {
    // Проверяем авторизацию
    if (localStorage.getItem('is_admin') !== 'true') {
      this.$router.push('/admin/login')
    } else {
      this.loadUserData()
    }
  }
}
</script>
