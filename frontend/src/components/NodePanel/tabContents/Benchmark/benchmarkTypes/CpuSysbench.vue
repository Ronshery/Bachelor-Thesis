<template>
  <div v-if="!chartsData.globalOptions" class="no-data">run to see results</div>
  <TabContentCardsWrapper v-else>
    <TabContentCard>
      <template v-slot:title> Score </template>
      <div class="donut-score-chart-wrapper">
        <div>
          <DonutChart
            class="donut-score-chart"
            style="font-size: 21px"
            :radius="80"
            :x="95"
            :y="95"
            :strokeWidth="30"
            :maxValue="10"
            :loadedView="true"
            :score="5"
            :strokeColor="'#CECAFF'"
            :isSegmented="false"
          />
        </div>
        <div
          style="
            padding: 10px;
            border-radius: 20px;
            box-shadow: 0 4px 4px 4px rgba(0, 0, 0, 0.25);
            margin-left: 2em;
          "
        >
          sysbench is a scriptable multi-threaded benchmark tool based on
          LuaJIT. It is most frequently used for database benchmarks, but can
          also be used to create arbitrarily complex workloads that do not
          involve a database server.
        </div>
      </div>
    </TabContentCard>
    <TabContentCard>
      <template v-slot:title> Options </template>
      <InnerTableCard
        :listAsObject="chartsData.globalOptions"
        :mappings="mappings"
      />
    </TabContentCard>
    <TabContentCard :cssStyle="{ minHeight: '400px' }">
      <template v-slot:title> Latency </template>
      <apexchart
        :series="chartsData.latencySeries"
        :options="chartsData.latencyOptions"
        :key="Math.random()"
      />
    </TabContentCard>
    <TabContentCard>
      <template v-slot:title> Events </template>
      <apexchart
        :series="chartsData.eventsSeries"
        :options="chartsData.eventsOptions"
        :key="Math.random()"
      />
    </TabContentCard>
  </TabContentCardsWrapper>
</template>

<script setup lang="ts">
import { defineProps, computed } from "vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import TabContentCardsWrapper from "@/components/NodePanel/tabContents/TabContentCardsWrapper.vue";
import Benchmark from "@/models/Benchmark";
import { IBenchmark } from "@/models/IBenchmark";
import { Collection, Item } from "@vuex-orm/core";
import {
  defaultBarOptions,
  mappings,
} from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";
import InnerTableCard from "@/components/NodePanel/tabContents/InnerTableCard.vue";
import DonutChart from "@/components/utils/DonutChart.vue";
// vue data
const props = defineProps(["nodeID"]);

// data
const benchmarks = computed(() => {
  const query = Benchmark.query()
    .where("node", props.nodeID)
    .where((benchmark: IBenchmark) => {
      return benchmark.id.includes("cpu-sysbench");
    })
    .orderBy("started");
  const currentBms = query.get();
  const runningBms = query.where("metrics", null).get();
  console.log("bms: ");
  console.log(currentBms);
  console.log("current running BMs: ");
  console.log(runningBms);

  return currentBms;
});

const chartsData = computed(() => {
  console.log("");
  console.log("");
  console.log("lets do series");
  const query = Benchmark.query()
    .where("node", props.nodeID)
    .where((benchmark: IBenchmark) => {
      return benchmark.id.includes("cpu-sysbench") && benchmark.metrics != null;
    })
    .orderBy("started");

  const latestBm = query.last();
  const currentBms = query.get();

  const { latencyOptions, latencySeries } = latencyApexArguments(
    currentBms,
    latestBm
  );

  const { eventsOptions, eventsSeries } = eventsApexArguments(
    currentBms,
    latestBm
  );

  const metrics = latestBm?.$getAttributes().metrics;
  let globalOptions = undefined;
  if (metrics) {
    globalOptions = {
      num_threads: metrics.num_threads,
      prime_numbers_limit: metrics.prime_numbers_limit,
      total_time: convertTotalTime(metrics.total_time),
    };
  }

  return {
    latencySeries,
    latencyOptions,
    eventsOptions,
    eventsSeries,
    globalOptions,
  };
});

