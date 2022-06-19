<template>
  <BenchmarkComponent
    :node="node"
    :availableBenchmarks="availableBenchmarks"
    :runningState="runningState"
  />
</template>

<script setup lang="ts">
import { computed, defineProps, ref, watch } from "vue";
import BenchmarkComponent from "@/components/NodePanel/tabContents/Benchmark/Benchmark.vue";
import Benchmark from "@/models/Benchmark";
import {
  BmResource,
  BmType,
} from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";
import { IBenchmark } from "@/models/IBenchmark";
import Node from "@/models/Node";

interface availableBMs {
  cpu?: BmType[];
  memory?: BmType[];
  disk?: BmType[];
  network?: BmType[];
}

// vue data
const props = defineProps(["node", "nodePanelOpen"]);

// data
const availableBenchmarks: availableBMs = {
  [BmResource.CPU]: [BmType.CPU_SYSBENCH],
  [BmResource.MEMORY]: [BmType.MEMORY_SYSBENCH],
  [BmResource.DISK]: [BmType.DISK_IOPING, BmType.DISK_FIO],
  [BmResource.NETWORK]: [BmType.NETWORK_IPERF3, BmType.NETWORK_QPERF],
};

// methods
let lastNode = 0;
watch(props, () => {
  if (props.node.id) {
    if (lastNode != props.node.id || lastNode == 0) {
      lastNode = props.node.id;
      console.log("fetch benchmarks");
      Benchmark.dispatch("fetchBenchmarksByNode", {
        nodeID: props.node.id,
      });
    }
  }
});

interface FetchingState {
  [key: string]: { isFetching: boolean; intervalID: undefined | number };
}

interface NodeFetchingState {
  [key: string]: FetchingState;
}

interface RunningState {
  [key: string]: {
    [BmType.CPU_SYSBENCH]: boolean;
    [BmType.MEMORY_SYSBENCH]: boolean;
    [BmType.DISK_IOPING]: boolean;
    [BmType.DISK_FIO]: boolean;
    [BmType.NETWORK_IPERF3]: boolean;
    [BmType.NETWORK_QPERF]: boolean;
  };
}

let runningStateList = ref<RunningState>({});
let fetchingActiveList = ref<NodeFetchingState>({});
const runningState = computed(() => {
  if (props.node.name == undefined) {
    return {
      [BmType.CPU_SYSBENCH]: false,
      [BmType.MEMORY_SYSBENCH]: false,
      [BmType.DISK_IOPING]: false,
      [BmType.DISK_FIO]: false,
      [BmType.NETWORK_IPERF3]: false,
      [BmType.NETWORK_QPERF]: false,
    };
  }

  const bmTypes = [
    BmType.CPU_SYSBENCH,
    BmType.MEMORY_SYSBENCH,
    BmType.DISK_IOPING,
    BmType.DISK_FIO,
    BmType.NETWORK_IPERF3,
    BmType.NETWORK_QPERF,
  ];

  initRunningState();
  for (const node in runningStateList.value) {
    for (let bmType of bmTypes) {
      const query = Benchmark.query().where("node", node);
      const runningBmsByType = query
        .where((benchmark: IBenchmark) => {
          return benchmark.id.includes(bmType);
        })
        .where("metrics", null)
        .get();
      updateRunningStateByNode(
        bmType as BmType,
        runningBmsByType.length > 0,
        node
      );
    }
  }

  return runningStateList.value[props.node.name];
});

watch(runningStateList.value, () => {
  initFetchingActiveList();
  for (const [node, nodeRunningState] of Object.entries(
    runningStateList.value
  )) {
    for (const [bmType, isRunning] of Object.entries(nodeRunningState)) {
      if (isRunning) {
        console.log(`fetch results of: ${bmType} in node: ${node}`);
        const query = Benchmark.query().where("node", node);
        const runningBm = query
          .where((benchmark: IBenchmark) => {
            return benchmark.id.includes(bmType);
          })
          .where("metrics", null)
          .get();
        fetchResultsByNode(runningBm[0], bmType as BmType, node);
      } else {
        // helps to clear interval in fetchResultsByNode()
        resetIsFetchingByNode(bmType as BmType, node);
      }
    }
  }
});

