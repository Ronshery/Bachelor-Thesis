<template>
  <div v-if="errorMsg != ''" class="error">
    {{ errorMsg }}
    <div class="lds-ring">
      <div></div>
      <div></div>
      <div></div>
      <div></div>
    </div>
  </div>
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
const props = defineProps(["options", "series", "errorMsg"]);

// data
const max = new Date().getTime(); // Current timestamp
const min = new Date(max - 5 * 60000).getTime(); // timestamp 90 days before

const range = max - min;
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
    range: range,
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

<style scoped>
.error {
  display: inline-block;
  color: #ef4343;
  padding: 3px;
  background-color: #fdc4c4;
  border-radius: 5px;
  margin-left: 1.25em;
  margin-top: 1em;
}
</style>
