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
            :strokeColor="'#5245EA'"
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
          fio is a tool that will spawn a number of threads or processes doing a
          particular type of I/O action as specified by the user. The typical
          use of fio is to write a job file matching the I/O load one wants to
          simulate. With the fio benchmark you can measure the I/O performance
          of the disks used in your Kubernetes cluster.
        </div>
      </div>
    </TabContentCard>
    <TabContentCard>
      <template v-slot:title> Fixed values </template>
      <InnerTableCard
        :listAsObject="chartsData.globalOptions"
        :mappings="mappings"
      />
    </TabContentCard>
    <TabContentCard>
      <template v-slot:title> Fio </template>
      <apexchart
        :series="chartsData.fioSeries"
        :options="chartsData.fioOptions"
        :key="Math.random()"
      />
    </TabContentCard>
  </TabContentCardsWrapper>
</template>

<script setup lang="ts">
import { computed, defineProps } from "vue";
import Benchmark from "@/models/Benchmark";
import { IBenchmark } from "@/models/IBenchmark";
import bmUtils, {
  BmType,
  mappings,
  defaultBarOptions,
} from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";
import InnerTableCard from "@/components/NodePanel/tabContents/InnerTableCard.vue";
import DonutChart from "@/components/utils/DonutChart.vue";
import TabContentCardsWrapper from "@/components/NodePanel/tabContents/TabContentCardsWrapper.vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import { Collection, Item } from "@vuex-orm/core";

// vue data
const props = defineProps(["nodeID"]);

// data
const chartsData = computed(() => {
  const query = Benchmark.query()
    .where("node", props.nodeID)
    .where((benchmark: IBenchmark) => {
      return (
        benchmark.id.includes(BmType.DISK_FIO) && benchmark.metrics != null
      );
    })
    .orderBy("started");

  const latestBm = query.last();
  const currentBms = query.get();

  const { latencyOptions, latencySeries } = bmUtils.latencyApexArguments(
    currentBms,
    latestBm,
    BmType.DISK_FIO
  );

  const { fioOptions, fioSeries } = fioApexArguments(currentBms, latestBm);

  const metrics = latestBm?.$getAttributes().metrics;

  let globalOptions = undefined;
  if (metrics) {
    globalOptions = {
      number_of_processes: metrics.number_of_processes,
    };
  }

  return {
    latencySeries,
    latencyOptions,
    fioOptions,
    fioSeries,
    globalOptions,
  };
});

// methods
const fioApexArguments = (
  currentBms: Collection<Benchmark>,
  latestBm: Item<Benchmark>
) => {
  const fioSeries = [
    {
      name: "write iops",
      data: [] as string[],
    },
    {
      name: "write mibps",
      data: [] as string[],
    },
  ];

  const categories: string[] = [];

  for (const bm of currentBms) {
    const tmp = bm.$getAttributes();
    const metrics = tmp.metrics;
    fioSeries[0].data.push(metrics.write_iops);
    fioSeries[1].data.push(metrics.write_mibps);
    const date = new Date(tmp.started + "Z");
    const minutes =
      date.getMinutes() < 10 ? `0${date.getMinutes()}` : date.getMinutes();
    categories.push(`${date.getHours()}:${minutes}`);
  }

  // on: panning and zoom enabled
  const tickPlacement = currentBms.length <= 3 ? "between" : "on";

  let fioOptions = JSON.parse(JSON.stringify(defaultBarOptions));

  fioOptions = {
    ...fioOptions,
    chart: {
      ...fioOptions.chart,
      id: "fio-" + latestBm?.$getAttributes().id,
      group: BmType.DISK_FIO,
    },
    xaxis: {
      ...fioOptions.xaxis,
      min: currentBms.length - 3,
      max: currentBms.length,
      categories: categories,
      tickPlacement: tickPlacement,
    },
    tooltip: {
      ...fioOptions.tooltip,
      fixed: {
        ...fioOptions.tooltip.fixed,
        offsetY: -120,
      },
    },
  };

  return { fioOptions, fioSeries };
};
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
