<template>
  <div>
    <v-container class="py-4">
      <!-- Заголовок -->
      <v-row>
        <v-col cols="12">
          <div class="mb-8">
            <h1 class="text-h2 font-weight-light white--text mb-2">Посты</h1>
            <div class="text-body-1" style="color:#BDB4FF">Последние публикации</div>
          </div>
        </v-col>
      </v-row>

      <!-- Сетка постов -->
      <v-row>
        <v-col v-for="post in posts" :key="post.id" cols="12" sm="6" lg="4">
          <v-hover v-slot="{ hover }">
            <v-card
              :elevation="hover ? 2 : 0"
              :class="{ 'on-hover': hover }"
              class="mx-auto transition-swing fill-height post-card"
              flat
            >
              <v-card-text class="pa-6">
                <h2 class="text-h5 font-weight-light mb-3 white--text">{{ post.title }}</h2>
                <div class="text-body-2 mb-4 post-excerpt" style="color:#D7D2FF">
                  {{ post.content }}
                </div>
                <div class="d-flex align-center justify-space-between">
                  <span class="text-caption" style="color:#A39AE6">{{ formatDate(post.published_date) }}</span>
                  <v-btn
                    text
                    color="#BB86FC"
                    :to="{ name: 'PostDetail', params: { id: post.id }}"
                    class="text-capitalize px-0"
                  >
                    Читать
                  </v-btn>
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
    }
  },
  watch: {
    currentPage() {
      this.fetchPosts()
    }
  },
  created() {
    this.fetchPosts()
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

.post-card {
  transition: all 0.3s ease;
  border: 1px solid #e0e0e0;
  border-radius: 0;
}

.on-hover {
  transform: translateY(-2px);
  border-color: #000;
}

.custom-pagination >>> .v-pagination__item {
  box-shadow: none;
  border: 1px solid #e0e0e0;
  border-radius: 0;
}

.custom-pagination >>> .v-pagination__item--active {
  background-color: #000 !important;
  color: white !important;
}

.v-card {
  overflow: hidden;
}

.text-h2 {
  font-weight: 300 !important;
  letter-spacing: -0.5px;
}
</style> 