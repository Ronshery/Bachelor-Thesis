<template>
  <div class="container">
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
    />
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
  reactive,
  watch,
  watchEffect,
} from "vue";
import * as vNG from "v-network-graph";
import { useStore } from "vuex";

// vue data
const props = defineProps(["nodes", "configs", "layers"]);
const emit = defineEmits(["nodeClicked"]);
const store = useStore();

// data
let zoomLevel = ref(1);
const selectedNodes = ref<string[]>([]);
const graph = ref<vNG.Instance>();
const layouts = ref<vNG.Layouts>();
const layoutsBackup = ref<vNG.Layouts>();
let layoutsBackupSet = false;

// methods
onMounted(() => {
  store.dispatch("initializeGraph", graph);
  graph.value?.panToCenter();
  graph.value?.fitToContents();
  zoomLevel.value = 0.5;
});

const reset = async () => {
  console.log(zoomLevel.value);
  zoomLevel.value = 0.1;
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
    graph.value?.panToCenter();
    graph.value?.fitToContents();
  });
};

const eventHandlers: vNG.EventHandlers = {
  "node:click": ({ node }) => {
    emit("nodeClicked", node);
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
};
</script>
<style scoped>
.container {
  background-color: #27293d;
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
