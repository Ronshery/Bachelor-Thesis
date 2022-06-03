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
          <span class="benchmark-type-title">{{ bmType }}</span>
          <span class="run-wrapper" :class="{ running: runningState[bmType] }">
            <span style="cursor: pointer" v-if="!runningState[bmType]">
              <img
                class="run-icon"
                alt="run"
                @click="runBenchmark(bmType)"
                :src="require('@/assets/benchmark/benchmark-run-icon.svg')"
              />
              <span class="run-text" @click="runBenchmark(bmType)"> run </span>
            </span>
            <span v-else>
              <img
                class="running-icon"
                alt="running"
                :src="require('@/assets/benchmark/benchmark-running-icon.svg')"
              /><span>running ...</span>
            </span>
          </span>
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

<style scoped>
.benchmark-type-title {
  font-size: 19px;
}

.run-wrapper {
  font-weight: bold;
  background-color: #00000080;
  margin-left: 1em;
  border-radius: 20px;
  padding: 8px 16px 8px 16px;
}

.run-icon {
  width: 16px;
  position: relative;
  top: 3px;
  margin-right: 5px;
  cursor: pointer;
}

.run-text:hover {
  color: lightgray;
}

.running-icon {
  width: 24px;
  position: relative;
  top: 6px;
  margin-right: 5px;
  animation: spin 2s linear infinite;
}

.running {
  background-color: #00000050;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
