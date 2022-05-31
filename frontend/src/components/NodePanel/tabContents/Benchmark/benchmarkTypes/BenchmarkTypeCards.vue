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
          <span
            v-if="bmType === 'cpu-sysbench' && runningState['cpu-sysbench']"
          >
            running...
          </span>
        </span>
      </template>
      <CpuSysbench
        v-if="bmType === 'cpu-sysbench'"
        :benchmarks="benchmarksByResourceType('cpu')"
        :nodeID="nodeID"
        @changedRunning="updateRunningState"
      />
      <div v-if="bmType === 'memory-sysbench'">
        {{ benchmarksByResourceType("memory") }}memory-sysbench results
      </div>
      <div v-if="bmType === 'disk-ioping'">
        {{ benchmarksByResourceType("disk-ioping") }}disk-ioping results
      </div>
      <div v-if="bmType === 'disk-fio'">
        {{ benchmarksByResourceType("disk-fio") }}disk-fio results
      </div>
      <div v-if="bmType === 'network-iperf3'">
        {{ benchmarksByResourceType("network-iperf3") }}network-iperf3 results
      </div>
      <div v-if="bmType === 'network-qperf'">
        {{ benchmarksByResourceType("network-qperf") }}network-qperf results
      </div>
    </TabContentCard>
  </div>
</template>

<script setup lang="ts">
import { defineProps, computed, ref } from "vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import CpuSysbench from "@/components/NodePanel/tabContents/Benchmark/benchmarkTypes/CpuSysbench.vue";
import { useStore } from "vuex";
import { IBenchmark } from "@/models/IBenchmark";

// vue data
const props = defineProps(["bmTypes", "nodeID"]);
const store = useStore();

// data
let runningState = ref({
  "cpu-sysbench": false,
  "memory-sysbench": false,
  "disk-ioping": false,
  "disk-fio": false,
  "network-iperf3": false,
  "network-qperf": false,
});

const BenchmarkModel = computed(() => store.$db().model("benchmarks"));
const benchmarksByResourceType = computed(() => {
  return function (resourceType: string) {
    let currentBenchmarks = BenchmarkModel.value
      .query()
      .where("node", props.nodeID)
      .where((benchmark: IBenchmark) => {
        return benchmark.id.includes(resourceType);
      });
    return currentBenchmarks.get();
  };
});
// methods
const runBenchmark = (benchmark: string) => {
  BenchmarkModel.value.dispatch("runBenchmark", {
    benchmarkType: benchmark,
    nodeID: props.nodeID,
  });
};
const updateRunningState = (param: { [key: string]: boolean }) => {
  const index: string = Object.keys(param)[0];
  switch (index) {
    case "cpu-sysbench":
      runningState.value["cpu-sysbench"] = param["cpu-sysbench"];
      break;
    case "memory-sysbench":
      runningState.value["memory-sysbench"] = param["memory-sysbench"];
      break;
    case "disk-ioping":
      runningState.value["disk-ioping"] = param["disk-ioping"];
      break;
    case "disk-fio":
      runningState.value["disk-fio"] = param["disk-fio"];
      break;
    case "network-iperf3":
      runningState.value["network-iperf3"] = param["network-iperf3"];
      break;
    case "network-qperf":
      runningState.value["network-qperf"] = param["network-qperf"];
      break;
  }
  console.log("running state:");
  console.log(runningState.value);
};
</script>

<style scoped></style>
