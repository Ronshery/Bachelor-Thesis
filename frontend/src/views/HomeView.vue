<template>
  <!--  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App" />
  </div>-->
  <StandartLayout>
    <NetworkGraphContainer />
  </StandartLayout>
</template>

<script setup lang="ts">
import { ref } from "vue";
import HelloWorld from "@/components/HelloWorld.vue";
import StandartLayout from "@/components/layouts/StandartLayout.vue";
import TwoColumnLayout from "@/components/layouts/TwoColumnLayout.vue";
import NetworkGraphContainer from "@/components/NetworkGraph/NetworkGraphContainer.vue";
</script>
<style scoped></style>
