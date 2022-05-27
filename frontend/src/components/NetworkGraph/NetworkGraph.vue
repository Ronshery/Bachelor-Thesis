<template>
  <div class="v-network-graph-container">
    <div class="graph-panel">
      <button @click="graph?.zoomIn()">Zoom In</button>
      <button @click="graph?.zoomOut()">Zoom Out</button>
      <button @click="graph?.fitToContents()">Fit</button>
      <button @click="graph?.panToCenter()">Center</button>
      <button @click="reset">Reset</button>
      {{ selectedNodes }}
      <br />
      {{ layouts }}
      <br />
      {{ layoutsBackup }}
    </div>
    <v-network-graph
      ref="graph"
      v-model:selected-nodes="selectedNodes"
      v-model:zoom-level="zoomLevel"
      :nodes="nodes"
      :configs="configs"
      :event-handlers="eventHandlers"
      :layers="layers"
      v-model:layouts="layouts"
    >
      <template #badge="{}">
        <circle
          v-for="(pos, node) in layoutsComputed.nodes"
          :key="node"
          :r="radius"
          :cx="pos.x"
          :cy="pos.y"
          :stroke-dasharray="0"
          :stroke-dashoffset="0"
          stroke="lightgray"
          fill="none"
          stroke-width="15"
          style="pointer-events: none"
        />
        <circle
          class="circle"
          v-for="(pos, node) in layoutsComputed.nodes"
          :key="node"
          :r="radius"
          :cx="pos.x"
          :cy="pos.y"
          :stroke-dasharray="strokeDashArray(pos.bmScore)"
          :stroke-dashoffset="percentToScore(25)"
          stroke="palevioletred"
          fill="none"
          stroke-width="15"
          style="pointer-events: none"
        />
        <text
          v-for="(pos, node) in layoutsComputed.nodes"
          :key="node"
          :x="pos.x"
          :y="pos.y"
          text-anchor="middle"
          alignment-baseline="central"
          style="pointer-events: none"
        >
          {{ pos.bmScore }}/{{ maxValue }}
        </text>
      </template>
    </v-network-graph>
  </div>
</template>

<script setup lang="ts">
import {
  ref,
  nextTick,
  defineEmits,
  defineProps,
  onMounted,
  computed,
  watch,
} from "vue";
import * as vNG from "v-network-graph";
import { useStore } from "vuex";
import { VNetworkGraph } from "v-network-graph";

// interfaces
interface Layouts extends vNG.Layouts {
  nodes: {
    [x: string]: {
      fixed?: boolean | undefined;
      x: number;
      y: number;
      bmScore: number;
    };
  };
}

// vue data
const props = defineProps([
  "nodes",
  "configs",
  "layers",
  "nodePanel",
  "networkGraphRight",
]);
const emit = defineEmits(["nodeClicked", "closePanel"]);
const store = useStore();

// data
let zoomLevel = ref(1);
const selectedNodes = ref<string[]>([]);
const graph = ref<vNG.Instance>();
const layouts = ref<Layouts>({ nodes: {} });
const layoutsBackup = ref<vNG.Layouts>();
let layoutsBackupSet = false;
let data = ref([1, 9, 5, 6]);
const layoutsComputed = computed(() => {
  const keys = Object.keys(layouts.value.nodes);
  Object.entries(layouts.value.nodes).forEach((node, index) => {
    layouts.value.nodes[keys[index]].bmScore = props.nodes[node[0]].bmScore;
  });
  return layouts.value;
});
const loadedView = ref(false);
// methods
let setTabContentHeight = () => {
  const tabContentContainerList = document.getElementsByClassName(
    "tab-content-container"
  );
  const nodePanelContainer = document.getElementById("node-panel-container");
  for (let i = 0; i <= tabContentContainerList.length; i++) {
    if (nodePanelContainer && tabContentContainerList[i]) {
      tabContentContainerList[i].style.height = `${
        nodePanelContainer.clientHeight - 50
      }px`;
    }
  }
};

onMounted(() => {
  console.log("NetworkGraph mounted");
  store.dispatch("initializeGraph", graph);
  nextTick(() => {
    graphCenterAndFit();
  });
  window.addEventListener("resize", () => {
    graphCenterAndFit();
    setTabContentHeight();
    console.log(window.innerWidth);
    if (window.innerWidth < 1230) {
      emit("closePanel", true);
    } else {
      emit("closePanel", false);
    }
  });
});

watch(props, () => {
  if (props.networkGraphRight == 0) {
    // NodePanel is open
    setGraphWrapperWidth(25);
  } else if (props.networkGraphRight != 0) {
    // NodePanel is closed
    setGraphWrapperWidth(100);
  }
});

const setGraphWrapperWidth = (widthValue: number) => {
  const graphWrapperElement = document.getElementById("graph-wrapper");
  if (graphWrapperElement != null) {
    graphWrapperElement.style.width = `${widthValue}%`;

    const intervalID = setInterval(() => {
      graphCenterAndFit();
    });
    setTimeout(() => {
      clearInterval(intervalID);
    }, 1500);
  }
};

const graphCenterAndFit = () => {
  graph.value?.panToCenter();
  graph.value?.fitToContents();
};

const reset = async () => {
  data.value[0] = 7;
  if (layouts.value && layoutsBackupSet && layoutsBackup.value) {
    for (const [key] of Object.entries(layouts.value.nodes)) {
      // assignment without reference
      console.log(layouts.value.nodes[key]);
      console.log(layoutsBackup.value.nodes[key]);
      layouts.value.nodes[key] = JSON.parse(
        JSON.stringify(layoutsBackup.value.nodes[key])
      );
    }
  }
  nextTick().then(() => {
    graphCenterAndFit();
  });
};

const eventHandlers: vNG.EventHandlers = {
  "node:click": ({ node }) => {
    emit("nodeClicked", props.nodes[node]);
  },
  "view:click": () => {
    emit("nodeClicked", null);
  },
  "node:dragstart": () => {
    // set layoutsBackup
    if (!layoutsBackupSet) {
      layoutsBackup.value = JSON.parse(JSON.stringify(layouts.value));
      layoutsBackupSet = true;
    }
  },
  "view:load": () => {
    loadedView.value = true;
  },
};

/// Node DonutChart
// data
const maxValue = 10;
const radius = 50;
const circumference = 2 * radius * Math.PI;
const strokeDashArray = (score: number) => {
  if (loadedView.value) {
    return `${convertedScore(score)} ${circumference - convertedScore(score)}`;
  } else {
    return `0 ${circumference}`;
  }
};
// circumference  === 100%
// x              === 60
// methods
const scoreToPercent = (score: number) => (100 * score) / circumference;
const percentToScore = (percent: number) => (circumference * percent) / 100;
const convertedScore = (score: number) => (score * circumference) / maxValue;
</script>
<style scoped>
.v-network-graph-container {
  background-color: #191824;
  height: 100vh;
  flex-grow: 1;
}

.graph-panel {
  position: absolute;
  display: flex;
  z-index: 10;
  color: white;
}
</style>
