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
  margin: 1em 1.5em 0 1.5em;
}
</style>
