<template>
  {{ getRunningState }}
  {{ benchmarks[benchmarks.length - 1] }}
  <TabContentCardsWrapper>
    <TabContentCard>
      <template v-slot:title> Latency </template>
      <ApexBarChart />
    </TabContentCard>
  </TabContentCardsWrapper>
</template>

<script setup lang="ts">
import { defineProps, watch, computed, defineEmits } from "vue";
import ApexBarChart from "@/components/utils/ApexBarChart.vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import TabContentCardsWrapper from "@/components/NodePanel/tabContents/TabContentCardsWrapper.vue";

// vue data
const props = defineProps(["benchmarks"]);
const emit = defineEmits(["changedRunning"]);

// data

// methods
const getBenchmarks = computed(() => {
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
  const emitParam = { "cpu-sysbench": getRunningState.value };
  emit("changedRunning", emitParam);
});
</script>

<style scoped></style>
