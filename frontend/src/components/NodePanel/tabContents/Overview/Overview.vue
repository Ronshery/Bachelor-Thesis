<template>
  <TabLayout>
    <OverviewLayout>
      <TabContentCard>
        <template v-slot:title>Score</template>
        <DonutCard
          :segments="segmentsComp"
          :score="nodeComp.bmScore"
          :nodeScore="nodeScore"
        />
      </TabContentCard>
      <TabContentCard>
        <template v-slot:title> Characteristic </template>
        <CharacteristicCard :nodeScore="nodeScore" />
      </TabContentCard>
      <TabContentCardsWrapper>
        <TabContentCard>
          <template v-slot:title> Node info </template>
          <template v-slot:default>
            <InnerTableCard
              :list-as-object="nodeInfoComp"
              :mappings="mappings"
            />
          </template>
        </TabContentCard>
        <TabContentCard
          v-for="graph in graphListApex"
          :key="graph.title"
          :cssStyle="{ backgroundColor: '#4c4f69', minHeight: '400px' }"
          :isSVG="true"
        >
          <template v-slot:title>
            <div class="graph-card-title">{{ graph.title }}</div>
          </template>
          <template v-slot:default>
            <ApexLineChart :series="graph.data" :errorMsg="metricsError" />
          </template>
        </TabContentCard>
      </TabContentCardsWrapper>
    </OverviewLayout>
  </TabLayout>
</template>

<script setup lang="ts">
import { computed, defineProps, ref, watch } from "vue";
import benchmarkService from "@/services/benchmark-service";
import DonutCard from "@/components/NodePanel/tabContents/Overview/DonutCard.vue";
import OverviewLayout from "@/components/NodePanel/tabContents/Overview/OverviewLayout.vue";
import ApexLineChart from "@/components/utils/ApexLineChart.vue";
import TabLayout from "@/components/NodePanel/tabContents/TabLayout.vue";
import TabContentCard from "@/components/NodePanel/tabContents/TabContentCard.vue";
import TabContentCardsWrapper from "@/components/NodePanel/tabContents/TabContentCardsWrapper.vue";
import InnerTableCard from "@/components/NodePanel/tabContents/InnerTableCard.vue";
import CharacteristicCard from "@/components/NodePanel/tabContents/Overview/CharacteristicCard.vue";
import Node from "@/models/Node";
import bmUtils, {
  BmType,
} from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";

interface Segment {
  benchmark: string;
  score: number;
  color: string;
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
const mappings = {
  architecture: "architecture",
  operatingSystem: "operating system",
  osImage: "OS image",
  kernelVersion: "kernel version",
  cpu: "cpu cores",
  memory: "memory",
  ephemeralStorage: "ephemeral storage",
  pods: "max pods",
};

const nodeComp = computed(() => {
  if (props.node == null) {
    return {
      bmScore: 0,
      metrics: { cpu_busy: [], memory_used: [] },
      status: undefined,
    };
  } else {
    if (props.node.name) {
      Node.dispatch("fetchScore", props.node);
    }
    return props.node;
  }
});

const metricsError = ref<string>("");

let graphListApex = ref<GraphList[]>([
  { id: "cpu_busy", title: "CPU busy", data: [] },
  { id: "memory_used", title: "Memory used", data: [] },
  { id: "disk_io_util", title: "Disk IO util", data: [] },
]);
interface DetailScore {
  max_score: number;
  min_score: number;
  score: number;
}
let segments = ref<Segment[]>([
  {
    benchmark: BmType.CPU_SYSBENCH,
    score: 0,
    color: "#E3E0FF",
  },
  {
    benchmark: BmType.MEMORY_SYSBENCH,
    score: 0,
    color: "#CECAFF",
  },
  {
    benchmark: BmType.DISK_IOPING,
    score: 0,
    color: "#AEA7FF",
  },
  {
    benchmark: BmType.DISK_FIO,
    score: 0,
    color: "#7D72FF",
  },
  {
    benchmark: BmType.NETWORK_IPERF3,
    score: 0,
    color: "#5245EA",
  },
  {
    benchmark: BmType.NETWORK_QPERF,
    score: 0,
    color: "#352BA9",
  },
]);

const segmentsComp = computed(() => {
  if (nodeScore.value != null) {
    const details = nodeScore.value["details"];
    for (const key in details) {
      const segment: Segment = {
        benchmark: key.toLowerCase().replace("_", "-"),
        score: details[key].score,
        color: bmUtils.bmTypecolorMapping(key as BmType),
      };
      updateSegmentsBackup(segment);
    }
  }
  return segments.value;
});

const updateSegmentsBackup = (updatedSegment: Segment) => {
  for (let i = 0; i < segments.value.length; i++) {
    if (segments.value[i].benchmark == updatedSegment.benchmark) {
      segments.value[i].score = updatedSegment.score;
    }
  }
};

// methods
const nodeScore = computed(() => {
  if (nodeComp.value != null) {
    return Node.find(nodeComp.value.id)?.$getAttributes().scores;
  }
  return null;
});
const nodeInfoComp = computed(() => {
  let kubeNodeInfo = nodeComp.value.status;
  let info: Record<string, string> = {};
  if (kubeNodeInfo) {
    info = {
      architecture: kubeNodeInfo.nodeInfo.architecture,
      operatingSystem: kubeNodeInfo.nodeInfo.operatingSystem,
      osImage: kubeNodeInfo.nodeInfo.osImage,
      kernelVersion: kubeNodeInfo.nodeInfo.kernelVersion,
      cpu: kubeNodeInfo.allocatable.cpu,
      memory: kubeNodeInfo.allocatable.memory,
      ephemeralStorage: kubeNodeInfo.allocatable["ephemeral-storage"],
      pods: kubeNodeInfo.allocatable.pods,
    };
  }
  return info;
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
  let timeDelta = -1;
  if (nodeID) {
    benchmarkService
      .get(`/metrics/${nodeID}/${timeDelta}`)
      .then((response) => {
        const responseData: { node_name: string } & {
          [key: string]: ChartData[];
        } = response.data;
        let dataNames = Object.keys(responseData);
        dataNames = dataNames.filter((key) => key != "node_name");

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
</style>
