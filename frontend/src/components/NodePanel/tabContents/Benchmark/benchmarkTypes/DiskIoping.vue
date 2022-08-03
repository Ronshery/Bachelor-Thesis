<template>
  <TabContentCardsWrapper>
    <ScoreCard
      strokeColor="#AEA7FF"
      :description="description"
      :nodeID="props.nodeID"
      :benchmarkType="BmType.DISK_IOPING"
      :link="'https://kubestone.io/en/latest/benchmarks/ioping/'"
    />
    <div v-if="!chartsData.globalOptions" class="no-data">
      run to see results
    </div>
    <TabContentCard v-if="chartsData.globalOptions">
      <template v-slot:title> Fixed values </template>
      <InnerTableCard
        :listAsObject="chartsData.globalOptions"
        :mappings="mappings"
      />
    </TabContentCard>
    <TabContentCard
      v-if="chartsData.globalOptions"
      :cssStyle="{ minHeight: '400px' }"
    >
      <template v-slot:title> Latency </template>
      <apexchart
        :series="chartsData.latencySeries"
        :options="chartsData.latencyOptions"
        :key="Math.random()"
      />
    </TabContentCard>
    <TabContentCard v-if="chartsData.globalOptions">
      <template v-slot:title> I/O operations per second </template>
      <apexchart
        :series="chartsData.iopsSeries"
        :options="chartsData.iopsOptions"
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
import TabContentCardsWrapper from "@/components/NodePanel/tabContents/TabContentCardsWrapper.vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import { Collection, Item } from "@vuex-orm/core";
import ScoreCard from "@/components/NodePanel/tabContents/Benchmark/utils/ScoreCard.vue";

// vue data
const props = defineProps(["nodeID"]);

// data
const description =
  "“A tool to monitor I/O latency in real time. It shows disk latency in the same way as ping shows network latency. With ioping benchmark you can measure the latency of the storage I/O subsystem in your Kubernetes cluster.”";
const chartsData = computed(() => {
  const query = Benchmark.query()
    .where("node", props.nodeID)
    .where((benchmark: IBenchmark) => {
      return (
        benchmark.id.includes(BmType.DISK_IOPING) && benchmark.metrics != null
      );
    })
    .orderBy("started");

  const latestBm = query.last();
  const currentBms = query.get();

  const { latencyOptions, latencySeries } = bmUtils.latencyApexArguments(
    currentBms,
    latestBm,
    BmType.DISK_IOPING
  );

  const { iopsOptions, iopsSeries } = iopsApexArguments(currentBms, latestBm);

  const metrics = latestBm?.$getAttributes().metrics;

  let globalOptions = undefined;
  if (metrics) {
    const metrics_converted: { [key: string]: string } =
      bmUtils.convertedMetrics(metrics);
    globalOptions = {
      number_of_requests: metrics_converted.number_of_requests,
    };
  }

  return {
    latencySeries,
    latencyOptions,
    iopsOptions,
    iopsSeries,
    globalOptions,
  };
});

// methods
const iopsApexArguments = (
  currentBms: Collection<Benchmark>,
  latestBm: Item<Benchmark>
) => {
  const iopsSeries = [
    {
      name: "iops",
      data: [] as string[],
    },
    {
      name: "transfer bitrate (KiB/s)",
      data: [] as string[],
    },
    {
      name: "total duration (ms)",
      data: [] as string[],
    },
  ];

  const categories: string[] = [];

  for (const bm of currentBms) {
    const tmp = bm.$getAttributes();
    const metrics = tmp.metrics;
    const metrics_converted: { [key: string]: string } =
      bmUtils.convertedMetrics(metrics);

    iopsSeries[0].data.push(metrics_converted.iops);
    iopsSeries[1].data.push(metrics_converted.transfer_bitrate);
    iopsSeries[2].data.push(metrics_converted.total_duration);
    const date = new Date(tmp.started + "Z");
    const clock = date.toLocaleString("en-US", {
      hour: "numeric",
      minute: "numeric",
      hour12: true,
    });
    const month =
      date.getMonth() < 10 ? `0${date.getMonth()}` : date.getMonth();
    categories.push(`${month}/${date.getDate()} ${clock}`);
  }

  // on: panning and zoom enabled
  const tickPlacement = currentBms.length <= 3 ? "between" : "on";

  let iopsOptions = JSON.parse(JSON.stringify(defaultBarOptions));

  iopsOptions = {
    ...iopsOptions,
    chart: {
      ...iopsOptions.chart,
      id: "iops-" + latestBm?.$getAttributes().id,
      group: BmType.DISK_IOPING,
    },
    xaxis: {
      ...iopsOptions.xaxis,
      min: currentBms.length - 3,
      max: currentBms.length,
      categories: categories,
      tickPlacement: tickPlacement,
    },
    tooltip: {
      ...iopsOptions.tooltip,
      fixed: {
        ...iopsOptions.tooltip.fixed,
        offsetY: -120,
      },
    },
  };

  return { iopsOptions, iopsSeries };
};
</script>
