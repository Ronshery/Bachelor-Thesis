<template>
  <Chart
    :size="props.size"
    :data="props.data"
    :margin="margin"
    :direction="direction"
    :axis="axis"
  >
    <template #layers>
      <Grid strokeDasharray="2,2" />
      <Line
        :dataKeys="dataKeys"
        type="monotone"
        :lineStyle="{
          stroke: '#9f7aea',
        }"
      />
      <!--      <Marker
        :value="1000"
        label="Mean."
        color="green"
        :strokeWidth="2"
        strokeDasharray="6 6"
      />-->
    </template>
    <template #widgets>
      <Tooltip borderColor="#48CAE4" />
    </template>
  </Chart>
</template>

<script setup lang="ts">
import { ref, defineProps, withDefaults } from "vue";
import { Chart, Grid, Line, Tooltip } from "vue3-charts";

interface Props {
  data: { time: string; value: string }[];
  size?: { width: number; height: number };
}
// vue data
const props = withDefaults(defineProps<Props>(), {
  data(props: Readonly<Props>): { time: string; value: string }[] {
    return [];
  },
  size(props: Readonly<Props>): { width: number; height: number } {
    return { width: 400, height: 320 };
  },
});

// data
const dataKeys: [string, string] = ["time", "value"];
const direction = ref("horizontal");
const margin = ref({
  left: 20,
  top: 20,
  right: 20,
  bottom: 20,
});
const axis = ref({
  primary: {
    type: "band",
  },
  secondary: {
    domain: ["0", "100"],
    type: "linear",
    ticks: 20,
  },
});
</script>

<style>
.tick > text {
  color: white !important;
}
</style>
