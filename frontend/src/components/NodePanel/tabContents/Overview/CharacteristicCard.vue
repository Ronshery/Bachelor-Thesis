<template>
  <apexchart :series="series" :options="options" />
</template>

<script setup lang="ts">
import { defineProps, watch, ref } from "vue";

// vue data
const props = defineProps(["nodeScore"]);

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

watch(props, () => {
  if (props.nodeScore != null) {
    const bmResources = [
      BmResource.CPU,
      BmResource.MEMORY,
      BmResource.DISK,
      BmResource.NETWORK,
    ];
    for (let i = 0; i < bmResources.length; i++) {
      let resource = bmResources[i];
      series.value[0].data[i] = parseFloat(
        Number(props.nodeScore[resource].score).toFixed(2)
      );
    }
  }
});

const series = ref([
  {
    data: [0, 0, 0, 0] as number[],
    name: "value",
  },
]);
</script>

<style scoped></style>
