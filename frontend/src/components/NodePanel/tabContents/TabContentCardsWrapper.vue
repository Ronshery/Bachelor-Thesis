<template>
  <div class="cards-wrapper">
    <slot />
  </div>
</template>

<script setup lang="ts" />

<style scoped>
.cards-wrapper {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
</style>
