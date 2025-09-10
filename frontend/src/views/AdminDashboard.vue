<template>
  <div>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-6">Панель управления</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="3">
        <v-card class="pa-4" color="primary" dark>
          <v-card-title class="text-h6">
            <v-icon left>mdi-post</v-icon>
            Всего постов
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ stats.totalPosts }}</div>
            <div class="text-caption">
              Опубликовано: {{ stats.publishedPosts }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card class="pa-4" color="success" dark>
          <v-card-title class="text-h6">
            <v-icon left>mdi-account-group</v-icon>
            Пользователи
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ stats.totalUsers }}</div>
            <div class="text-caption">
              Админов: {{ stats.adminUsers }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card class="pa-4" color="warning" dark>
          <v-card-title class="text-h6">
            <v-icon left>mdi-calendar-today</v-icon>
            За сегодня
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ stats.todayPosts }}</div>
            <div class="text-caption">
              Новых постов
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card class="pa-4" color="info" dark>
          <v-card-title class="text-h6">
            <v-icon left>mdi-calendar-week</v-icon>
            За неделю
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ stats.weekPosts }}</div>
            <div class="text-caption">
              Новых постов
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-6">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>
            Последние посты
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              small
              to="/admin/posts"
            >
              Все посты
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="recentPosts"
              :loading="loading"
              :items-per-page="5"
              hide-default-footer
            >
              <template slot="item.published_date" slot-scope="{ item }">
                {{ formatDate(item.published_date) }}
              </template>
              <template slot="item.actions" slot-scope="{ item }">
                <v-btn
                  small
                  color="primary"
                  :to="`/admin/posts/${item.id}/edit`"
                >
                  Редактировать
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>
            Статистика постов
          </v-card-title>
          <v-card-text>
            <div class="text-center">
              <div class="text-h4 mb-2">{{ stats.publishedPosts }}</div>
              <div class="text-caption text--secondary mb-4">Опубликованных постов</div>
              
              <div class="text-h4 mb-2">{{ stats.totalPosts - stats.publishedPosts }}</div>
              <div class="text-caption text--secondary mb-4">Черновиков</div>
              
              <v-progress-circular
                :value="(stats.publishedPosts / stats.totalPosts) * 100"
                size="80"
                width="8"
                color="primary"
                class="mb-2"
              >
                {{ Math.round((stats.publishedPosts / stats.totalPosts) * 100) }}%
              </v-progress-circular>
              <div class="text-caption text--secondary">Процент опубликованных</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      loading: false,
      stats: {
        totalPosts: 0,
        publishedPosts: 0,
        totalUsers: 0,
        adminUsers: 0,
        todayPosts: 0,
        weekPosts: 0
      },
      recentPosts: [],
      headers: [
        { text: 'Заголовок', value: 'title' },
        { text: 'Автор', value: 'author' },
        { text: 'Дата публикации', value: 'published_date' },
        { text: 'Действия', value: 'actions', sortable: false }
      ]
    }
  },
  methods: {
    async loadStats() {
      this.loading = true
      try {
        // Загружаем статистику
        const [postsResponse, usersResponse] = await Promise.all([
          axios.get('/api/posts/'),
          axios.get('/api/users/')
        ])

        const posts = postsResponse.data
        const users = usersResponse.data

        // Общая статистика постов
        this.stats.totalPosts = posts.length
        this.stats.publishedPosts = posts.filter(post => post.published_date).length

        // Статистика пользователей
        this.stats.totalUsers = users.length
        this.stats.adminUsers = users.filter(user => user.is_staff).length

        // Статистика по времени
        const now = new Date()
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
        const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000)

        this.stats.todayPosts = posts.filter(post => {
          const postDate = new Date(post.created_date)
          return postDate >= today
        }).length

        this.stats.weekPosts = posts.filter(post => {
          const postDate = new Date(post.created_date)
          return postDate >= weekAgo
        }).length

        // Загружаем последние посты
        this.recentPosts = posts
          .sort((a, b) => new Date(b.created_date) - new Date(a.created_date))
          .slice(0, 5)
      } catch (error) {
        console.error('Ошибка загрузки статистики:', error)
        this.$toast.error('Ошибка загрузки статистики')
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'Не опубликован'
      return new Date(dateString).toLocaleDateString('ru-RU')
    }
  },
  mounted() {
    this.loadStats()
  }
}
</script>
