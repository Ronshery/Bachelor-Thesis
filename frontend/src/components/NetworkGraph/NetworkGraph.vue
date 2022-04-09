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
      {{ layoutsData }}
      <br />
      {{ layoutsBackup }}
    </div>
    <v-network-graph
      ref="graph"
      v-model:selected-nodes="selectedNodes"
      v-model:zoom-level="zoomLevel"
      :nodes="nodes"
      :edges="edges"
      :configs="configs"
      v-model:layouts="layoutsData"
      :event-handlers="eventHandlers"
      :layers="layers"
    >
      <!-- Additional layer -->
      <template #badge="{ scale }">
        <!--
          If the `view.scalingObjects` config is `false`(default),
          scaling does not change the display size of the nodes/edges.
          The `scale` is passed as a scaling factor to implement
          this behavior. -->
        <circle
          v-for="(pos, node) in layoutsData.nodes"
          :key="node"
          :cx="pos.x * scale"
          :cy="pos.y * scale"
          :r="4 * scale"
          :fill="nodes[node].active ? '#00cc00' : '#ff5555'"
          style="pointer-events: none"
        />
      </template>
    </v-network-graph>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, defineEmits, defineProps, onMounted } from "vue";
import * as vNG from "v-network-graph";
import { useStore } from "vuex";

// vue data
const props = defineProps(["nodes", "edges", "configs", "layouts", "layers"]);
const emit = defineEmits(["nodeClicked"]);
const store = useStore();

// data
let zoomLevel = ref(1);
const selectedNodes = ref<string[]>([]);
const layoutsData = ref(props.layouts);
const graph = ref<vNG.Instance>();
const layoutsBackup = JSON.parse(JSON.stringify(props.layouts));

// methods
onMounted(() => {
  console.log(store.state);
});

const reset = async () => {
  zoomLevel.value = 1;
  for (const [key, value] of Object.entries(layoutsData.value.nodes)) {
    // assignment without reference
    layoutsData.value.nodes[key] = JSON.parse(
      JSON.stringify(layoutsBackup)
    ).nodes[key];
  }
  nextTick().then(() => {
    graph.value?.panToCenter();
    graph.value?.fitToContents();
  });
};

const eventHandlers: vNG.EventHandlers = {
  "node:click": ({ node }) => {
    console.log(node);
    console.log(props);
    emit("nodeClicked", node);
  },
  "view:click": () => {
    emit("nodeClicked", null);
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
