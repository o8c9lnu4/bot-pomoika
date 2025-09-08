import Vue from 'vue'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    dark: true,
    themes: {
      dark: {
        primary: '#7C4DFF',
        secondary: '#9E8CFF',
        accent: '#BB86FC',
        background: '#0d0b14',
        surface: '#151226',
        error: '#FF5252',
        info: '#8A80FF',
        success: '#64FFDA',
        warning: '#FFB300'
      }
    }
  },
  icons: {
    iconfont: 'mdi'
  }
}) 