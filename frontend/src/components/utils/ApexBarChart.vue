<template>
  <div id="barchart" ref="barchart"></div>
  <apexchart type="bar" :options="options" :series="series"></apexchart>
</template>

<script setup lang="ts">
const options = {
  chart: {
    type: "bar",
    stacked: true,
  },
  plotOptions: {
    bar: {
      horizontal: true,
    },
  },
  legend: {
    onItemClick: {
      toggleDataSeries: false,
    },
  },
  xaxis: {
    categories: [""],
  },
};

const series = [
  {
    name: "min",
    data: [400],
  },
  {
    name: "avg",
    data: [300],
  },
  {
    name: "max",
    data: [500],
  },
];
</script>

<style scoped></style>
