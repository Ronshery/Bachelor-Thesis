<template>
  <circle
    v-for="(pos, node) in layoutsNodes"
    :key="node"
    :show="node"
    :r="radius"
    :cx="pos.x"
    :cy="pos.y"
    :stroke-dasharray="0"
    :stroke-dashoffset="0"
    stroke="lightgray"
    fill="none"
    stroke-width="15"
    style="pointer-events: none"
  />
  <circle
    class="circle"
    v-for="(pos, node) in layoutsNodes"
    :key="node"
    :show="node"
    :r="radius"
    :cx="pos.x"
    :cy="pos.y"
    :stroke-dasharray="strokeDashArray(pos.bmScore)"
    :stroke-dashoffset="percentToScore(25)"
    stroke="PaleVioletRed"
    fill="none"
    stroke-width="15"
    style="pointer-events: none"
  />
  <text
    v-for="(pos, node) in layoutsNodes"
    :key="node"
    :x="pos.x"
    :y="pos.y"
    text-anchor="middle"
    alignment-baseline="central"
    style="pointer-events: none"
  >
    {{ pos.bmScore }}/{{ maxValue }}
  </text>
</template>

<script setup lang="ts">
import { defineProps, ref } from "vue";

// vue data
const props = defineProps(["layoutsNodes", "radius", "maxValue", "loadedView"]);

// data
const circumference = 2 * props.radius * Math.PI;
const strokeDashArray = (score: number) => {
  if (props.loadedView) {
    return `${convertedScore(score)} ${circumference - convertedScore(score)}`;
  } else {
    return `0 ${circumference}`;
  }
};
// circumference  === 100%
// x              === 60
// methods
const scoreToPercent = (score: number) => (100 * score) / circumference;
const percentToScore = (percent: number) => (circumference * percent) / 100;
const convertedScore = (score: number) =>
  (score * circumference) / props.maxValue;
</script>

<style scoped>
.circle {
  transition: stroke-dasharray 1200ms;
}
</style>
