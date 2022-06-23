<template>
  <TabContentCardsWrapper>
    <ScoreCard
      strokeColor="#CECAFF"
      :description="description"
      :nodeID="props.nodeID"
      :benchmarkType="BmType.MEMORY_SYSBENCH"
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
import { computed, defineProps } from "vue";
import Benchmark from "@/models/Benchmark";
import { IBenchmark } from "@/models/IBenchmark";
import bmUtils, {
  BmType,
  mappings,
} from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";
import InnerTableCard from "@/components/NodePanel/tabContents/InnerTableCard.vue";
import TabContentCardsWrapper from "@/components/NodePanel/tabContents/TabContentCardsWrapper.vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
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
        benchmark.id.includes(BmType.MEMORY_SYSBENCH) &&
        benchmark.metrics != null
      );
    })
    .orderBy("started");

  const latestBm = query.last();
  const currentBms = query.get();

  const { latencyOptions, latencySeries } = bmUtils.latencyApexArguments(
    currentBms,
    latestBm,
    BmType.MEMORY_SYSBENCH
  );

  const { eventsOptions, eventsSeries } = bmUtils.eventsApexArguments(
    currentBms,
    latestBm,
    BmType.MEMORY_SYSBENCH
  );

  const metrics = latestBm?.$getAttributes().metrics;
  let globalOptions = undefined;
  if (metrics) {
    const metrics_converted: { [key: string]: string } =
      bmUtils.convertedMetrics(metrics);
    globalOptions = {
      num_threads: metrics_converted.number_of_threads,
      block_size: metrics_converted.block_size,
      total_size: metrics_converted.total_size,
      operation: metrics_converted.operation,
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
</script>
