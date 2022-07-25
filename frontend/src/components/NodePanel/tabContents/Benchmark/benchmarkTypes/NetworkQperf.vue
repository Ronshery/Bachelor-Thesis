<template>
  <TabContentCardsWrapper>
    <ScoreCard
      :description="description"
      strokeColor="#352BA9"
      :nodeID="props.nodeID"
      :benchmarkType="BmType.NETWORK_QPERF"
      :link="'https://kubestone.io/en/latest/benchmarks/qperf/'"
    />
    <div
      v-if="chartsData.qperfBandWidthSeries[0].data.length === 0"
      class="no-data"
    >
      run to see results
    </div>
    <TabContentCard v-if="chartsData.qperfBandWidthSeries[0].data.length > 0">
      <template v-slot:title>TCP information (transfer)</template>
      <apexchart
        :series="chartsData.qperfBandWidthSeries"
        :options="chartsData.qperfBandWidthOptions"
        :key="Math.random()"
      />
    </TabContentCard>
    <TabContentCard v-if="chartsData.qperfBandWidthSeries[0].data.length > 0">
      <template v-slot:title>TCP information (latency)</template>
      <apexchart
        :series="chartsData.qperfLatencySeries"
        :options="chartsData.qperfLatencyOptions"
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
  defaultBarOptions,
} from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";
import TabContentCardsWrapper from "@/components/NodePanel/tabContents/TabContentCardsWrapper.vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import { Collection, Item } from "@vuex-orm/core";
import ScoreCard from "@/components/NodePanel/tabContents/Benchmark/utils/ScoreCard.vue";

// vue data
const props = defineProps(["nodeID"]);

// data
const description =
  '"Qperf measures bandwidth and latency between two nodes. It can work over TCP/IP as well as the RDMA transports. On one of the nodes, qperf is typically run with no arguments designating it the server node. One may then run qperf on a client node to obtain measurements such as bandwidth, latency and cpu utilization. In its most basic form, qperf is run on one node in server mode by invoking it with no arguments. On the other node, it is run with two arguments: the name of the server node followed by the name of the test. With the qperf benchmark, you can measure the I/O performance of the network hardware and stack used in your Kubernetes cluster."';
const chartsData = computed(() => {
  const query = Benchmark.query()
    .where("node", props.nodeID)
    .where((benchmark: IBenchmark) => {
      return (
        benchmark.id.includes(BmType.NETWORK_QPERF) && benchmark.metrics != null
      );
    })
    .orderBy("started");

  const latestBm = query.last();
  const currentBms = query.get();

  const { qperfBandWidthOptions, qperfBandWidthSeries } =
    qperfBandWidthApexArguments(currentBms, latestBm);

  const { qperfLatencyOptions, qperfLatencySeries } = qperfLatencyApexArguments(
    currentBms,
    latestBm
  );

  return {
    qperfBandWidthOptions,
    qperfBandWidthSeries,
    qperfLatencyOptions,
    qperfLatencySeries,
  };
});

// methods
const qperfBandWidthApexArguments = (
  currentBms: Collection<Benchmark>,
  latestBm: Item<Benchmark>
) => {
  const qperfBandWidthSeries = [
    {
      name: "bandwidth (GB/sec)",
      data: [] as string[],
    },
    {
      name: "msg rate (K/sec)",
      data: [] as string[],
    },
    {
      name: "recv cost (sec/GB)",
      data: [] as string[],
    },
    {
      name: "recv cpus used (%)",
      data: [] as string[],
    },
    {
      name: "send cost (sec/GB)",
      data: [] as string[],
    },
    {
      name: "send cpus used (%)",
      data: [] as string[],
    },
  ];

  const categories: string[] = [];

  for (const bm of currentBms) {
    const tmp = bm.$getAttributes();
    const metrics = tmp.metrics;
    const metrics_converted: { [key: string]: string } =
      bmUtils.convertedMetrics(metrics);

    qperfBandWidthSeries[0].data.push(metrics_converted.tcp_bw_bandwidth);
    qperfBandWidthSeries[1].data.push(metrics_converted.tcp_bw_msg_rate);
    qperfBandWidthSeries[2].data.push(
      metrics_converted.tcp_bw_recv_cost
        ? metrics_converted.tcp_bw_recv_cost
        : "0"
    );
    qperfBandWidthSeries[3].data.push(metrics_converted.tcp_bw_recv_cpus_used);
    qperfBandWidthSeries[4].data.push(
      metrics_converted.tcp_bw_send_cost
        ? metrics_converted.tcp_bw_send_cost
        : "0"
    );
    qperfBandWidthSeries[5].data.push(metrics_converted.tcp_bw_send_cpus_used);
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

  let qperfBandWidthOptions = JSON.parse(JSON.stringify(defaultBarOptions));

  qperfBandWidthOptions = {
    ...qperfBandWidthOptions,
    chart: {
      ...qperfBandWidthOptions.chart,
      id: "qperf-" + latestBm?.$getAttributes().id,
      group: BmType.NETWORK_QPERF,
    },
    xaxis: {
      ...qperfBandWidthOptions.xaxis,
      min: currentBms.length - 3,
      max: currentBms.length,
      categories: categories,
      tickPlacement: tickPlacement,
    },
    tooltip: {
      ...qperfBandWidthOptions.tooltip,
      fixed: {
        ...qperfBandWidthOptions.tooltip.fixed,
        offsetY: -120,
      },
    },
  };

  return { qperfBandWidthOptions, qperfBandWidthSeries };
};

const qperfLatencyApexArguments = (
  currentBms: Collection<Benchmark>,
  latestBm: Item<Benchmark>
) => {
  const qperfLatencySeries = [
    {
      name: "latency (us)",
      data: [] as string[],
    },
    {
      name: "latency local cpu used (%)",
      data: [] as string[],
    },
    {
      name: "latency remote cpu used (%)",
      data: [] as string[],
    },
  ];

  const categories: string[] = [];

  for (const bm of currentBms) {
    const tmp = bm.$getAttributes();
    const metrics = tmp.metrics;
    const metrics_converted: { [key: string]: string } =
      bmUtils.convertedMetrics(metrics);

    qperfLatencySeries[0].data.push(
      metrics_converted.tcp_lat_latency
        ? metrics_converted.tcp_lat_latency
        : "0"
    );
    qperfLatencySeries[1].data.push(metrics_converted.tcp_lat_loc_cpus_used);
    qperfLatencySeries[2].data.push(metrics_converted.tcp_lat_rem_cpus_used);
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

  let qperfLatencyOptions = JSON.parse(JSON.stringify(defaultBarOptions));

  qperfLatencyOptions = {
    ...qperfLatencyOptions,
    chart: {
      ...qperfLatencyOptions.chart,
      id: "qperf-" + latestBm?.$getAttributes().id,
      group: BmType.NETWORK_QPERF,
    },
    xaxis: {
      ...qperfLatencyOptions.xaxis,
      min: currentBms.length - 3,
      max: currentBms.length,
      categories: categories,
      tickPlacement: tickPlacement,
    },
    tooltip: {
      ...qperfLatencyOptions.tooltip,
      fixed: {
        ...qperfLatencyOptions.tooltip.fixed,
        offsetY: -120,
      },
    },
  };

  return { qperfLatencyOptions, qperfLatencySeries };
};
</script>

<style scoped>
.no-data {
  color: white;
  font-weight: bold;
}
</style>
