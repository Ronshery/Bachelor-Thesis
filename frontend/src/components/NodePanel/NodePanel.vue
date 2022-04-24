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
import { ref, defineProps, watch, onMounted, defineEmits } from "vue";
import { useStore } from "vuex";
import Tabs from "@/components/NodePanel/Tabs.vue";

// vue data
const props = defineProps(["selectedNode"]);
const store = useStore();
const emit = defineEmits(["nodePanel"]);
// data
const nodePanelOpen = ref(false);
const nodePanelAnimationDone = ref(false);
let firstTimeAnimation = true;
const nodePanelContainer = ref();
let nodePanelWidth = ref();
let nodePanelHeight = ref();
const loadAgain = ref(false);
// methods
// too avoid first time calculation
let resizeStarted = false;
/*onMounted(() => {
  window.addEventListener("resize", () => {
    // !firstTimeAnimation: otherwise it would set width and height to zero
    if (resizeStarted && !firstTimeAnimation) {
      console.log("resize ");
      const intervalID = setInterval(() => {
        setTabContentWidth();
      });
      setTimeout(() => {
        clearInterval(intervalID);
      }, 1500);
    }

    resizeStarted = true;
  });
});*/
const listener = () => {
  loadAgain.value = true;
  setTabContentWidth();
};

watch(nodePanelOpen, () => {
  if (nodePanelOpen.value) {
    window.addEventListener("resize", listener);
  }
});

watch(props, () => {
  if (nodePanelContainer.value != null) {
    if (props.selectedNode.show) {
      nodePanelContainer.value.style.width = "70%";
      // is needed for loading in Tabs.vue
      if (!nodePanelAnimationDone.value) {
        setTimeout(() => {
          nodePanelAnimationDone.value = true;
          firstTimeAnimation = false;
        }, 1500);
      }
      positionGraph();
      nodePanelOpen.value = true;
    } else if (!props.selectedNode.show && !firstTimeAnimation) {
      //firstTimeAnimation is needed to avoid canceling the animation during the first time
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
    if (
      (!nodePanelWidth.value && !nodePanelHeight.value) ||
      (loadAgain.value && nodePanelOpen.value) ||
      nodePanelWidth.value == 0
    ) {
      console.log("do it ");
      setTabContentWidth();
      loadAgain.value = false;
    }
  }, 1500);
};

const setTabContentWidth = () => {
  nodePanelWidth.value = nodePanelContainer.value.clientWidth;
  nodePanelHeight.value = nodePanelContainer.value.clientHeight;
  const tabContents = document.getElementsByClassName("tab-content-container");
  const tabHeaderContainer = document.getElementById("tab-header-container");
  if (tabHeaderContainer) {
    tabHeaderContainer.classList.add("tabHeaderSize");
  }
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
  transition: width 1500ms;
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

.tabHeaderSize {
  width: v-bind(nodePanelWidth + "px");
}
</style>
