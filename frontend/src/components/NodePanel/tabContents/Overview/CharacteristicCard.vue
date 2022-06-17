<template>
  <apexchart :series="series" :options="options" />
</template>

<script setup lang="ts">
// data
import { BmResource } from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";

const options = {
  chart: {
    height: 350,
    type: "radar",
  },
  fill: {
    opacity: 0.5,
  },
  plotOptions: {
    radar: {
      size: 140,
      polygons: {
        strokeColors: "#e9e9e9",
        fill: {
          colors: ["#f8f8f8", "#fff"],
        },
      },
    },
  },
  colors: ["#7D72FF"],
  xaxis: {
    categories: [
      BmResource.CPU,
      BmResource.MEMORY,
      BmResource.DISK,
      BmResource.NETWORK,
    ],
    labels: {
      style: {
        fontSize: "15px",
      },
    },
  },
  yaxis: {
    show: true,
    labels: {
      style: {
        offsetY: 5,
      },
    },
    max: 10,
    min: 0,
  },
  dataLabels: {
    enabled: true,
  },
};

const series = [
  {
    data: [10, 5, 6, 3],
    name: "value",
  },
];
</script>

<style scoped></style>
