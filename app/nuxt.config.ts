// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  server: {
    host: '0.0.0.0',
    port: 3000
  },
  app: {
    baseURL: process.env.NODE_ENV == 'production' ? "/" : "/dev"
  },
  build: {
    transpile: ['@vuepic/vue-datepicker']
},
  modules: [
    'nuxt-lodash',
    'nuxt-quasar-ui',
    '@unocss/nuxt'
  ],
  quasar: {
    plugins: [
      'BottomSheet',
      'Dialog',
      'Loading',
      'Notify',
      'Dark',
    ],
    extras: {
      font: 'roboto-font',
      fontIcons: ['material-icons','fontawesome-v6'],
    },
  },
  ssr: false
})
