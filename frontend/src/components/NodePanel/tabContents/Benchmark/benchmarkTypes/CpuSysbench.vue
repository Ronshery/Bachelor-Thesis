<template>
  {{ benchmarks }}
  <TabContentCardsWrapper>
    <TabContentCard>
      <template v-slot:title> Latency </template>
      <ApexBarChart
        :series="chartsData.latencySeries"
        :options="chartsData.latencyOptions"
      />
    </TabContentCard>
  </TabContentCardsWrapper>
</template>

<script setup lang="ts">
import { defineProps, computed } from "vue";
import ApexBarChart from "@/components/utils/ApexBarChart.vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import TabContentCardsWrapper from "@/components/NodePanel/tabContents/TabContentCardsWrapper.vue";
import Benchmark from "@/models/Benchmark";
import { IBenchmark } from "@/models/IBenchmark";
import { Collection, Item } from "@vuex-orm/core";

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

  const { latencyOptions, latencySeries } = latencyApexBarArguments(
    currentBms,
    latestBm
  );

  return {
    latencySeries: latencySeries,
    latencyOptions: latencyOptions,
  };
});
// methods

const latencyApexBarArguments = (
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
    categories.push(`${date.getHours()}:${date.getMinutes()}`);
  }

  console.log("series: ");
  console.log(latencySeries);
  console.log("categories: ");
  console.log(categories);

  // on: panning and zoom enabled
  const tickPlacement = currentBms.length <= 3 ? "between" : "on";

  //  because of bug needs to be defined here
  const latencyOptions = {
    chart: {
      id: "latency-" + latestBm?.$getAttributes().id,
      type: "bar",
      group: "cpu-sysbench",
      width: 20,
      stacked: false,
    },
    stroke: {
      colors: ["transparent"],
      width: 5,
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "50%",
        borderRadius: 2,
        dataLabels: {
          position: "top",
        },
      },
    },
    dataLabels: {
      offsetY: -20,
      style: {
        colors: ["#000000"],
      },
    },
    legend: {
      onItemClick: {
        toggleDataSeries: true,
      },
    },
    xaxis: {
      type: "category",
      min: currentBms.length - 3,
      max: currentBms.length,
      categories: categories,
      tickPlacement: tickPlacement,
      labels: {
        formatter: function (value: string) {
          console.log("test");
          if (value == undefined || !value.toString().includes(":")) {
            return "asd";
          }
          let list = value.split(":");
          let scn = list[1];
          if (parseInt(scn) < 10) {
            return `${list[0]}:0${list[1]}`;
          }
          return value;
        },
      },
    },
    yaxis: {
      max: 80,
    },
    noData: {
      text: "run to see results",
      offsetY: -15,
      style: {
        color: "#000000",
      },
    },
  };
  return { latencyOptions, latencySeries };
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

<style scoped></style>
