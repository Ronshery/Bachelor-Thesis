<template>
  <div class="donut-chart-container">
    <div class="donut-chart-wrapper">
      <DonutChart
        class="segmented-donut"
        :radius="80"
        :x="95"
        :y="95"
        :strokeWidth="30"
        :maxValue="10"
        :loadedView="true"
        :score="score"
        :isSegmented="true"
        :segments="segments"
      />
    </div>

    <div class="segments-donut-chart">
      <div class="row" v-for="segment in segments" :key="segment.score">
        <div>
          <DonutChart
            class="segment-donut-chart"
            :radius="35"
            :x="42"
            :y="42"
            :strokeWidth="13"
            :maxValue="10"
            :loadedView="true"
            :score="segment.score"
            :strokeColor="segment.color"
          />
        </div>

        <div class="benchmark-description">
          <div class="benchmark-description-inner">
            <span class="benchmark-name"> {{ segment.benchmark }}</span>

            <div>
              {{ segment.text }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import DonutChart from "@/components/utils/DonutChart.vue";

// vue data
const props = defineProps(["segments", "score"]);
</script>

<style scoped>
.donut-chart-container {
  display: flex;
  background-color: white;
  border-radius: 20px;
  padding: 2em;
  margin-bottom: 1.5em;
}
.segmented-donut {
  width: 190px;
  height: 190px;
  margin: 0 3em 0 2em;
}
.segment-donut-chart {
  width: 85px;
  height: 85px;
}

.segments-donut-chart {
  display: flex;
  flex-direction: column;
}

.row {
  display: flex;
  margin-bottom: 1em;
}

.row:last-child {
  margin-bottom: unset;
}

.benchmark-name {
  font-weight: bold;
}

.benchmark-description {
  border-radius: 11px;
  box-shadow: 0 4px 4px 4px rgba(0, 0, 0, 0.25);
  height: 61px;
  margin-left: 1em;
  padding: 10px 10px 2px 10px;
}

.benchmark-description-inner {
  overflow: auto;
  height: 56px;
}

.donut-chart-wrapper {
  align-self: center;
}

::-webkit-scrollbar-thumb {
  background: #cecaff;
  border-radius: 50px !important;
}

::-webkit-scrollbar {
  width: 6px;
}
</style>
