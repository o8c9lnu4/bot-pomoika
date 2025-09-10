<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar dark color="primary">
            <v-toolbar-title>Вход в админку</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="login">
              <v-text-field
                v-model="form.username"
                label="Имя пользователя"
                name="username"
                prepend-icon="mdi-account"
                type="text"
                required
                :error-messages="errors.username"
              ></v-text-field>

              <v-text-field
                v-model="form.password"
                label="Пароль"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                required
                :error-messages="errors.password"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="login" :loading="loading">
              Войти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminLogin',
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      errors: {},
      loading: false
    }
  },
  methods: {
    async login() {
      this.loading = true
      this.errors = {}
      
      try {
        const response = await axios.post('/api/auth/login/', this.form)
        
        if (response.data.message) {
          const user = response.data.user
          
          // Проверяем, является ли пользователь администратором
          if (!user.is_staff) {
            this.$toast.error('У вас нет прав доступа к админке')
            return
          }
          
          // Сохраняем информацию о пользователе
          localStorage.setItem('admin_user', JSON.stringify(user))
          localStorage.setItem('is_admin', 'true')
          localStorage.setItem('admin_token', Date.now().toString()) // Простой токен
          
          this.$toast.success('Добро пожаловать в админку!')
          this.$router.push('/admin')
        }
      } catch (error) {
        if (error.response && error.response.data) {
          if (typeof error.response.data === 'object') {
            this.errors = error.response.data
          } else {
            this.$toast.error(error.response.data)
          }
        } else {
          this.$toast.error('Ошибка при входе в систему')
        }
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    // Проверяем, не авторизован ли уже пользователь
    if (localStorage.getItem('is_admin') === 'true') {
      this.$router.push('/admin')
    }
  }
}
</script>

<style scoped>
.fill-height {
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>
