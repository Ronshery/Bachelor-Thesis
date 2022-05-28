<template>
  <Benchmark :node="node" :availableBenchmarks="availableBenchmarks" />
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import Benchmark from "@/components/NodePanel/tabContents/Benchmark/Benchmark.vue";

interface availableBMs {
  cpu: string[];
  memory: string[];
  disk: string[];
  network: string[];
}

// vue data
const props = defineProps(["node", "nodePanelOpen"]);

// data
const availableBenchmarks: availableBMs = {
  cpu: ["cpu-sysbench"],
  memory: ["memory-sysbench"],
  disk: ["disk-ioping", "disk-fio"],
  network: ["network-iperf3", "network-qperf"],
};
</script>

<style scoped></style>
