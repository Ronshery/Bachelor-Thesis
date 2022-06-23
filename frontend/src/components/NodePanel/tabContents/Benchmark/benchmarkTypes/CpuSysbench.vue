<template>
  <TabContentCardsWrapper>
    <ScoreCard
      :description="description"
      strokeColor="#E3E0FF"
      :nodeID="props.nodeID"
      :benchmarkType="BmType.CPU_SYSBENCH"
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
import bmUtils, {
  mappings,
  BmType,
} from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";
import InnerTableCard from "@/components/NodePanel/tabContents/InnerTableCard.vue";
import ScoreCard from "@/components/NodePanel/tabContents/Benchmark/utils/ScoreCard.vue";

// vue data
const props = defineProps(["nodeID"]);

// data
const description =
  "sysbench is a scriptable multi-threaded benchmark tool based on LuaJIT. It is most frequently used for database benchmarks, but can also be used to create arbitrarily complex workloads that do not involve a database server.";
const chartsData = computed(() => {
  const query = Benchmark.query()
    .where("node", props.nodeID)
    .where((benchmark: IBenchmark) => {
      return (
        benchmark.id.includes(BmType.CPU_SYSBENCH) && benchmark.metrics != null
      );
    })
    .orderBy("started");

  const latestBm = query.last();
  const currentBms = query.get();

  let { latencyOptions, latencySeries } = bmUtils.latencyApexArguments(
    currentBms,
    latestBm,
    BmType.CPU_SYSBENCH
  );

  const { eventsOptions, eventsSeries } = bmUtils.eventsApexArguments(
    currentBms,
    latestBm,
    BmType.CPU_SYSBENCH
  );

  const metrics = latestBm?.$getAttributes().metrics;

  let globalOptions = undefined;
  if (metrics) {
    const metrics_converted: { [key: string]: string } =
      bmUtils.convertedMetrics(metrics);
    globalOptions = {
      num_threads: metrics_converted.num_threads,
      prime_numbers_limit: metrics_converted.prime_numbers_limit,
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
