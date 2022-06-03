<template>
  <div :id="benchmark + '-chapter'" class="benchmark-chapter">
    {{ bmUtils.benchmarkNameMapper(benchmark) }}
  </div>
  <div class="horizontal-line" />
  <div class="benchmark-chapter-content">
    <slot />
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import bmUtils from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";

// vue data
const props = defineProps(["benchmark"]);
</script>

<style scoped>
.benchmark-chapter {
  color: white;
  font-size: 22px;
  line-height: 28px;
  border-bottom: 1px solid white;
}

.benchmark-chapter-content {
  margin-top: 0.5em;
}
</style>
