<template>
  <OverviewLayout>
    <DonutCard :segments="segments" :score="nodeComp.bmScore" />
    <OverviewCard>
      <template v-slot:title> Node info </template>
      <template v-slot:default>
        <div class="wrapper">
          <div
            class="row"
            v-for="(value, index) in nodeInfoComp[0]"
            :key="value"
          >
            <div class="row-element">
              {{ nodeInfoComp[0][index] }}
            </div>
            <div class="row-element row-element-right">
              {{ nodeInfoComp[1][index] }}
            </div>
          </div>
        </div>
      </template>
    </OverviewCard>
    <OverviewCard
      v-for="graph in graphList"
      :key="graph.title"
      :cssStyle="{ backgroundColor: '#4c4f69' }"
      :isSVG="true"
    >
      <template v-slot:title>
        <div class="graph-card-title">{{ graph.title }}</div>
      </template>
      <template v-slot:default>
        <LineChart :data="graph.data.value" :size="LineChartSVGSize" />
      </template>
    </OverviewCard>
  </OverviewLayout>
</template>

<script setup lang="ts">
import { computed, defineProps, ref, watch } from "vue";
import LineChart from "@/components/utils/LineChart.vue";
import benchmarkService from "@/services/benchmark-service";
import DonutCard from "@/components/NodePanel/tabContents/Overview/DonutCard.vue";
import OverviewCard from "@/components/NodePanel/tabContents/Overview/OverviewCard.vue";
import OverviewLayout from "@/components/NodePanel/tabContents/Overview/OverviewLayout.vue";

interface Segment {
  benchmark: string;
  score: number;
  color: string;
  text: string;
}

interface ChartData {
  time: string;
  value: string;
}

interface ILatestDatas {
  [key: string]: ChartData[];
}

// vue data
const props = defineProps(["node", "nodePanelOpen"]);

// data
const nodeComp = computed(() => {
  if (props.node == null) {
    return {
      bmScore: 0,
      metrics: { cpu_busy: [], memory_used: [] },
      status: undefined,
    };
  } else {
    return props.node;
  }
});
const cpuBusyData = ref<ChartData[]>([]);
const memoryUsedData = ref<ChartData[]>([]);
const diskIoUtilData = ref<ChartData[]>([]);

/*const cpuBusyDataComp = computed(() => cpuBusyData.value);
const memoryUsedDataComp = computed(() => memoryUsedData.value);
const diskIoUtilDataComp = computed(() => diskIoUtilData.value);*/

let graphList = [
  {
    title: "CPU busy",
    data: cpuBusyData,
  },
  {
    title: "Memory used",
    data: memoryUsedData,
  },
  {
    title: "Disk IO util",
    data: diskIoUtilData,
  },
];

const segments: Array<Segment> = [
  {
    benchmark: "cpu-sysbench",
    score: 2,
    color: "#CECAFF",
    text: "sysbench is a scriptable multi-threaded benchmark tool based on LuaJIT. It is most frequently used for database benchmarks, but can also be used to create arbitrarily complex workloads that do not involve a database server.",
  },
  {
    benchmark: "memory-sysbench",
    score: 5,
    color: "#AEA7FF",
    text: "sysbench is a scriptable multi-threaded benchmark tool based on LuaJIT. It is most frequently used for database benchmarks, but can also be used to create arbitrarily complex workloads that do not involve a database server.",
  },
  /*  {
    benchmark: "network-iperf3",
    score: 5,
    color: "#AEA7FF",
  },
  {
    benchmark: "network-qperf",
    score: 5,
    color: "#AEA7FF",
  },*/
  {
    benchmark: "disk-ioping",
    score: 1,
    color: "#7D72FF",
    text: "A tool to monitor I/O latency in real time. It shows disk latency in the same way as ping shows network latency.",
  },
  {
    benchmark: "disk-fio",
    score: 3,
    color: "#5245EA",
    text: "fio is a tool that will spawn a number of threads or processes doing a particular type of I/O action as specified by the user. The typical use of fio is to write a job file matching the I/O load one wants to simulate.",
  },
];

// methods
const nodeInfoComp = computed(() => {
  let kubeNodeInfo = nodeComp.value.status;
  let list: [string[], string[]] = [[], []];
  if (kubeNodeInfo) {
    let info = {
      architecture: kubeNodeInfo.nodeInfo.architecture,
      operatingSystem: kubeNodeInfo.nodeInfo.operatingSystem,
      osImage: kubeNodeInfo.nodeInfo.osImage,
      kernelVersion: kubeNodeInfo.nodeInfo.kernelVersion,
      cpu: kubeNodeInfo.allocatable.cpu,
      memory: kubeNodeInfo.allocatable.memory,
      ephemeralStorage: kubeNodeInfo.allocatable["ephemeral-storage"],
      pods: kubeNodeInfo.allocatable.pods,
    };

    let i = 0;
    for (const [key, value] of Object.entries(info)) {
      let keyString = key;
      let valueString = value;
      switch (keyString) {
        case "cpu":
          keyString = "cpu cores";
          break;
        case "operatingSystem":
          keyString = "operating system";
          break;
        case "osImage":
          keyString = "OS image";
          break;
        case "kernelVersion":
          keyString = "kernel version";
          break;
        case "ephemeralStorage":
          keyString = "ephemeral storage";
          break;
        case "pods":
          keyString = "max pods";
          break;
      }

      list[0][i] = keyString;
      list[1][i] = valueString;
      i++;
    }
  }
  return list;
});

