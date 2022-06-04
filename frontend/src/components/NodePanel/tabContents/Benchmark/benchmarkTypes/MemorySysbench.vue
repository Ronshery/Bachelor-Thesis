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
            :strokeColor="'#AEA7FF'"
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
      <template v-slot:title> Fixed values </template>
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
import { computed, defineProps } from "vue";
import Benchmark from "@/models/Benchmark";
import { IBenchmark } from "@/models/IBenchmark";
import bmUtils, {
  BmType,
  mappings,
} from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";
import InnerTableCard from "@/components/NodePanel/tabContents/InnerTableCard.vue";
import DonutChart from "@/components/utils/DonutChart.vue";
import TabContentCardsWrapper from "@/components/NodePanel/tabContents/TabContentCardsWrapper.vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";

// vue data
const props = defineProps(["nodeID"]);

// data
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
    globalOptions = {
      num_threads: metrics.number_of_threads,
      block_size: metrics.block_size,
      total_size: metrics.total_size,
      operation: metrics.operation,
      total_time: bmUtils.convertTotalTime(metrics.total_time),
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
