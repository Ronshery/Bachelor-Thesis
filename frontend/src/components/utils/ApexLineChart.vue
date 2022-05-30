<template>
  <div v-if="errorMsg !== ''" class="error">
    {{ errorMsg }}
  </div>
  <apexchart
    :options="options"
    :series="series"
    @beforeZoom="beforeZoom"
    @beforeResetZoom="beforeResetZoom"
  ></apexchart>
</template>

<script setup lang="ts">
import { defineProps, ref } from "vue";

interface AxisMinMax {
  min: Date;
  max: Date;
}

interface ApexZoomConfig {
  xaxis: AxisMinMax;
  yaxis: AxisMinMax;
}

// vue data
const props = defineProps(["series", "errorMsg"]);

// data
let initmax = new Date().getTime(); // Current timestamp
let initmin = new Date(initmax - 5 * 60000).getTime(); // timestamp 90 days before
let initrange = initmax - initmin;

const options = ref({
  chart: {
    id: "linechart",
    toolbar: {
      tools: {
        download: false,
      },
    },
  },
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
  xaxis: {
    type: "datetime",
    labels: {
      datetimeUTC: false,
      style: {
        colors: "#FFFFFF",
      },
    },
    axisTicks: {
      show: true,
    },
    range: initrange,
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
});

// methods
const beforeResetZoom = () => {
  options.value = {
    ...options.value,
    xaxis: {
      ...options.value.xaxis,
      axisTicks: {
        show: true,
      },
      range: initrange,
    },
  };
};

const beforeZoom = (chartContext: never, config: ApexZoomConfig) => {
  let max, min;
  let now = new Date();
  let showAxisTicks = true;
  max = new Date(config.xaxis.max).getTime();
  min = new Date(config.xaxis.min).getTime();

  // if max is in future zoom fully out
  if (max > now.getTime()) {
    max = props.series[0].data[props.series[0].data.length - 1].x.getTime();
    min = props.series[0].data[0].x.getTime();
    showAxisTicks = false;
  }
  options.value = {
    ...options.value,
    xaxis: {
      ...options.value.xaxis,
      axisTicks: {
        show: showAxisTicks,
      },
      range: max - min,
    },
  };
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
