<template>
    <q-layout view="hHh lpR fFf">
    <q-page-container>
      <q-page class="window-height window-width">
        <NuxtPage />
      </q-page>
    </q-page-container>
  </q-layout>

</template>

<script setup>
useHead({
  title: 'AI4CS',
  script: [
    { hid: 'gm', src: 'https://maps.googleapis.com/maps/api/js?key=AIzaSyDqpZWfYPvfKtilFrzArr_3Pqt6v5TpPSs&callback=Function.prototype', defer: true },
  ],
  meta: [
    {
    name: "viewport",
    content:"width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"
    },
    {
    name: "apple-mobile-web-app-capable",
    content:"yes"
    }
  ]
})
</script>

<style>
@font-face {
  font-family: TitilliumWeb;
  src: url(./assets/TitilliumWeb-Regular.ttf)
}

body {
  font-family: 'TitilliumWeb'
}
</style>