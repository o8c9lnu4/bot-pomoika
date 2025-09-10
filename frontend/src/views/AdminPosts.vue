<template>
  <div>
    <v-row>
      <v-col cols="12">
        <div class="d-flex justify-space-between align-center mb-6">
          <h1 class="text-h4">Управление постами</h1>
          <v-btn
            color="primary"
            @click="createPost"
          >
            <v-icon left>mdi-plus</v-icon>
            Создать пост
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <v-card>
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="posts"
          :loading="loading"
          :items-per-page="10"
          class="elevation-1"
        >
          <template slot="item.published_date" slot-scope="{ item }">
            <v-chip
              :color="item.published_date ? 'success' : 'warning'"
              small
            >
              {{ item.published_date ? 'Опубликован' : 'Черновик' }}
            </v-chip>
          </template>
          <template slot="item.created_date" slot-scope="{ item }">
            {{ formatDate(item.created_date) }}
          </template>
          <template slot="item.actions" slot-scope="{ item }">
            <v-btn
              small
              color="primary"
              class="mr-2"
              @click="editPost(item)"
            >
              Редактировать
            </v-btn>
            <v-btn
              small
              :color="item.published_date ? 'warning' : 'success'"
              class="mr-2"
              @click="togglePublish(item)"
            >
              {{ item.published_date ? 'Снять с публикации' : 'Опубликовать' }}
            </v-btn>
            <v-btn
              small
              color="error"
              @click="deletePost(item)"
            >
              Удалить
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <!-- Диалог создания/редактирования поста -->
    <v-dialog v-model="dialog" max-width="800px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ isEdit ? 'Редактировать пост' : 'Создать пост' }}</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="postForm.title"
              label="Заголовок"
              :rules="titleRules"
              required
            ></v-text-field>
            
            <v-textarea
              v-model="postForm.content"
              label="Содержание"
              :rules="contentRules"
              required
              rows="6"
            ></v-textarea>
            
            <v-text-field
              v-model="postForm.image_url"
              label="URL изображения"
            ></v-text-field>
            
            <v-switch
              v-model="postForm.published"
              label="Опубликовать сразу"
            ></v-switch>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">
            Отмена
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="savePost"
            :disabled="!valid"
          >
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h5">Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить пост "{{ postToDelete?.title }}"?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="deleteDialog = false">
            Отмена
          </v-btn>
          <v-btn color="red darken-1" text @click="confirmDelete">
            Удалить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminPosts',
  data() {
    return {
      loading: false,
      posts: [],
      dialog: false,
      deleteDialog: false,
      isEdit: false,
      valid: false,
      postToDelete: null,
      postForm: {
        title: '',
        content: '',
        image_url: '',
        published: false
      },
      titleRules: [
        v => !!v || 'Заголовок обязателен',
        v => (v && v.length >= 3) || 'Заголовок должен содержать минимум 3 символа'
      ],
      contentRules: [
        v => !!v || 'Содержание обязательно',
        v => (v && v.length >= 10) || 'Содержание должно содержать минимум 10 символов'
      ],
      headers: [
        { text: 'ID', value: 'id', sortable: true },
        { text: 'Заголовок', value: 'title', sortable: true },
        { text: 'Статус', value: 'published_date', sortable: true },
        { text: 'Дата создания', value: 'created_date', sortable: true },
        { text: 'Действия', value: 'actions', sortable: false }
      ]
    }
  },
  methods: {
    async loadPosts() {
      this.loading = true
      try {
        const response = await axios.get('/api/posts/')
        this.posts = response.data
      } catch (error) {
        console.error('Ошибка загрузки постов:', error)
        this.$toast.error('Ошибка загрузки постов')
      } finally {
        this.loading = false
      }
    },
    createPost() {
      this.isEdit = false
      this.postForm = {
        title: '',
        content: '',
        image_url: '',
        published: false
      }
      this.dialog = true
    },
    editPost(post) {
      this.isEdit = true
      this.postForm = {
        id: post.id,
        title: post.title,
        content: post.content,
        image_url: post.image_url || '',
        published: !!post.published_date
      }
      this.dialog = true
    },
    async savePost() {
      if (!this.$refs.form.validate()) return

      try {
        const postData = {
          title: this.postForm.title.trim(),
          content: this.postForm.content.trim(),
          image_url: this.postForm.image_url?.trim() || null,
          published_date: this.postForm.published ? new Date().toISOString() : null
        }

        // Валидация URL изображения
        if (postData.image_url && !this.isValidUrl(postData.image_url)) {
          this.$toast.error('Введите корректный URL изображения')
          return
        }

        if (this.isEdit) {
          await axios.put(`/api/posts/${this.postForm.id}/`, postData)
          this.$toast.success('Пост успешно обновлен')
        } else {
          await axios.post('/api/posts/', postData)
          this.$toast.success('Пост успешно создан')
        }

        this.dialog = false
        this.loadPosts()
      } catch (error) {
        console.error('Ошибка сохранения поста:', error)
        if (error.response && error.response.data) {
          const errors = error.response.data
          if (typeof errors === 'object') {
            Object.keys(errors).forEach(key => {
              this.$toast.error(`${key}: ${errors[key]}`)
            })
          } else {
            this.$toast.error('Ошибка сохранения поста')
          }
        } else {
          this.$toast.error('Ошибка сохранения поста')
        }
      }
    },
    isValidUrl(string) {
      try {
        new URL(string)
        return true
      } catch (_) {
        return false
      }
    },
    async togglePublish(post) {
      try {
        const postData = {
          title: post.title,
          content: post.content,
          image_url: post.image_url,
          published_date: post.published_date ? null : new Date().toISOString()
        }
        
        await axios.put(`/api/posts/${post.id}/`, postData)
        post.published_date = postData.published_date
        this.$toast.success(post.published_date ? 'Пост опубликован' : 'Пост снят с публикации')
      } catch (error) {
        console.error('Ошибка изменения статуса публикации:', error)
        this.$toast.error('Ошибка изменения статуса публикации')
      }
    },
    deletePost(post) {
      this.postToDelete = post
      this.deleteDialog = true
    },
    async confirmDelete() {
      try {
        await axios.delete(`/api/posts/${this.postToDelete.id}/`)
        this.deleteDialog = false
        this.loadPosts()
        this.$toast.success('Пост удален')
      } catch (error) {
        console.error('Ошибка удаления поста:', error)
        this.$toast.error('Ошибка удаления поста')
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ru-RU')
    }
  },
  mounted() {
    this.loadPosts()
  }
}
</script>
