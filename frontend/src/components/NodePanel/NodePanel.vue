<template>
  <div id="node-panel-container">
    <Tabs :nodePanelOpen="nodePanelOpen" :node="selectedNode" />
  </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, watch, defineProps } from "vue";
import Tabs from "@/components/NodePanel/Tabs.vue";
// vue data
const props = defineProps(["selectedNode", "closePanel"]);
const emit = defineEmits(["updatePanelWidth", "updatePanelRight"]);

// data
const nodePanelRightPercent = ref(-50);
const nodePanelOpen = ref(false);
//methods
watch(nodePanelRightPercent, () => {
  emit("updatePanelRight", nodePanelRightPercent.value);
});
watch(props, () => {
  if (props.selectedNode && props.selectedNode.show) {
    nodePanelRightPercent.value = 0;
    nodePanelOpen.value = true;
  } else if (props.selectedNode && !props.selectedNode.show) {
    nodePanelRightPercent.value = -50;
    nodePanelOpen.value = false;
  }

  if (props.closePanel) {
    console.log("now close panel");
    nodePanelRightPercent.value = -50;
    nodePanelOpen.value = false;
  }
});
</script>

<style scoped>
#node-panel-container {
  position: absolute;
  top: 0;
  right: v-bind(nodePanelRightPercent + "%");
  height: 100vh;
  background-color: #393b54;
  width: 50%;
  z-index: 10;
  transition: right 1500ms;
}
</style>
