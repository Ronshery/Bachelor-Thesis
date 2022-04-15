<template>
  <div v-show="isActive">
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { ref, defineExpose, defineProps } from "vue";
// data
const isActive = ref(false);

defineExpose({ isActive });
</script>

<style scoped></style>
