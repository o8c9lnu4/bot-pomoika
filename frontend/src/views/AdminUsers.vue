<template>
  <div>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 mb-6">Управление пользователями</h1>
      </v-col>
    </v-row>

    <v-card>
      <v-card-text>
        <v-row class="mb-4">
          <v-col cols="12" md="6">
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Поиск пользователей"
              single-line
              hide-details
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="statusFilter"
              :items="statusOptions"
              label="Фильтр по статусу"
              clearable
            ></v-select>
          </v-col>
        </v-row>
        
        <v-data-table
          :headers="headers"
          :items="filteredUsers"
          :loading="loading"
          :items-per-page="10"
          :search="search"
          class="elevation-1"
        >
          <template slot="item.date_joined" slot-scope="{ item }">
            {{ formatDate(item.date_joined) }}
          </template>
          <template slot="item.is_staff" slot-scope="{ item }">
            <v-chip
              :color="item.is_staff ? 'success' : 'default'"
              small
            >
              {{ item.is_staff ? 'Администратор' : 'Пользователь' }}
            </v-chip>
          </template>
          <template slot="item.actions" slot-scope="{ item }">
            <v-btn
              small
              color="primary"
              @click="toggleStaffStatus(item)"
            >
              {{ item.is_staff ? 'Убрать права' : 'Сделать админом' }}
            </v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminUsers',
  data() {
    return {
      loading: false,
      users: [],
      search: '',
      statusFilter: null,
      statusOptions: [
        { text: 'Все пользователи', value: null },
        { text: 'Администраторы', value: true },
        { text: 'Обычные пользователи', value: false }
      ],
      headers: [
        { text: 'ID', value: 'id', sortable: true },
        { text: 'Имя пользователя', value: 'username', sortable: true },
        { text: 'Email', value: 'email', sortable: true },
        { text: 'Статус', value: 'is_staff', sortable: true },
        { text: 'Дата регистрации', value: 'date_joined', sortable: true },
        { text: 'Действия', value: 'actions', sortable: false }
      ]
    }
  },
  computed: {
    filteredUsers() {
      let filtered = this.users
      
      if (this.statusFilter !== null) {
        filtered = filtered.filter(user => user.is_staff === this.statusFilter)
      }
      
      return filtered
    }
  },
  methods: {
    async loadUsers() {
      this.loading = true
      try {
        const response = await axios.get('/api/users/')
        this.users = response.data
      } catch (error) {
        console.error('Ошибка загрузки пользователей:', error)
        this.$toast.error('Ошибка загрузки пользователей')
      } finally {
        this.loading = false
      }
    },
    async toggleStaffStatus(user) {
      const action = user.is_staff ? 'убрать права администратора' : 'назначить администратором'
      const confirmMessage = `Вы уверены, что хотите ${action} у пользователя "${user.username}"?`
      
      if (confirm(confirmMessage)) {
        try {
          await axios.patch(`/api/users/${user.id}/`, {
            is_staff: !user.is_staff
          })
          user.is_staff = !user.is_staff
          this.$toast.success(`Статус пользователя ${user.username} обновлен`)
        } catch (error) {
          console.error('Ошибка обновления статуса:', error)
          this.$toast.error('Ошибка обновления статуса пользователя')
        }
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ru-RU')
    }
  },
  mounted() {
    this.loadUsers()
  }
}
</script>
