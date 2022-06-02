<template>
  {{ runningState }}
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
          <span v-if="runningState[bmType]"> running... </span>
        </span>
      </template>
      <CpuSysbench v-if="bmType === BmType.CPU_SYSBENCH" :nodeID="nodeID" />
      <div v-if="bmType === BmType.MEMORY_SYSBENCH">
        memory-sysbench results
      </div>
      <div v-if="bmType === BmType.DISK_IOPING">disk-ioping results</div>
      <div v-if="bmType === BmType.DISK_FIO">disk-fio results</div>
      <div v-if="bmType === BmType.NETWORK_IPERF3">network-iperf3 results</div>
      <div v-if="bmType === BmType.NETWORK_QPERF">network-qperf results</div>
    </TabContentCard>
  </div>
</template>

<script setup lang="ts">
import { computed, defineProps } from "vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import CpuSysbench from "@/components/NodePanel/tabContents/Benchmark/benchmarkTypes/CpuSysbench.vue";
import { IBenchmark } from "@/models/IBenchmark";
import Benchmark from "@/models/Benchmark";
import { BmType } from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";

// vue data
const props = defineProps(["bmTypes", "nodeID"]);

// data

// methods
const runBenchmark = (benchmarkType: BmType) => {
  Benchmark.dispatch("runBenchmark", {
    benchmarkType: benchmarkType,
    nodeID: props.nodeID,
  });
};

const runningState = computed(() => {
  const bmTypes = [
    BmType.CPU_SYSBENCH,
    BmType.MEMORY_SYSBENCH,
    BmType.DISK_IOPING,
    BmType.DISK_FIO,
    BmType.NETWORK_IPERF3,
    BmType.NETWORK_QPERF,
  ];
  const query = Benchmark.query().where("node", props.nodeID);
  const runningStateNew = {
    [BmType.CPU_SYSBENCH]: false,
    [BmType.MEMORY_SYSBENCH]: false,
    [BmType.DISK_IOPING]: false,
    [BmType.DISK_FIO]: false,
    [BmType.NETWORK_IPERF3]: false,
    [BmType.NETWORK_QPERF]: false,
  };
  for (let bmType of bmTypes) {
    const runningBmsByType = query
      .where((benchmark: IBenchmark) => {
        return benchmark.id.includes(bmType);
      })
      .where("metrics", null)
      .get();

    runningStateNew[bmType] = runningBmsByType.length > 0;
  }
  return runningStateNew;
});
</script>

<style scoped></style>
