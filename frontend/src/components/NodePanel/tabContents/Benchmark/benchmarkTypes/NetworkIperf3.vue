<template>
  <TabContentCardsWrapper>
    <ScoreCard
      :description="description"
      strokeColor="#5245EA"
      :nodeID="props.nodeID"
      :benchmarkType="BmType.NETWORK_IPERF3"
    />
    <div v-if="chartsData.iPerf3Series[0].data.length === 0" class="no-data">
      run to see results
    </div>
    <TabContentCard v-if="chartsData.iPerf3Series[0].data.length > 0">
      <template v-slot:title> iPerf3</template>
      <apexchart
        :series="chartsData.iPerf3Series"
        :options="chartsData.iPerf3Options"
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
  "iPerf3 is a tool for active measurements of the maximum achievable bandwidth on IP networks. It supports tuning of various parameters related to timing, buffers and protocols (TCP, UDP, SCTP with IPv4 and IPv6). With the iPerf3 benchmark, you can measure the I/O performance of the network hardware and stack used in your Kubernetes cluster.";
const chartsData = computed(() => {
  const query = Benchmark.query()
    .where("node", props.nodeID)
    .where((benchmark: IBenchmark) => {
      return (
        benchmark.id.includes(BmType.NETWORK_IPERF3) &&
        benchmark.metrics != null
      );
    })
    .orderBy("started");

  const latestBm = query.last();
  const currentBms = query.get();

  const { iPerf3Options, iPerf3Series } = iPerf3ApexArguments(
    currentBms,
    latestBm
  );

  return {
    iPerf3Options,
    iPerf3Series,
  };
});

// methods
const iPerf3ApexArguments = (
  currentBms: Collection<Benchmark>,
  latestBm: Item<Benchmark>
) => {
  const iPerf3Series = [
    {
      name: "transfer bitrate (Gbits/sec)",
      data: [] as string[],
    },
  ];

  const categories: string[] = [];

  for (const bm of currentBms) {
    const tmp = bm.$getAttributes();
    const metrics = tmp.metrics;
    const metrics_converted: { [key: string]: string } =
      bmUtils.convertedMetrics(metrics);

    iPerf3Series[0].data.push(metrics_converted.transfer_bitrate);
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

  let iPerf3Options = JSON.parse(JSON.stringify(defaultBarOptions));

  iPerf3Options = {
    ...iPerf3Options,
    chart: {
      ...iPerf3Options.chart,
      id: "iPerf3-" + latestBm?.$getAttributes().id,
      group: BmType.NETWORK_IPERF3,
    },
    xaxis: {
      ...iPerf3Options.xaxis,
      min: currentBms.length - 3,
      max: currentBms.length,
      categories: categories,
      tickPlacement: tickPlacement,
    },
    tooltip: {
      ...iPerf3Options.tooltip,
      fixed: {
        ...iPerf3Options.tooltip.fixed,
        offsetY: -120,
      },
    },
  };

  return { iPerf3Options, iPerf3Series };
};
</script>

<style scoped>
.no-data {
  color: white;
  font-weight: bold;
}
</style>
