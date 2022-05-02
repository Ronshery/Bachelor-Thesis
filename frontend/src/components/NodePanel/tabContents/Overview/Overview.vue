<template>
  <div
    style="
      background-color: white;
      margin: 0 1.5em 0 1.5em;
      border-radius: 20px;
    "
  >
    <DonutChart
      :radius="50"
      :maxValue="10"
      :loadedView="true"
      :score="nodeComp.bmScore"
      :isSegmented="true"
      :segments="segments"
    />

    <DonutChart
      v-for="segment in segments"
      :key="segment.score"
      :radius="35"
      :maxValue="10"
      :loadedView="true"
      :score="segment.score"
      :strokeColor="segment.color"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, defineProps } from "vue";
import DonutChart from "@/components/utils/DonutChart.vue";

interface Segment {
  score: number;
  color: string;
}

// vue data
const props = defineProps(["node"]);

// data
const nodeComp = computed(() => {
  if (props.node == null) {
    return {
      bmScore: 0,
    };
  } else {
    return props.node;
  }
});

const segments: Array<Segment> = [
  {
    score: 2,
    color: "#CECAFF",
  },
  {
    score: 5,
    color: "#AEA7FF",
  },
  {
    score: 1,
    color: "#7D72FF",
  },
  {
    score: 3,
    color: "#5245EA",
  },
];
</script>

<style scoped></style>
