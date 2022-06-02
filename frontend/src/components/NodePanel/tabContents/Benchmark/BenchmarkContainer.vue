<template>
  {{ node.name }}
  <BenchmarkComponent :node="node" :availableBenchmarks="availableBenchmarks" />
</template>

<script setup lang="ts">
import { defineProps, watch } from "vue";
import BenchmarkComponent from "@/components/NodePanel/tabContents/Benchmark/Benchmark.vue";
import Benchmark from "@/models/Benchmark";
import {
  BmResource,
  BmType,
} from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";

interface availableBMs {
  cpu?: BmType[];
  memory?: BmType[];
  disk?: BmType[];
  network?: BmType[];
}

// vue data
const props = defineProps(["node", "nodePanelOpen"]);

// data
const availableBenchmarks: availableBMs = {
  [BmResource.CPU]: [BmType.CPU_SYSBENCH],
  [BmResource.MEMORY]: [BmType.MEMORY_SYSBENCH],
  [BmResource.DISK]: [BmType.DISK_IOPING, BmType.DISK_FIO],
  [BmResource.NETWORK]: [BmType.NETWORK_IPERF3, BmType.NETWORK_QPERF],
};

// methods
let lastNode = 0;
watch(props, () => {
  if (props.node.id) {
    if (lastNode != props.node.id || lastNode == 0) {
      lastNode = props.node.id;
      console.log("fetch benchmarks");
      Benchmark.dispatch("fetchBenchmarksByNode", {
        nodeID: props.node.id,
      });
    }
  }
});
</script>

<style scoped></style>
