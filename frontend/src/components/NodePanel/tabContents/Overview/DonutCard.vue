<template>
  <div class="donut-card-container">
    <div class="donut-chart-wrapper">
      <DonutChart
        class="segmented-donut"
        :radius="80"
        :x="95"
        :y="95"
        :strokeWidth="30"
        :maxValue="10"
        :loadedView="true"
        :score="scoreComp.value"
      />
    </div>
    <div class="segments-donut-container">
      <div>
        <div
          class="segment-donut-content-wrapper"
          v-for="segment in segments"
          :key="segment.benchmark"
        >
          <div class="benchmark-name">{{ segment.benchmark }}</div>
          <div class="segment-donut-chart-wrapper">
            <DonutChart
              class="segment-donut-chart"
              :radius="35"
              :x="42"
              :y="42"
              :strokeWidth="13"
              :maxValue="10"
              :loadedView="true"
              :score="bmUtils.getRoundedScore(segment.score)"
              :strokeColor="segment.color"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, watch, ref, computed } from "vue";
import DonutChart from "@/components/utils/DonutChart.vue";
import bmUtils from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";

// vue data
const props = defineProps(["segments", "nodeScore"]);

const scoreVal = ref<number>(0);
watch(props, () => {
  if (props.nodeScore != null) {
    scoreVal.value = bmUtils.getRoundedScore(props.nodeScore.total.score);
  }
});

const scoreComp = computed(() => scoreVal);
</script>

<style scoped>
.donut-card-container {
  display: flex;
  margin-top: 1em;
}

.donut-chart-wrapper {
  width: 50%;
  align-self: center;
}

.segmented-donut {
  width: 190px;
  height: 190px;
  padding: 0 0 0 1.5em;
  font-size: 21px;
}

.segments-donut-container {
  display: inline-block;
  width: 50%;
  margin: 0 1em 0 0;
}

.segment-donut-chart-wrapper {
  margin-left: 15%;
}

.segment-donut-content-wrapper {
  display: inline-block;
  width: 50%;
}

.segment-donut-chart {
  width: 85px;
  height: 85px;
}

.benchmark-name {
  width: 8.2em;
  text-align: center;
  vertical-align: middle;
}
</style>