// methods
const convertTotalTime = (time: string) => {
  let substr = time.toString().substring(0, time.length - 1);
  let convertedTime = Number(substr).toFixed(0);
  convertedTime = convertedTime + time[time.length - 1];
  return convertedTime;
};
const latencyApexArguments = (
  currentBms: Collection<Benchmark>,
  latestBm: Item<Benchmark>
) => {
  const latencySeries = [
    {
      name: "min",
      data: [] as string[],
    },
    {
      name: "avg",
      data: [] as string[],
    },
    {
      name: "max",
      data: [] as string[],
    },
    {
      name: "95p",
      data: [] as string[],
    },
  ];
  const categories: string[] = [];
  for (let bm of currentBms) {
    let tmp = bm.$getAttributes();
    let metrics = tmp.metrics;
    latencySeries[0].data.push(metrics.latency_min);
    latencySeries[1].data.push(metrics.latency_avg);
    latencySeries[2].data.push(metrics.latency_max);
    latencySeries[3].data.push(metrics.latency_95p);
    let date = new Date(tmp.started + "Z");
    let minutes =
      date.getMinutes() < 10 ? `0${date.getMinutes()}` : date.getMinutes();
    categories.push(`${date.getHours()}:${minutes}`);
  }

  // on: panning and zoom enabled
  const tickPlacement = currentBms.length <= 3 ? "between" : "on";

  //  because of bug needs to be defined here
  let latencyOptions = JSON.parse(JSON.stringify(defaultBarOptions));
  latencyOptions = {
    ...latencyOptions,
    chart: {
      ...latencyOptions.chart,
      id: "latency-" + latestBm?.$getAttributes().id,
      group: "cpu-sysbench",
    },
    xaxis: {
      ...latencyOptions.xaxis,
      min: currentBms.length - 3,
      max: currentBms.length,
      categories: categories,
      tickPlacement: tickPlacement,
    },
    tooltip: {
      ...latencyOptions.tooltip,
      fixed: {
        ...latencyOptions.tooltip.fixed,
        offsetY: -120,
      },
    },
  };
  return { latencyOptions, latencySeries };
};

const eventsApexArguments = (
  currentBms: Collection<Benchmark>,
  latestBm: Item<Benchmark>
) => {
  const eventsSeries = [
    {
      name: "#events per second",
      data: [] as string[],
    },
    {
      name: "#events avg",
      data: [] as string[],
    },
    {
      name: "#events stddev",
      data: [] as string[],
    },
    {
      name: "exctime avg",
      data: [] as string[],
    },
    {
      name: "exctime stddev",
      data: [] as string[],
    },
  ];
  const categories: string[] = [];
  for (let bm of currentBms) {
    let tmp = bm.$getAttributes();
    let metrics = tmp.metrics;
    eventsSeries[0].data.push(Number(metrics.events_per_second).toFixed(0));
    eventsSeries[1].data.push(Number(metrics.fairness_events_avg).toFixed(0));
    eventsSeries[2].data.push(
      Number(metrics.fairness_events_stddev).toFixed(0)
    );
    eventsSeries[3].data.push(Number(metrics.fairness_exctime_avg).toFixed(2));
    eventsSeries[4].data.push(
      Number(metrics.fairness_exctime_stddev).toFixed(2)
    );
    let date = new Date(tmp.started + "Z");
    console.log(eventsSeries);
    let minutes =
      date.getMinutes() < 10 ? `0${date.getMinutes()}` : date.getMinutes();
    categories.push(`${date.getHours()}:${minutes}`);
  }
  const tickPlacement = currentBms.length <= 3 ? "between" : "on";

  let eventsOptions = JSON.parse(JSON.stringify(defaultBarOptions));
  eventsOptions = {
    ...eventsOptions,
    chart: {
      ...eventsOptions.chart,
      id: "events-" + latestBm?.$getAttributes().id,
      group: "cpu-sysbench",
    },
    xaxis: {
      ...eventsOptions.xaxis,
      min: currentBms.length - 3,
      max: currentBms.length,
      categories: categories,
      tickPlacement: tickPlacement,
    },
  };
  return { eventsOptions, eventsSeries };
};
/* for multiple y axis combinations
*     yaxis: [
      {
        seriesName: "95p",
        title: {
          text: "min, avg, 95p",
        },
      },
      {
        show: false,
        seriesName: "95p",
      },
      {
        opposite: true,
        title: {
          text: "max",
        },
        seriesName: "max",
      },
      {
        show: false,
        seriesName: "95p",
      },
    ],
* */
</script>

<style scoped>
.no-data {
  color: white;
  font-weight: bold;
}

.donut-score-chart {
  width: 191px;
  height: 191px;
}

.donut-score-chart-wrapper {
  display: flex;
}
</style>
