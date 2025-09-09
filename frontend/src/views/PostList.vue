<template>
  <div>
    <v-container class="py-4">
      <!-- Компактный заголовок для мини-приложения -->
      <v-row>
        <v-col cols="12">
          <div class="mb-4">
            <h1 class="text-h5 font-weight-medium white--text mb-1">Новости</h1>
            <div class="text-caption" style="color:#BDB4FF">Последние публикации</div>
          </div>
        </v-col>
      </v-row>

      <!-- Компактная сетка постов для мини-приложения -->
      <v-row>
        <v-col v-for="post in posts" :key="post.id" cols="12">
          <v-hover v-slot="{ hover }">
            <v-card
              :elevation="hover ? 4 : 1"
              :class="{ 'on-hover': hover }"
              class="mx-auto transition-swing post-card-mini"
              color="#151226"
              @click="goToPost(post.id)"
            >
              <v-card-text class="pa-3">
                <div class="d-flex align-start justify-space-between mb-2">
                  <h3 class="text-subtitle-1 font-weight-medium white--text mb-1" style="line-height: 1.3;">
                    {{ post.title }}
                  </h3>
                  <v-icon small style="color:#BB86FC">mdi-chevron-right</v-icon>
                </div>
                <div class="text-body-2 mb-2 post-excerpt-mini" style="color:#D7D2FF">
                  {{ post.content }}
                </div>
                <div class="text-caption" style="color:#A39AE6">
                  {{ formatDate(post.published_date) }}
                </div>
              </v-card-text>
            </v-card>
          </v-hover>
        </v-col>
      </v-row>

      <!-- Сообщение об отсутствии постов -->
      <v-row v-if="posts.length === 0 && !loading" class="mt-6">
        <v-col cols="12" sm="8" md="6" class="mx-auto">
          <v-card class="text-center pa-6" flat color="#151226">
            <h2 class="text-h5 font-weight-light mb-2 white--text">
              Пока нет опубликованных постов
            </h2>
            <p class="text-body-1" style="color:#A39AE6" mb-0>
              Загляните позже
            </p>
          </v-card>
        </v-col>
      </v-row>

      <!-- Пагинация -->
      <v-row v-if="totalPages > 1" class="mt-8">
        <v-col cols="12" class="text-center">
          <v-pagination
            v-model="currentPage"
            :length="totalPages"
            :total-visible="7"
            color="#BB86FC"
            class="custom-pagination"
          ></v-pagination>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PostList',
  data() {
    return {
      posts: [],
      currentPage: 1,
      totalPages: 1,
      loading: false
    }
  },
  methods: {
    async fetchPosts() {
      this.loading = true
      try {
        console.log('Fetching posts from:', `/api/posts/?page=${this.currentPage}`)
        const response = await axios.get(`/api/posts/?page=${this.currentPage}`)
        console.log('API Response:', response.data)
        this.posts = response.data.results
        this.totalPages = Math.ceil(response.data.count / 10)
      } catch (error) {
        console.error('Error fetching posts:', error)
        console.error('Error details:', {
          message: error.message,
          response: error.response ? {
            status: error.response.status,
            data: error.response.data
          } : 'No response',
          config: {
            url: error.config.url,
            method: error.config.method,
            baseURL: error.config.baseURL
          }
        })
        // Показываем ошибку в Telegram
        if (window.Telegram && window.Telegram.WebApp) {
          window.Telegram.WebApp.showAlert('Ошибка загрузки данных');
        }
      } finally {
        setTimeout(() => {
          this.loading = false
        }, 500)
      }
    },
    formatDate(date) {
      return new Date(date).toLocaleString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      })
    },
    goToPost(postId) {
      this.$router.push({ name: 'PostDetail', params: { id: postId } });
    }
  },
  watch: {
    currentPage() {
      this.fetchPosts()
    }
  },
  created() {
    this.fetchPosts()
  },
  mounted() {
    // Слушаем событие обновления данных
    this.$root.$on('refresh-data', () => {
      this.fetchPosts()
    })
  }
}
</script>

<style scoped>
.post-excerpt {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.6;
}

.post-excerpt-mini {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
}

.post-card {
  transition: all 0.3s ease;
  border: 1px solid rgba(187, 134, 252, 0.2);
  border-radius: 12px;
  background: #151226 !important;
}

.post-card-mini {
  transition: all 0.2s ease;
  border: 1px solid rgba(187, 134, 252, 0.2);
  border-radius: 8px;
  background: #151226 !important;
  cursor: pointer;
}

.on-hover {
  transform: translateY(-2px);
  border-color: #BB86FC;
  box-shadow: 0 4px 16px rgba(124, 77, 255, 0.15) !important;
}

.custom-pagination >>> .v-pagination__item {
  box-shadow: none;
  border: 1px solid rgba(187, 134, 252, 0.3);
  border-radius: 8px;
  background: #151226 !important;
  color: #BB86FC !important;
}

.custom-pagination >>> .v-pagination__item--active {
  background-color: #BB86FC !important;
  color: #0d0b14 !important;
}

.v-card {
  overflow: hidden;
}

.text-h2 {
  font-weight: 300 !important;
  letter-spacing: -0.5px;
}
</style> 