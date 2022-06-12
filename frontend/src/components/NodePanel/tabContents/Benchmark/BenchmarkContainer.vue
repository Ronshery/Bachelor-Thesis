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
import bmUtils, {
  BmResource,
  BmType,
} from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";
import { IBenchmark } from "@/models/IBenchmark";

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

let fetchingActiveList = ref<NodeFetchingState>({});
const runningState = computed(() => {
  const bmTypes = [
    BmType.CPU_SYSBENCH,
    BmType.MEMORY_SYSBENCH,
    BmType.DISK_IOPING,
    BmType.DISK_FIO,
    BmType.NETWORK_IPERF3,
    BmType.NETWORK_QPERF,
  ];

  const runningStateNew = {
    [BmType.CPU_SYSBENCH]: false,
    [BmType.MEMORY_SYSBENCH]: false,
    [BmType.DISK_IOPING]: false,
    [BmType.DISK_FIO]: false,
    [BmType.NETWORK_IPERF3]: false,
    [BmType.NETWORK_QPERF]: false,
  };
  for (let bmType of bmTypes) {
    const query = Benchmark.query().where("node", props.node.id);
    const runningBmsByType = query
      .where((benchmark: IBenchmark) => {
        return benchmark.id.includes(bmType);
      })
      .where("metrics", null)
      .get();
    runningStateNew[bmType] = runningBmsByType.length > 0;
  }

  initFetchingActiveList();
  for (const [bmType, isRunning] of Object.entries(runningStateNew)) {
    if (isRunning) {
      console.log(`fetch results of: ${bmType} in node: ${props.node.id}`);
      const query = Benchmark.query().where("node", props.node.id);
      const runningBm = query
        .where((benchmark: IBenchmark) => {
          return benchmark.id.includes(bmType);
        })
        .where("metrics", null)
        .get();
      fetchResults(runningBm[0], bmType as BmType);
    } else {
      resetFetchingActiveList(bmType as BmType);
    }
  }

  return runningStateNew;
});

const fetchResults = (benchmark: Benchmark, bmType: BmType) => {
  const spec = benchmark.$getAttributes().spec;
  if (
    !fetchingActiveList.value[props.node.name][bmType].isFetching &&
    fetchingActiveList.value[props.node.name][bmType].intervalID == undefined
  ) {
    // there is no fetching active do it now
    fetchingActiveList.value[props.node.name][bmType].isFetching = true;
    let bmDuration = parseInt(bmUtils.getBMDuration(spec.spec.options)) * 1000;
    if (bmDuration == 1000) {
      bmDuration = 30000;
    }
    setTimeout(() => {
      fetchingActiveList.value[props.node.name][bmType].intervalID =
        setInterval(() => {
          Benchmark.dispatch("fetchBenchmarkById", benchmark);
        }, 1000);
    }, bmDuration);
  } else {
    console.log(
      "old fetch - intervalID: " +
        fetchingActiveList.value[props.node.name][bmType].intervalID
    );
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
const resetFetchingActiveList = (bmType: BmType) => {
  if (props.node.name != undefined) {
    fetchingActiveList.value[props.node.name][bmType].isFetching = false;
    clearInterval(fetchingActiveList.value[props.node.name][bmType].intervalID);
    fetchingActiveList.value[props.node.name][bmType].intervalID = undefined;
  }
};
</script>

<style scoped></style>
