<template>
  <!--  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App" />
  </div>-->
  <div id="graph-wrapper">
    <NetworkGraphContainer />
  </div>
</template>

<script setup lang="ts">
import NetworkGraphContainer from "@/components/NetworkGraph/NetworkGraphContainer.vue";
</script>

<style scoped>
#graph-wrapper {
  transition: width 1500ms;
  width: 100%;
  min-width: 390px;
}
</style>
