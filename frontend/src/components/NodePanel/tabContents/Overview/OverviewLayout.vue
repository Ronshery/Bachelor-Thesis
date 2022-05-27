<template>
  <div class="overview-layout-container">
    <slot />
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.overview-layout-container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
</style>
