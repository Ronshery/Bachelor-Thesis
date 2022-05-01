<template>
  <div
    ref="tabContentContainer"
    class="tab-content-container"
    v-show="isActive"
  >
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { ref, defineExpose, onMounted } from "vue";

// data
const isActive = ref(false);
const tabContentContainer = ref();
// methods
onMounted(() => {
  const nodePanelContainer = document.getElementById("node-panel-container");
  if (nodePanelContainer && tabContentContainer.value) {
    tabContentContainer.value.style.height = `${
      nodePanelContainer.clientHeight - 50
    }px`;
  }
});

defineExpose({ isActive });
</script>

<style scoped>
.tab-content-container {
  overflow: auto;
  height: 100vh;
}
</style>
