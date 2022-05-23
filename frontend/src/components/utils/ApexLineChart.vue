<template>
  <apexchart
    width="100%"
    height="auto"
    :options="options"
    :series="series"
  ></apexchart>
</template>

<script setup lang="ts">
import { defineProps } from "vue";

// vue data
const props = defineProps(["options", "series"]);

// data
const options = {
  animations: {
    enabled: true,
    speed: 4000,
  },
  tooltip: {
    theme: "light",
    marker: {
      show: false,
    },
    x: {
      formatter: (x: number) => {
        let date = new Date(x);
        return `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
      },
    },
  },
  stroke: {
    colors: ["#cecaff"],
  },
  dataLabels: {
    style: {
      colors: ["#FFFFFF", "#E91E63", "#9C27B0"],
    },
  },
  markers: {
    colors: ["#000000"],
  },
  grid: {
    column: {
      colors: ["#F44336", "#E91E63", "#9C27B0"],
    },
  },
  chart: {
    id: "vuechart-example",
  },
  xaxis: {
    type: "datetime",
    labels: {
      datetimeUTC: false,
      style: {
        colors: "#FFFFFF",
      },
    },
  },
  yaxis: {
    labels: {
      style: {
        colors: "#FFFFFF",
      },
    },
  },
  noData: {
    text: "Loading...",
    style: {
      color: "#FFFFFF",
    },
  },
};
</script>

<style scoped></style>
