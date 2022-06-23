<template>
  <TabContentCard>
    <template v-slot:title>
      Score <NoBenchmarksInfo v-if="benchmarkScore === 0" />
    </template>
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
          :score="benchmarkScore"
          :strokeColor="strokeColor"
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
        {{ description }}
      </div>
    </div>
  </TabContentCard>
</template>

<script setup lang="ts">
import { computed, defineProps } from "vue";
import DonutChart from "@/components/utils/DonutChart.vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import Node from "@/models/Node";
import bmUtils from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";
import NoBenchmarksInfo from "@/components/NodePanel/tabContents/Benchmark/utils/NoBenchmarksInfo.vue";

// vue data
const props = defineProps([
  "strokeColor",
  "description",
  "nodeID",
  "benchmarkType",
]);

// data
const benchmarkScore = computed(() => {
  if (props.nodeID != null) {
    const currentScores = Node.find(props.nodeID)?.$getAttributes().scores;
    if (currentScores != null) {
      return bmUtils.getRoundedScore(
        currentScores.details[
          bmUtils.convertToBmTypeUpperCase(props.benchmarkType)
        ].score
      );
    }
  }
  return 0;
});
</script>

<style scoped>
.donut-score-chart {
  width: 191px;
  height: 191px;
}

.donut-score-chart-wrapper {
  display: flex;
}
</style>
