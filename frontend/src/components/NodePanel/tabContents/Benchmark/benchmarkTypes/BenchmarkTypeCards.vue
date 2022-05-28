<template>
  {{ benchmarks }}
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
import { defineProps, computed } from "vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import CpuSysbench from "@/components/NodePanel/tabContents/Benchmark/benchmarkTypes/CpuSysbench.vue";
import { useStore } from "vuex";

// vue data
const props = defineProps(["bmTypes", "nodeID"]);
const store = useStore();

// data
const BenchmarkModel = computed(() => store.$db().model("benchmarks"));
const benchmarks = computed(() =>
  BenchmarkModel.value.query().where("node", props.nodeID).get()
);
// methods
const runBenchmark = (benchmark: string) => {
  BenchmarkModel.value.dispatch("runBenchmark", {
    benchmarkType: benchmark,
    nodeID: props.nodeID,
  });
};
</script>

<style scoped></style>
