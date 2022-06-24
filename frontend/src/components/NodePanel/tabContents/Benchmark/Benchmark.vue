<template>
  <TabLayout>
    <div class="benchmark-tool-box">
      <span
        class="run-wrapper tooltip"
        style="margin-left: unset"
        :class="{
          'run-disabled': runAllState || runAllClicked,
        }"
      >
        <ToolTip> runs only non-active benchmarks </ToolTip>
        <span
          v-if="!runAllState && !runAllClicked"
          :class="{ 'cursor-pointer': !runAllState }"
          @click="runAllBenchmarks()"
        >
          <img
            class="run-icon"
            alt="run"
            :src="require('@/assets/benchmark/benchmark-run-icon.svg')"
          />
          <span :class="{ 'run-text': !runAllState && !runAllClicked }">
            run all
          </span>
        </span>
        <span v-else>
          <img
            class="run-icon"
            alt="run"
            :src="require('@/assets/benchmark/benchmark-run-icon.svg')"
          /><span>run all</span>
        </span>
      </span>
    </div>
    <div class="menu-wrapper">
      <Menu :items="menuItems" @itemClicked="itemClicked" :id="props.node.id" />
    </div>
    <BenchmarkChapter
      v-for="(bm, key) in availableBenchmarks"
      :key="key"
      :benchmark="key"
    >
      <div v-if="key === BmResource.CPU">
        <BenchmarkTypeCards
          :bmTypes="bm"
          :nodeID="props.node.name"
          :runningState="runningState"
        />
      </div>
      <div v-if="key === BmResource.NETWORK">
        <BenchmarkTypeCards
          :bmTypes="bm"
          :nodeID="props.node.name"
          :runningState="runningState"
        />
      </div>
      <div v-if="key === BmResource.MEMORY">
        <BenchmarkTypeCards
          :bmTypes="bm"
          :nodeID="props.node.name"
          :runningState="runningState"
        />
      </div>
      <div v-if="key === BmResource.DISK">
        <BenchmarkTypeCards
          :bmTypes="bm"
          :nodeID="props.node.name"
          :runningState="runningState"
        />
      </div>
    </BenchmarkChapter>
  </TabLayout>
</template>

<script setup lang="ts">
import { computed, defineProps, ref, watch } from "vue";
import TabLayout from "@/components/NodePanel/tabContents/TabLayout.vue";
import Menu from "@/components/utils/Menu.vue";
import BenchmarkChapter from "@/components/NodePanel/tabContents/Benchmark/BenchmarkChapter.vue";
import BenchmarkTypeCards from "@/components/NodePanel/tabContents/Benchmark/benchmarkTypes/BenchmarkTypeCards.vue";
import bmScript, {
  BmResource,
  BmType,
} from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";
import Node from "@/models/Node";
import Benchmark from "@/models/Benchmark";
import bmUtils from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";
import ToolTip from "@/components/utils/ToolTip.vue";

// vue data
const props = defineProps([
  "node",
  "nodePanelOpen",
  "availableBenchmarks",
  "runningState",
]);

// data
const runAllClickedList = ref<{ [key: string]: boolean }>({});
const runAllClicked = computed(() => runAllClickedList.value[props.node.id]);

// methods
const menuItems = computed(() => {
  let list = Object.keys(props.availableBenchmarks);
  for (let i = 0; i < list.length; i++) {
    list[i] = bmScript.benchmarkNameMapper(list[i] as BmResource);
  }
  return list;
});

const itemClicked = (param: BmResource) => {
  let chapterID = param.toLowerCase().split(" ")[0] + "-chapter";
  const chapterElement = document.getElementById(chapterID);
  if (chapterElement) {
    chapterElement.scrollIntoView({ behavior: "smooth", block: "start" });
  }
};

const runAllBenchmarks = () => {
  updateRunAllClicked(true);
  let index = 1;
  for (const benchmarkType in props.runningState) {
    if (!props.runningState[benchmarkType]) {
      let nodeParam = props.node.id;

      if (bmUtils.isNetworkBenchmark(benchmarkType as BmType)) {
        const allNodes = Node.all();
        const randomServerNodeIndex = Math.floor(
          Math.random() * allNodes.length
        );
        nodeParam =
          props.node.id +
          "@@@" +
          allNodes[randomServerNodeIndex].$getAttributes().id;
      }

      // in an effort not to overload the server
      setTimeout(() => {
        Benchmark.dispatch("runBenchmark", {
          benchmarkType: benchmarkType as BmType,
          nodeID: nodeParam,
        });
      }, 5000 * index);
      index++;
    }
  }
};

const runAllState = computed(() => {
  for (let isRunning of Object.values(props.runningState)) {
    if (!isRunning) {
      return false;
    }
  }
  updateRunAllClicked(false);
  return true;
});

const updateRunAllClicked = (newVal: boolean) => {
  runAllClickedList.value[props.node.id] = newVal;
};

watch(props, () => {
  if (!runAllClickedList.value[props.node.id]) {
    runAllClickedList.value[props.node.id] = false;
  }
});
</script>

<style scoped>
.menu-wrapper {
  position: absolute;
  right: 2em;
  top: 3.25em;
  z-index: 13;
}

.benchmark-tool-box {
  margin-bottom: 1em;
}
</style>