const setLineChartSVGSize = () => {
  for (let card of document.getElementsByClassName("chart")) {
    let lineChartSVG = card.firstElementChild;
    if (lineChartSVG) {
      lineChartSVG.setAttribute("width", "100%");
      lineChartSVG.setAttribute("height", "100%");
      LineChartSVGSize.value = {
        width: lineChartSVG.clientWidth,
        height: lineChartSVG.clientHeight,
      };
    }
  }
};

watch(props, () => {
  if (props.nodePanelOpen) {
    setTimeout(() => {
      setLineChartSVGSize();
    });
  }
});

window.addEventListener("resize", () => {
  setLineChartSVGSize();
});

const LineChartSVGSize = ref<{ width: number; height: number }>({
  width: 420,
  height: 300,
});

setInterval(() => {
  fetchData(nodeComp.value.id);
}, 60000);

watch(props, () => {
  if (props.nodePanelOpen) {
    // fetch full data when clicking on node
    resetLatestDatas();
    fetchData(nodeComp.value.id);
  }
});

const resetLatestDatas = () => {
  latestDatas.cpu_busy = [];
  latestDatas.memory_used = [];
  latestDatas.disk_io_util = [];
};

const fetchData = (nodeID: string) => {
  let timeDelta = 480;

  if (nodeID) {
    benchmarkService.get(`/metrics/${nodeID}/${timeDelta}`).then((response) => {
      let dataNames = Object.keys(response.data);
      dataNames = dataNames.filter((key) => key != "node_name");
      dataNames.forEach((dataName) => {
        let data = response.data[dataName];

        if (dataName == "memory_used") {
          memoryUsedData.value = avg(dataName, data, 7);
        } else if (dataName == "cpu_busy") {
          cpuBusyData.value = avg(dataName, data, 7);
        } else if (dataName == "disk_io_util") {
          diskIoUtilData.value = avg(dataName, data, 7);
        }
      });
    });
  }
};

let latestDatas: ILatestDatas = {
  cpu_busy: [],
  memory_used: [],
  disk_io_util: [],
};

const avg = (
  dataName: string,
  data: { time: string; value: string }[],
  size: number
) => {
  let newData: ChartData[] = [];

  switch (dataName) {
    case "cpu_busy":
      if (latestDatas.cpu_busy.length > 0) {
        newData = onlyLastData(dataName, data, size);
      }
      break;
    case "memory_used":
      if (latestDatas.memory_used.length > 0) {
        newData = onlyLastData(dataName, data, size);
      }
      break;
    case "disk_io_util":
      if (latestDatas.disk_io_util.length > 0) {
        newData = onlyLastData(dataName, data, size);
      }
      break;
  }

  if (newData.length == 0) {
    newData = fullData(dataName, data, size);
  }

  setLatestDatas(dataName, newData);
  return newData;
};

const onlyLastData = (
  dataName: string,
  data: ChartData[],
  size: number
): ChartData[] => {
  let sum = 0;
  let date = new Date(data[data.length - 1].time);
  let minutes = convertMinutes(date.getMinutes());
  let latestData = latestDatas[dataName];
  if (latestData[latestData.length - 1].time.split(":")[1] == minutes) {
    console.log("same minute");
    return latestData;
  }

  for (let i = data.length - size; i < data.length; i++) {
    sum += parseInt(data[i].value);
  }
  let avg = sum / size;

  let newPoint = {
    time: `${date.getHours()}:${minutes}`,
    value: avg.toString(),
  };
  latestData.push(newPoint);
  latestData = latestData.slice(1, latestData.length);
  return latestData;
};

const fullData = (
  dataName: string,
  data: ChartData[],
  size: number
): ChartData[] => {
  let sum = 0;
  let newData = [];
  for (let i = 0; i < data.length; i++) {
    sum += parseInt(data[i].value);
    let date = new Date(data[i].time);
    if (i % size == size - 1 && i != 0) {
      let avg = sum / size;
      let minutes = convertMinutes(date.getMinutes());
      let newPoint = {
        time: `${date.getHours()}:${minutes}`,
        value: avg.toString(),
      };
      newData.push(newPoint);
      sum = 0;
    }
  }
  return newData;
};

const setLatestDatas = (dataName: string, newData: ChartData[]) => {
  switch (dataName) {
    case "cpu_busy":
      latestDatas.cpu_busy = newData;
      break;
    case "memory_used":
      latestDatas.memory_used = newData;
      break;
    case "disk_io_util":
      latestDatas.disk_io_util = newData;
      break;
  }
};
const convertMinutes = (minutes: number) => {
  let convertedMinute;
  if (minutes < 10) {
    convertedMinute = "0" + minutes.toString();
  } else {
    convertedMinute = minutes.toString();
  }
  return convertedMinute;
};
</script>

<style scoped>
.graph-card-title {
  margin-left: 1.25em;
  margin-top: 1em;
  color: white;
  font-weight: bold;
}

.row {
  display: flex;
  padding: 0.25vw;
}

.row-element {
  width: 50%;
}

.row-element-right {
  color: #006fff;
}

.wrapper {
  background-color: #efefef;
  border-radius: 7px;
  box-shadow: 0 2px 2px 2px rgba(0, 0, 0, 0.29);
  padding: 0.25vw 0 0.25vw 0.5vw;
}
</style>
