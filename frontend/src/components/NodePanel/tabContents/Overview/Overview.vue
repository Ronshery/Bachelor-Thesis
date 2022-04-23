<template>
  <div
    style="
      background-color: white;
      margin: 0 1.5em 0 1.5em;
      border-radius: 20px;
    "
  >
    <DonutChart
      :layoutsNodes="{ node1: { x: 60, y: 60, bmScore: 1 } }"
      :radius="50"
      :maxValue="10"
      :loadedView="true"
    />
  </div>
</template>

<script setup lang="ts">
import DonutChart from "@/components/utils/DonutChart.vue";
</script>

<style scoped></style>