const fetchResultsByNode = (
  benchmark: Benchmark,
  bmType: BmType,
  nodeName: string
) => {
  if (
    !fetchingActiveList.value[nodeName][bmType].isFetching &&
    fetchingActiveList.value[nodeName][bmType].intervalID == undefined
  ) {
    // there is no fetching active do it now
    fetchingActiveList.value[nodeName][bmType].isFetching = true;
    /*
    // not usable yet, because after page reload it is counted from the beginning
    const spec = benchmark.$getAttributes().spec;
    let bmDuration = parseInt(bmUtils.getBMDuration(spec.spec.options)) * 1000;
    if (bmDuration == 1000) {
      bmDuration = 30000;
    }*/
    const bmDuration = 5000;
    setTimeout(() => {
      fetchingActiveList.value[nodeName][bmType].intervalID = setInterval(
        () => {
          // needs .toString() to avoid call by reference
          const tmp =
            fetchingActiveList.value[nodeName][bmType].intervalID?.toString();
          if (!fetchingActiveList.value[nodeName][bmType].isFetching) {
            resetIntervalIDByNode(bmType, nodeName, parseInt(tmp ? tmp : ""));
            Node.dispatch("fetchScore", props.node);
          } else {
            Benchmark.dispatch("fetchBenchmarkById", benchmark);
          }
        },
        1000
      );
    }, bmDuration);
  } else {
    console.log(
      "old fetch - intervalID: " +
        fetchingActiveList.value[nodeName][bmType].intervalID
    );
  }
};
const updateRunningStateByNode = (
  bmType: BmType,
  isRunning: boolean,
  nodeName: string
) => {
  runningStateList.value[nodeName][bmType] = isRunning;
};

const initRunningState = () => {
  if (
    props.node.name != undefined &&
    runningStateList.value[props.node.name] == undefined
  ) {
    runningStateList.value[props.node.name] = {
      [BmType.CPU_SYSBENCH]: false,
      [BmType.MEMORY_SYSBENCH]: false,
      [BmType.DISK_IOPING]: false,
      [BmType.DISK_FIO]: false,
      [BmType.NETWORK_IPERF3]: false,
      [BmType.NETWORK_QPERF]: false,
    };
  }
};

const initFetchingActiveList = () => {
  if (
    props.node.name != undefined &&
    fetchingActiveList.value[props.node.name] == undefined
  ) {
    fetchingActiveList.value[props.node.name] = {
      [BmType.CPU_SYSBENCH]: {
        isFetching: false,
        intervalID: undefined,
      },
      [BmType.MEMORY_SYSBENCH]: {
        isFetching: false,
        intervalID: undefined,
      },
      [BmType.DISK_IOPING]: {
        isFetching: false,
        intervalID: undefined,
      },
      [BmType.DISK_FIO]: {
        isFetching: false,
        intervalID: undefined,
      },
      [BmType.NETWORK_IPERF3]: {
        isFetching: false,
        intervalID: undefined,
      },
      [BmType.NETWORK_QPERF]: {
        isFetching: false,
        intervalID: undefined,
      },
    };
  }
};
const resetIntervalIDByNode = (
  bmType: BmType,
  nodeName: string,
  intervalID: number
) => {
  if (props.node.name != undefined) {
    fetchingActiveList.value[nodeName][bmType].isFetching = false;
    clearInterval(intervalID);
    fetchingActiveList.value[nodeName][bmType].intervalID = undefined;
  }
};

const resetIsFetchingByNode = (bmType: BmType, nodeName: string) => {
  if (props.node.name != undefined) {
    fetchingActiveList.value[nodeName][bmType].isFetching = false;
  }
};
</script>

<style scoped></style>
