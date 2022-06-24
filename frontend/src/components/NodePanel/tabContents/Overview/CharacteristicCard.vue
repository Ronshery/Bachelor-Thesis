<template>
  <apexchart :series="series" :options="options" />
</template>

<script setup lang="ts">
import { defineProps, ref, watch } from "vue";
// data
import bmUtils, {
  BmResource,
  BmType,
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

    const diskBms = [BmType.DISK_FIO, BmType.DISK_IOPING];
    const networkBms = [BmType.NETWORK_QPERF, BmType.NETWORK_IPERF3];

    for (let i = 0; i < bmResources.length; i++) {
      let resource = bmResources[i];
      let score = 0;
      let sum = 0;
      const details = props.nodeScore.details;
      if (resource == BmResource.DISK) {
        for (let diskBm of diskBms) {
          sum += details[bmUtils.convertToBmTypeUpperCase(diskBm)].score;
        }
        score = bmUtils.getRoundedScore(sum / diskBms.length);
      } else if (resource == BmResource.NETWORK) {
        for (let networkBm of networkBms) {
          sum += details[bmUtils.convertToBmTypeUpperCase(networkBm)].score;
        }
        score = bmUtils.getRoundedScore(sum / networkBms.length);
      } else {
        score = bmUtils.getRoundedScore(props.nodeScore[resource].score);
      }
      series.value[0].data[i] = score;
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
