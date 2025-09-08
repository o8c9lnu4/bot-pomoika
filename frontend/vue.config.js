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
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/admin': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        bypass: function(req) {
          if (req.url.startsWith('/admin')) {
            return false; // Пропускаем запросы к админке напрямую к Django
          }
        }
      },
      '/static': {
        target: 'http://localhost:8000',
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