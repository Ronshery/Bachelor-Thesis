<template>
  <div :id="benchmark + '-chapter'" class="benchmark-chapter">
    {{ bmScript.benchmarkNameMapper(benchmark) }}
  </div>
  <div class="horizontal-line" />
  <div class="benchmark-chapter-content">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import bmScript from "@/components/NodePanel/tabContents/Benchmark/utils/bm-script";

// vue data
const props = defineProps(["benchmark"]);
</script>

<style scoped>
.benchmark-chapter {
  color: white;
  font-size: 20px;
  line-height: 28px;
  border-bottom: 1px solid white;
}

.benchmark-chapter-content {
  margin-top: 0.5em;
}
</style>
