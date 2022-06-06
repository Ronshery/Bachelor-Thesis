<template>
  <svg v-if="props.isSegmented">
    <circle
      :r="props.radius"
      :cx="props.x"
      :cy="props.y"
      :stroke-dasharray="0"
      :stroke-dashoffset="0"
      stroke="lightgray"
      fill="none"
      :stroke-width="props.strokeWidth"
      style="pointer-events: none"
    />
    <circle
      class="circle"
      v-for="(segment, index) in props.segments"
      :key="segment"
      :id="'segment-' + index"
      :cx="props.x"
      :cy="props.y"
      :stroke-dasharray="strokeDashArray(scaledScore(segment.score))"
      stroke-dashoffset="0"
      :stroke="segment.color"
      fill="none"
      :stroke-width="props.strokeWidth"
      style="pointer-events: none"
      :r="props.radius"
    />

    <text
      :x="props.x"
      :y="props.y"
      text-anchor="middle"
      alignment-baseline="central"
      style="pointer-events: none"
    >
      {{ props.score }}/{{ props.maxValue }}
    </text>
  </svg>
  <svg v-else>
    <circle
      :r="props.radius"
      :cx="props.x"
      :cy="props.y"
      :stroke-dasharray="0"
      :stroke-dashoffset="0"
      stroke="lightgray"
      fill="none"
      :stroke-width="props.strokeWidth"
      style="pointer-events: none"
    />
    <circle
      class="circle"
      :r="props.radius"
      :cx="props.x"
      :cy="props.y"
      :stroke-dasharray="strokeDashArray(props.score)"
      :stroke-dashoffset="percentToScore(25)"
      :stroke="props.strokeColor"
      fill="none"
      :stroke-width="props.strokeWidth"
      style="pointer-events: none"
    />
    <text
      :x="props.x"
      :y="props.y"
      text-anchor="middle"
      alignment-baseline="central"
      style="pointer-events: none"
    >
      {{ props.score }}/{{ props.maxValue }}
    </text>
  </svg>
</template>

<script setup lang="ts">
import { defineProps, onUpdated, withDefaults } from "vue";

interface Segment {
  score: number;
  color: string;
}

interface Props {
  score: number;
  radius: number;
  x: number;
  y: number;
  strokeWidth: number;
  maxValue: number;
  loadedView: boolean;
  isSegmented?: boolean;
  segments?: Array<Segment>;
  strokeColor?: string;
}

// vue data
const props = withDefaults(defineProps<Props>(), {
  score: 0,
  loadedView: false,
  radius: 0,
  maxValue: 0,
  isSegmented: false,
  segments: () => [],
  strokeColor: "PaleVioletRed",
});

// data
const circumference = 2 * props.radius * Math.PI;

// methods
const strokeDashArray = (score: number) => {
  if (props.loadedView) {
    const segmentLength = convertedScore(score);
    return `${segmentLength} ${circumference - segmentLength}`;
  } else {
    return `0 ${circumference}`;
  }
};

const scaledScore = (score: number) => {
  return score / props.segments.length;
};

onUpdated(() => {
  setStrokeDashOffsets();
});

// currentOffset = circumference - segments total length + first segments offset
const setStrokeDashOffsets = () => {
  let currentOffset;
  let precededSegmentsLength;
  for (let i = 0; i < props.segments.length; i++) {
    let segment = document.getElementById("segment-" + i);
    precededSegmentsLength = 0;
    precededSegmentsLength = getPrecededSegmentsLength(i);
    currentOffset =
      circumference - precededSegmentsLength + percentToScore(-75);
    if (segment != null) {
      segment.setAttribute("stroke-dashoffset", currentOffset.toString());
    }
  }
};

const getPrecededSegmentsLength = (index: number) => {
  let precededSegmentsLength = 0;
  for (let i = 0; i < index; i++) {
    let segment = document.getElementById("segment-" + i);
    if (segment != null) {
      let dashArray = segment.getAttribute("stroke-dasharray");
      if (dashArray != null) {
        precededSegmentsLength += parseInt(dashArray.split(" ")[0]);
      }
    }
  }
  return precededSegmentsLength;
};
const scoreToPercent = (score: number) => (100 * score) / circumference;
const percentToScore = (percent: number) => (circumference * percent) / 100;
// score to segment size
const convertedScore = (score: number) =>
  (score * circumference) / props.maxValue;
</script>

<style>
.circle {
  transition: all 1200ms;
  transition-property: stroke-dasharray, stroke-dashoffset;
}
</style>
