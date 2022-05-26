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
      v-for="graph in graphListApex"
      :key="graph.title"
      :cssStyle="{ backgroundColor: '#4c4f69' }"
      :isSVG="true"
    >
      <template v-slot:title>
        <div class="graph-card-title">{{ graph.title }}</div>
      </template>
      <template v-slot:default>
        <ApexLineChart :series="graph.data" :errorMsg="metricsError" />
      </template>
    </OverviewCard>
  </OverviewLayout>
</template>

<script setup lang="ts">
import { computed, defineProps, ref, watch } from "vue";
import benchmarkService from "@/services/benchmark-service";
import DonutCard from "@/components/NodePanel/tabContents/Overview/DonutCard.vue";
import OverviewCard from "@/components/NodePanel/tabContents/Overview/OverviewCard.vue";
import OverviewLayout from "@/components/NodePanel/tabContents/Overview/OverviewLayout.vue";
import ApexLineChart from "@/components/utils/ApexLineChart.vue";

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

interface ApexDataPoint {
  x: Date;
  y: string;
}

interface ApexData {
  name: string;
  data: ApexDataPoint[];
}

interface GraphList {
  id: string;
  title: string;
  data: ApexData[];
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

const metricsError = ref<string>("");

let graphListApex = ref<GraphList[]>([
  { id: "cpu_busy", title: "CPU busy", data: [] },
  { id: "memory_used", title: "Memory used", data: [] },
  { id: "disk_io_util", title: "Disk IO util", data: [] },
]);

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

watch(props, () => {
  if (props.nodePanelOpen) {
    // fetch full data when clicking on node
    fetchData(nodeComp.value.id);
    setInterval(() => {
      metricsError.value = "";
      fetchData(nodeComp.value.id);
    }, 60000);
  }
});

const dataNameMapper = (dataName: string): string => {
  switch (dataName) {
    case "memory_used":
      return "Memory used";
    case "disk_io_util":
      return "Disk IO util";
    case "cpu_busy":
      return "CPU busy";
  }
  return "";
};

let firstCall = true;
const fetchData = async (nodeID: string) => {
  let timeDelta = 420;
  if (nodeID) {
    benchmarkService
      .get(`/metrics/${nodeID}/${timeDelta}`)
      .then((response) => {
        const responseData: { node_name: string } & {
          [key: string]: ChartData[];
        } = response.data;
        let dataNames = Object.keys(responseData);
        dataNames = dataNames.filter((key) => key != "node_name");
        console.log(dataNames);

        //initialize graphList
        /*        if (firstCall) {
          firstCall = false;
          dataNames.forEach((dataName) => {
            graphListApex.value.push({
              id: dataName,
              title: dataNameMapper(dataName),
              data: [],
            });
          });
        }*/
        dataNames.forEach((dataName) => {
          let data = response.data[dataName];

          for (let i = 0; i < graphListApex.value.length; i++) {
            if (graphListApex.value[i].id == dataName) {
              graphListApex.value[i].data = [
                { name: "value", data: convertDataToApex(data) },
              ];
            }
          }
        });
        console.log(graphListApex);
      })
      .catch((error) => {
        console.log(error);
        metricsError.value = error.response.data.detail;
      });
  }
};

const convertDataToApex = (
  data: { time: string; value: string }[]
): ApexDataPoint[] => {
  let newData: ApexDataPoint[] = [];
  for (let i = 0; i < data.length; i++) {
    let date = new Date(data[i].time);
    let point = {
      x: date,
      y: Number(data[i].value).toFixed(2),
    };
    newData.push(point);
  }
  return newData;
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
