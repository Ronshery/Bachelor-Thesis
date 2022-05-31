<template>
  <div id="barchart" ref="barchart"></div>
  <apexchart type="bar" :options="options" :series="props.series"></apexchart>
</template>

<script setup lang="ts">
import { defineProps } from "vue";

// vue data
const props = defineProps(["series"]);
const options = {
  chart: {
    type: "bar",
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: "30%",
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
    categories: [""],
  },
  noData: {
    text: "run to see results",
    offsetY: -15,
    style: {
      color: "#000000",
    },
  },
};

const series = [
  {
    name: "min",
    data: ["400", "200"],
  },
  {
    name: "avg",
    data: ["300", "250"],
  },
  {
    name: "max",
    data: ["500", "70"],
  },
];
</script>

<style scoped></style>
