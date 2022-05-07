<template>
  <div class="donut-chart-container">
    <DonutChart
      class="segmented-donut"
      :radius="80"
      :x="95"
      :y="95"
      :strokeWidth="30"
      :maxValue="10"
      :loadedView="true"
      :score="nodeComp.bmScore"
      :isSegmented="true"
      :segments="segments"
    />

    <div class="segments-donut-chart">
      <div class="row" v-for="segment in segments" :key="segment.score">
        <DonutChart
          class="segment-donut-chart"
          :radius="35"
          :x="42"
          :y="42"
          :strokeWidth="13"
          :maxValue="10"
          :loadedView="true"
          :score="segment.score"
          :strokeColor="segment.color"
        />

        <div class="benchmark-description">
          <span class="benchmark-name"> {{ segment.benchmark }}</span>

          <div>
            {{ segment.text }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, defineProps } from "vue";
import DonutChart from "@/components/utils/DonutChart.vue";

interface Segment {
  benchmark: string;
  score: number;
  color: string;
  text: string;
}

// vue data
const props = defineProps(["node"]);

// data
const nodeComp = computed(() => {
  if (props.node == null) {
    return {
      bmScore: 0,
    };
  } else {
    return props.node;
  }
});

const segments: Array<Segment> = [
  {
    benchmark: "cpu-sysbench",
    score: 2,
    color: "#CECAFF",
    text: "sysbench is a scriptable multi-threaded benchmark tool based on LuaJIT. It is most frequently used for database benchmarks, but can also be used to create arbitrarily complex workloads that do not involve a database server.",
  },
  {
    benchmark: "memory-sysbench",
    score: 5,
    color: "#AEA7FF",
    text: "sysbench is a scriptable multi-threaded benchmark tool based on LuaJIT. It is most frequently used for database benchmarks, but can also be used to create arbitrarily complex workloads that do not involve a database server.",
  },
  /*  {
    benchmark: "network-iperf3",
    score: 5,
    color: "#AEA7FF",
  },
  {
    benchmark: "network-qperf",
    score: 5,
    color: "#AEA7FF",
  },*/
  {
    benchmark: "disk-ioping",
    score: 1,
    color: "#7D72FF",
    text: "A tool to monitor I/O latency in real time. It shows disk latency in the same way as ping shows network latency.",
  },
  {
    benchmark: "disk-fio",
    score: 3,
    color: "#5245EA",
    text: "fio is a tool that will spawn a number of threads or processes doing a particular type of I/O action as specified by the user. The typical use of fio is to write a job file matching the I/O load one wants to simulate.",
  },
];
</script>

<style scoped>
.donut-chart-container {
  display: flex;
  background-color: white;
  margin: 0 1.5em 0 1.5em;
  border-radius: 20px;
  padding: 3em;
}
.segmented-donut {
  width: 190px;
  height: 190px;
  align-self: center;
  margin: 0 3em 0 2em;
}
.segment-donut-chart {
  width: 85px;
  height: 85px;
}

.segments-donut-chart {
  display: flex;
  flex-direction: column;
}

.row {
  display: flex;
  margin-bottom: 1em;
}

.row:last-child {
  margin-bottom: unset;
}

.benchmark-name {
  font-weight: bold;
}

.benchmark-description {
  border-radius: 11px;
  box-shadow: 0px 4px 4px 4px rgba(0, 0, 0, 0.25);
  width: 20vw;
  height: 61px;
  overflow: auto;
  margin-left: 1em;
  padding: 10px;
}
</style>
