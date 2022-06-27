<template>
  <apexchart :series="series" :options="options" />
</template>

<script setup lang="ts">
import { defineProps, ref, watch } from "vue";
// data
import bmUtils, {
  BmResource,
} from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";

// vue data
const props = defineProps(["nodeScore"]);

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
        colors: ["black", "black", "black", "black"],
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
      series.value[0].data[i] = bmUtils.getRoundedScore(
        props.nodeScore[resource].score
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
