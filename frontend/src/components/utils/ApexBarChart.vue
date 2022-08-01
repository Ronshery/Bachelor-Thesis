<template>
  <apexchart
    type="bar"
    :options="options"
    :series="series"
    :key="Math.random()"
  ></apexchart>
  <!-- key: trigger render again for sync charts -->
</template>

<script setup lang="ts">
import { defineProps } from "vue";

// vue data
const props = defineProps(["series", "options"]);
</script>

<style scoped></style>
