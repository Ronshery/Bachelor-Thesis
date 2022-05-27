<template>
  <Benchmark :node="node" :availableBenchmarks="availableBenchmarks" />
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import Benchmark from "@/components/NodePanel/tabContents/Benchmark/Benchmark.vue";
//cpu-sysbench-qvsku571ke
// vue data
const props = defineProps(["node", "nodePanelOpen"]);

// data
const availableBenchmarks = [
  "cpu_sysbench",
  "memory-sysbench",
  "disk-ioping",
  "disk-fio",
];
</script>

<style scoped></style>
