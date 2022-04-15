<template>
  <div id="node-panel-container">
    <Tabs :nodePanelOpen="nodePanelOpen" :node="selectedNode" />
    <!--
    {{ props.selectedNode }}
-->
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, watch } from "vue";
import { useStore } from "vuex";
import Tabs from "@/components/NodePanel/Tabs.vue";

// vue data
const props = defineProps(["selectedNode"]);
const store = useStore();

// data
const nodePanelOpen = ref(false);

// methods
watch(props, () => {
  const nodePanelContainer = document.getElementById("node-panel-container");
  if (nodePanelContainer != null) {
    if (props.selectedNode) {
      nodePanelContainer.style.width = "70%";
      positionGraph();
      nodePanelOpen.value = true;
    } else if (props.selectedNode == null) {
      nodePanelOpen.value = false;
      nodePanelContainer.style.width = "0";
      positionGraph();
    }
  }
});

const positionGraph = () => {
  if (nodePanelOpen.value) {
    return 0;
  }
  const graph = store.getters["graph"];
  const intervalID = setInterval(() => {
    graph.panToCenter();
    graph.fitToContents();
  });
  setTimeout(() => {
    clearInterval(intervalID);
  }, 1500);
};
</script>

<style scoped>
#node-panel-container {
  background-color: #6753e1;
  transition: width 1500ms;
  width: 0;
  z-index: 10;
}
</style>
