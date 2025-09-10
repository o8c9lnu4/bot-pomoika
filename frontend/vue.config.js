const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ],
  outputDir: 'dist',
  assetsDir: '',
  publicPath: '/static/',
  filenameHashing: false,
  productionSourceMap: false,
  devServer: {
    proxy: {
      '/api': {
        target: process.env.NODE_ENV === 'production' ? 'https://bot-pomoika.onrender.com' : 'http://localhost:8000',
        changeOrigin: true
      },
      '/admin': {
        target: process.env.NODE_ENV === 'production' ? 'https://bot-pomoika.onrender.com' : 'http://localhost:8000',
        changeOrigin: true,
        bypass: function(req) {
          if (req.url.startsWith('/admin')) {
            return false; // Пропускаем запросы к админке напрямую к Django
          }
        }
      },
      '/static': {
        target: process.env.NODE_ENV === 'production' ? 'https://bot-pomoika.onrender.com' : 'http://localhost:8000',
        changeOrigin: true
      }
    },
    historyApiFallback: {
      rewrites: [
        { from: /^\/(?!admin|api|static).*/, to: '/static/index.html' }
      ]
    }
  }
}) 