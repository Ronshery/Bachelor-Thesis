<template>
  <div ref="nodePanelContainer" id="node-panel-container">
    <Tabs
      :nodePanelOpen="nodePanelOpen"
      :node="selectedNode"
      :nodePanelAnimationDone="nodePanelAnimationDone"
    />
    <!--
    {{ props.selectedNode }}
-->
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, watch, onMounted } from "vue";
import { useStore } from "vuex";
import Tabs from "@/components/NodePanel/Tabs.vue";

// vue data
const props = defineProps(["selectedNode"]);
const store = useStore();

// data
const nodePanelOpen = ref(false);
const nodePanelAnimationDone = ref(false);
const nodePanelContainer = ref();
let nodePanelWidth = ref();
let nodePanelHeight = ref();
// methods
let resizeStarted = false;
onMounted(() => {
  window.addEventListener("resize", () => {
    if (resizeStarted) {
      const intervalID = setInterval(() => {
        setTabContentWidth();
      });
      setTimeout(() => {
        clearInterval(intervalID);
      }, 1500);
    }

    resizeStarted = true;
  });
});
watch(props, () => {
  if (nodePanelContainer.value != null) {
    if (props.selectedNode.show) {
      nodePanelContainer.value.style.width = "70%";
      // is needed for loading in Tabs.vue
      if (!nodePanelAnimationDone.value) {
        setTimeout(() => {
          nodePanelAnimationDone.value = true;
        }, 1500);
      }
      positionGraph();
      nodePanelOpen.value = true;
    } else if (!props.selectedNode.show) {
      nodePanelOpen.value = false;
      nodePanelContainer.value.style.width = "0";
      positionGraph();
    }
  }
});

const positionGraph = () => {
  if (nodePanelOpen.value) {
    return;
  }
  const graph = store.getters["graph"];
  // position graph while opening/closing NodePanel
  const intervalID = setInterval(() => {
    graph.panToCenter();
    graph.fitToContents();
  });
  setTimeout(() => {
    clearInterval(intervalID);
    if (!nodePanelWidth.value && !nodePanelHeight.value) {
      setTabContentWidth();
    }
  }, 1500);
};

const setTabContentWidth = () => {
  nodePanelWidth.value = nodePanelContainer.value.clientWidth;
  nodePanelHeight.value = nodePanelContainer.value.clientHeight;
  const tabContents = document.getElementsByClassName("tab-content-container");
  for (let i = 0; i < tabContents.length; i++) {
    tabContents[i].classList.add("contentSize");
    /*    tabContents[i].setAttribute(
      "style",
      `${tabContents[i].getAttribute("style")}; width: ${
        nodePanelWidth.value
      }px; height: ${nodePanelHeight.value - 50}px`
    );*/
  }
};
</script>

<style scoped>
#node-panel-container {
  background-color: #6753e1;
  transition: all 1500ms;
  width: 0;
  height: 100vh;
  z-index: 10;
  overflow: hidden;
}
</style>

<style>
.contentSize {
  width: v-bind(nodePanelWidth + "px");
  height: v-bind(nodePanelHeight - 50 + "px");
}
</style>
