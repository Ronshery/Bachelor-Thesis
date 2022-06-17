<template>
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
          :score="score"
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
import { defineProps } from "vue";
import DonutChart from "@/components/utils/DonutChart.vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";

// vue data
const props = defineProps(["score", "strokeColor", "description"]);
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
