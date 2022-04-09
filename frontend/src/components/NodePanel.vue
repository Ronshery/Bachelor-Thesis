<template>
  <div id="node-panel-container">{{ props.node }}</div>
</template>

<script setup lang="ts">
import { defineProps, nextTick, watch } from "vue";

const props = defineProps(["node", "graph"]);

watch(props, () => {
  const nodePanelContainer = document.getElementById("node-panel-container");
  if (nodePanelContainer != null) {
    if (props.node) {
      nodePanelContainer.style.width = "70%";
    } else if (props.node == null) {
      nodePanelContainer.style.width = "0";
    }
  }
});
</script>

<style scoped>
#node-panel-container {
  background-color: yellow;
  transition: width 1500ms;
  width: 0;
}
</style>
