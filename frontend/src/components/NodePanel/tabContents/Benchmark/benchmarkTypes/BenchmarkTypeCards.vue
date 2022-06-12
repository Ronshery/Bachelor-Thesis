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
          <span class="benchmark-type-title">{{ bmType }}</span>
          <DropDown
            v-if="isNetworkBenchmark(bmType)"
            :bmType="bmType"
            :nodeID="nodeID"
            @networkSelected="updateSelectValue"
            :key="bmType"
          />
          <span
            class="run-wrapper"
            :class="{
              'run-disabled':
                selections[bmType] === '0' || runningState[bmType],
            }"
          >
            <span
              :class="{ 'cursor-pointer': selections[bmType] !== '0' }"
              v-if="!runningState[bmType]"
              @click="runBenchmark(bmType)"
            >
              <img
                class="run-icon"
                alt="run"
                :src="require('@/assets/benchmark/benchmark-run-icon.svg')"
              />
              <span :class="{ 'run-text': selections[bmType] !== '0' }">
                run
              </span>
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
      <MemorySysbench
        v-if="bmType === BmType.MEMORY_SYSBENCH"
        :nodeID="nodeID"
      />
      <DiskIoping v-if="bmType === BmType.DISK_IOPING" :nodeID="nodeID" />
      <DiskFio v-if="bmType === BmType.DISK_FIO" :nodeID="nodeID" />
      <NetworkIperf3 v-if="bmType === BmType.NETWORK_IPERF3" :nodeID="nodeID" />
      <NetworkQperf v-if="bmType === BmType.NETWORK_QPERF" :nodeID="nodeID" />
    </TabContentCard>
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref, Ref } from "vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import CpuSysbench from "@/components/NodePanel/tabContents/Benchmark/benchmarkTypes/CpuSysbench.vue";
import Benchmark from "@/models/Benchmark";
import { BmType } from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";
import MemorySysbench from "@/components/NodePanel/tabContents/Benchmark/benchmarkTypes/MemorySysbench.vue";
import DiskIoping from "@/components/NodePanel/tabContents/Benchmark/benchmarkTypes/DiskIoping.vue";
import DiskFio from "@/components/NodePanel/tabContents/Benchmark/benchmarkTypes/DiskFio.vue";
import NetworkIperf3 from "@/components/NodePanel/tabContents/Benchmark/benchmarkTypes/NetworkIperf3.vue";
import DropDown from "@/components/NodePanel/tabContents/Benchmark/utils/DropDown.vue";
import NetworkQperf from "@/components/NodePanel/tabContents/Benchmark/benchmarkTypes/NetworkQperf.vue";

// vue data
const props = defineProps(["bmTypes", "nodeID", "runningState"]);

// data
let iPerf3SelectValue = ref("0");
let qperfSelectValue = ref("0");
const selections = ref<{ [key: string]: Ref<string> }>({
  [BmType.NETWORK_IPERF3]: iPerf3SelectValue,
  [BmType.NETWORK_QPERF]: qperfSelectValue,
});

// methods
const runBenchmark = (benchmarkType: BmType) => {
  let nodeParam = props.nodeID;
  if (selections.value[benchmarkType] == "0") {
    return;
  }
  if (isNetworkBenchmark(benchmarkType)) {
    nodeParam = props.nodeID + "@@@" + selections.value[benchmarkType];
  }
  Benchmark.dispatch("runBenchmark", {
    benchmarkType: benchmarkType,
    nodeID: nodeParam,
  });
};

const updateSelectValue = (param: { bmType: BmType; value: string }) => {
  if (param.bmType == BmType.NETWORK_IPERF3) {
    iPerf3SelectValue.value = param.value;
  } else {
    qperfSelectValue.value = param.value;
  }
};

const isNetworkBenchmark = (benchmarkType: BmType) => {
  return (
    benchmarkType == BmType.NETWORK_IPERF3 ||
    benchmarkType == BmType.NETWORK_QPERF
  );
};
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
}

.run-icon:hover + .run-text {
  color: #bdbdbd;
}

.cursor-pointer {
  cursor: pointer;
}

.run-disabled {
  opacity: 30%;
}

.run-text:hover {
  color: #bdbdbd;
}

.running-icon {
  width: 24px;
  position: relative;
  top: 6px;
  margin-right: 5px;
  animation: spin 2s linear infinite;
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

<style>
.no-data {
  color: white;
  font-weight: bold;
  width: 100%;
}
</style>
