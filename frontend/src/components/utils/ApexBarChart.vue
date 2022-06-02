<template>
  <apexchart
    type="bar"
    :options="options"
    :series="series"
    :key="options.chart.id"
  ></apexchart>
</template>

<script setup lang="ts">
import { defineProps } from "vue";

// vue data
const props = defineProps(["series", "options"]);

/*
const options = ref({
  chart: {
    type: "bar",
    stacked: false,
  },
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 2,
      dataLabels: {
        position: "top",
      },
    },
  },
  dataLabels: {
    offsetY: -20,
    style: {
      colors: ["#000000"],
    },
  },
  legend: {
    onItemClick: {
      toggleDataSeries: true,
    },
  },
  xaxis: {
    type: "category",
    categories: props.categories,
    tickPlacement: "on",
  },
  yaxis: {
    max: 50,
  },
  noData: {
    text: "run to see results",
    offsetY: -15,
    style: {
      color: "#000000",
    },
  },
});
*/
</script>

<style scoped></style>
