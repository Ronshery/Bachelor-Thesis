<template>
  <div v-for="bmType in bmTypes" :key="bmType">
    <TabContentCard
      :cssStyle="{
        backgroundColor: '#4c4f69',
        width: '100%',
      }"
    >
      <template v-slot:title>
        <span style="color: white">
          {{ bmType }}
          <span
            style="color: green; font-weight: bold; cursor: pointer"
            @click="runBenchmark(bmType)"
          >
            run
          </span>
        </span>
      </template>
      <CpuSysbench v-if="bmType == 'cpu-sysbench'" />
    </TabContentCard>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import CpuSysbench from "@/components/NodePanel/tabContents/Benchmark/benchmarkTypes/CpuSysbench.vue";
import benchmarkService from "@/services/benchmark-service";

interface RunResponse {
  id: string;
  spec: object;
}

// vue data
const props = defineProps(["bmTypes", "nodeID"]);

// data
const benchmarkRunResponses: RunResponse[] = [];

// methods
const runBenchmark = (benchmark: string) => {
  console.log(benchmark);
  benchmarkService
    .post(`/benchmark/${benchmark.split("_").join("-")}/${props.nodeID}`)
    .then((response) => {
      console.log(response.data);
      benchmarkRunResponses.push(response.data);
      window.localStorage.setItem(
        "benchmarkRunResponses",
        JSON.stringify(benchmarkRunResponses)
      );
    });
};
</script>

<style scoped></style>
