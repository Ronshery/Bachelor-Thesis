<template>
  {{ getRunningState }}
  {{ benchmarks[benchmarks.length - 1] }}
  <TabContentCardsWrapper>
    <TabContentCard>
      <template v-slot:title> Latency </template>
      <ApexBarChart :series="latencySeries" />
    </TabContentCard>
  </TabContentCardsWrapper>
</template>

<script setup lang="ts">
import { defineProps, watch, computed, defineEmits, ref } from "vue";
import ApexBarChart from "@/components/utils/ApexBarChart.vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import TabContentCardsWrapper from "@/components/NodePanel/tabContents/TabContentCardsWrapper.vue";

interface CPUSysbenchResult {
  [key: string]: string;
}
// vue data
const props = defineProps(["benchmarks", "nodeID"]);
const emit = defineEmits(["changedRunning"]);

// data
interface ApexBarDataPoint {
  name: string;
  data: string[];
}

const latencySeries = ref<ApexBarDataPoint[]>([]);
// methods
const getBenchmarks = computed(() => {
  console.log("benchmarkslist changed: " + props.nodeID);
  if (props.benchmarks) {
    return props.benchmarks;
  } else {
    return [];
  }
});
const getRunningState = computed(() => {
  let returnValue = false;
  if (getBenchmarks.value.length != 0) {
    let latestBenchmark = props.benchmarks[props.benchmarks.length - 1];
    returnValue = latestBenchmark.results == null;
  }
  return returnValue;
});

watch(getRunningState, () => {
  console.log("value changed");
  console.log(getRunningState.value);
  if (!getRunningState.value) {
    convertResultsToBar();
  }
  const emitParam = { "cpu-sysbench": getRunningState.value };
  emit("changedRunning", emitParam);
});

const convertResultsToBar = () => {
  const latestBenchmark = props.benchmarks[props.benchmarks.length - 1];
  if (latestBenchmark.node == props.nodeID) {
    const results: CPUSysbenchResult = latestBenchmark.results;
    latencySeries.value = [
      {
        name: "min",
        data: [results.latency_min],
      },
      {
        name: "avg",
        data: [results.latency_avg],
      },
      {
        name: "max",
        data: [results.latency_max],
      },
      {
        name: "95p",
        data: [results.latency_95p],
      },
    ];
  }
};
</script>

<style scoped></style>
