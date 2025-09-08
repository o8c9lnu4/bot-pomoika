<template>
  <div>
    <v-container class="py-8">
      <v-row>
        <v-col cols="12">
          <v-btn
            text
            color="black"
            to="/"
            class="mb-8 text-capitalize"
            flat
          >
            ← Назад
          </v-btn>
        </v-col>
      </v-row>

      <v-row v-if="loading" justify="center" align="center" style="min-height: 400px;">
        <v-col cols="auto">
          <v-progress-circular
            indeterminate
            color="black"
            size="32"
          ></v-progress-circular>
        </v-col>
      </v-row>

      <template v-else-if="post">
        <v-row>
          <v-col cols="12" lg="8" class="mx-auto">
            <article>
              <!-- Заголовок -->
              <header class="mb-8">
                <h1 class="text-h2 font-weight-light black--text mb-4">{{ post.title }}</h1>
                <div class="d-flex align-center">
                  <span class="text-body-2 grey--text">{{ formatDate(post.published_date) }}</span>
                  <v-divider vertical class="mx-4"></v-divider>
                  <span class="text-body-2 grey--text">{{ getReadingTime() }} мин. чтения</span>
                </div>
              </header>

              <!-- Содержание -->
              <div class="post-content">
                <div class="text-body-1 grey--text text--darken-2">{{ post.content }}</div>
              </div>

              <!-- Действия -->
              <footer class="mt-8 pt-4 border-top">
                <v-btn
                  text
                  color="black"
                  @click="sharePost"
                  class="text-capitalize"
                >
                  Поделиться
                </v-btn>
              </footer>
            </article>
          </v-col>
        </v-row>
      </template>

      <v-row v-else justify="center">
        <v-col cols="12" sm="8" md="6" class="mx-auto">
          <v-card
            class="text-center pa-6"
            flat
          >
            <h2 class="text-h5 font-weight-light mb-2 black--text">
              Пост не найден
            </h2>
            <p class="text-body-1 grey--text mb-4">
              Возможно, он был удален или перемещен.
            </p>
            <v-btn
              color="black"
              to="/"
              class="text-capitalize"
              outlined
            >
              Вернуться на главную
            </v-btn>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PostDetail',
  props: {
    id: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      post: null,
      loading: false
    }
  },
  methods: {
    async fetchPost() {
      this.loading = true
      try {
        const response = await axios.get(`/api/posts/${this.id}/`)
        this.post = response.data
      } catch (error) {
        console.error('Error fetching post:', error)
        this.post = null
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
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    getReadingTime() {
      if (!this.post?.content) return 1
      const words = this.post.content.trim().split(/\s+/).length
      return Math.max(1, Math.ceil(words / 200))
    },
    sharePost() {
      if (navigator.share) {
        navigator.share({
          title: this.post.title,
          text: this.post.content.substring(0, 100) + '...',
          url: window.location.href
        })
      }
    }
  },
  created() {
    this.fetchPost()
  }
}
</script>

<style scoped>
.post-content {
  line-height: 1.8;
  white-space: pre-line;
}

.text-h2 {
  font-weight: 300 !important;
  letter-spacing: -0.5px;
}

.border-top {
  border-top: 1px solid #e0e0e0;
}

.v-progress-circular {
  position: relative;
}

.v-card {
  border: 1px solid #e0e0e0;
  border-radius: 0;
}
</style> 