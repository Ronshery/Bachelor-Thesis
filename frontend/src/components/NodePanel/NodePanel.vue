<template>
  <div id="node-panel-container">
    <Tabs :nodePanelOpen="nodePanelOpen" :node="nodeComp" />
  </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, watch, defineProps, computed } from "vue";
import Tabs from "@/components/NodePanel/Tabs.vue";
// vue data
const props = defineProps(["selectedNode", "closePanel"]);
const emit = defineEmits(["updatePanelWidth", "updatePanelRight"]);

// data
const nodePanelRightPercent = ref(-75);
const nodePanelOpen = ref(false);
const nodeComp = computed(() => {
  if (props.selectedNode == null) {
    return {
      score: 0,
      metrics: { cpu_busy: [], memory_used: [] },
      status: undefined,
    };
  } else {
    return props.selectedNode;
  }
});
//methods
watch(nodePanelRightPercent, () => {
  emit("updatePanelRight", nodePanelRightPercent.value);
});
watch(props, () => {
  if (props.selectedNode && props.selectedNode.show) {
    nodePanelRightPercent.value = 0;
    nodePanelOpen.value = true;
  } else if (props.selectedNode && !props.selectedNode.show) {
    nodePanelRightPercent.value = -75;
    nodePanelOpen.value = false;
  }

  if (props.closePanel) {
    console.log("now close panel");
    nodePanelRightPercent.value = -75;
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
  width: 75%;
  z-index: 10;
  transition: right 1500ms;
}
</style>
