<template>
  <TabContentCardsWrapper>
    <TabContentCard>
      <template v-slot:title> Score</template>
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
          iPerf3 is a tool for active measurements of the maximum achievable
          bandwidth on IP networks. It supports tuning of various parameters
          related to timing, buffers and protocols (TCP, UDP, SCTP with IPv4 and
          IPv6). With the iPerf3 benchmark, you can measure the I/O performance
          of the network hardware and stack used in your Kubernetes cluster.
        </div>
      </div>
    </TabContentCard>
    <TabContentCard>
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
import {
  BmType,
  defaultBarOptions,
} from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";
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
    iPerf3Series[0].data.push(metrics.transfer_bitrate);
    const date = new Date(tmp.started + "Z");
    const minutes =
      date.getMinutes() < 10 ? `0${date.getMinutes()}` : date.getMinutes();
    categories.push(`${date.getHours()}:${minutes}`);
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

.donut-score-chart {
  width: 191px;
  height: 191px;
}

.donut-score-chart-wrapper {
  display: flex;
}
</style>
