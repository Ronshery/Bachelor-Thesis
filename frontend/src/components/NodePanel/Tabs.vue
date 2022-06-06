<template>
  <div id="tab-header-container">
    <div v-for="(tab, index) in tabList" :key="tab.title" class="tab-container">
      <div
        @click="changeTab($event, index)"
        class="tab"
        :class="{
          selected: index == 0,
          'first-is-selected': index == 1,
        }"
      >
        {{ tab.title }}
      </div>
    </div>
  </div>
  <div>
    <Tab ref="OverviewComponent" :nodePanelOpen="nodePanelOpen">
      <OverviewContainer :node="node" :nodePanelOpen="nodePanelOpen" />
    </Tab>
    <Tab ref="BenchmarkComponent" :nodePanelOpen="nodePanelOpen"
      >{{ node }} Benchmark Content
    </Tab>
    <Tab ref="SettingsComponent" :nodePanelOpen="nodePanelOpen"
      >{{ node }} Settings Content</Tab
    >
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, watch, nextTick } from "vue";
import Tab from "@/components/NodePanel/Tab.vue";
import OverviewContainer from "@/components/NodePanel/tabContents/Overview/OverviewContainer.vue";

interface ITab {
  element: HTMLElement;
  index: number;
  title: string;
}

// vue data
const props = defineProps(["node", "nodePanelOpen"]);

// data
const tabHeight = "50px";
const selectedTab = ref<ITab>();
const OverviewComponent = ref();
const BenchmarkComponent = ref();
const SettingsComponent = ref();
const tabList = ref([
  { title: "Overview", ref: OverviewComponent },
  { title: "Benchmark", ref: BenchmarkComponent },
  { title: "Settings", ref: SettingsComponent },
]);
//methods
let timer: number;
let firstTime = false;
let lastSelectedNode: typeof props.node;
watch(props, () => {
  if (!props.nodePanelOpen) {
    console.log("close");
    // only reset when NodePanel is fully closed
    timer = setTimeout(() => {
      resetTabClasses(null);
      changeTab(document.getElementsByClassName("tab")[0], 0);
    }, 1500);
  } else if (props.nodePanelOpen) {
    console.log("open");
    blinkNodeName();
    resetActiveTab();
    // don't close if interrupt closing NodePanel
    clearTimeout(timer);
  }
  if (!firstTime) {
    firstTime = true;
    nextTick(() => {
      tabList.value[0].ref.isActive = true;
    });
  }
});

const blinkNodeName = () => {
  const nodeNameWrapper =
    document.getElementsByClassName("node-name-wrapper")[0];
  nodeNameWrapper.classList.add("blink_me");
  setTimeout(() => {
    nodeNameWrapper.classList.remove("blink_me");
  }, 900);
};
const resetActiveTab = () => {
  if (lastSelectedNode == undefined) {
    lastSelectedNode = props.node;
  } else if (lastSelectedNode.id != props.node.id) {
    changeTab(document.getElementsByClassName("tab")[0], 0);
    lastSelectedNode = props.node;
  }
};

const changeTab = (event: any, index: number) => {
  const tabElement = event.target ? event.target : event;
  updateBorderRadius(index, tabElement);
  tabList.value.forEach((tab, i) => {
    tab.ref.isActive = index === i;
  });
  selectedTab.value = {
    element: tabElement,
    index: index,
    title: tabElement.innerText,
  };
};

const updateBorderRadius = (
  selectedIndex: number,
  selectedElement: HTMLElement
) => {
  resetTabClasses(selectedElement);
  const tabsElementList = document.getElementsByClassName("tab");

  if (selectedIndex != 0) {
    document
      .getElementsByClassName("tab")
      [selectedIndex - 1].classList.add("next-is-selected");
  }
  if (selectedIndex != tabsElementList.length - 1) {
    document
      .getElementsByClassName("tab")
      [selectedIndex + 1].classList.add("before-is-selected");
  }
};

const resetTabClasses = (selectedElement: HTMLElement | null) => {
  const tabsElementList = document.getElementsByClassName("tab");

  // reset
  for (let i = 0; i < tabsElementList.length; i++) {
    tabsElementList[i].className = "tab";
  }
  if (selectedElement == null) {
    tabsElementList[0].className = "tab selected";
    tabsElementList[1].classList.add("before-is-selected");
    return;
  }
  selectedElement.classList.add("selected");
};
</script>

<style scoped>
#tab-header-container {
  height: v-bind(tabHeight);
  display: flex;
  background-color: white;
}

.tab-container {
  background-color: #393b54;
  color: black;
  font-weight: bold;
  width: 100%;
}

.tab {
  background-color: white;
  line-height: v-bind(tabHeight);
  text-align: center;
  padding: 0 30px 0 30px;
  cursor: pointer;
}

.selected {
  background-color: #393b54;
  color: white;
}

.first-is-selected {
  border-bottom-left-radius: 20px;
}

.next-is-selected {
  border-bottom-right-radius: 20px;
}

.before-is-selected {
  border-bottom-left-radius: 20px;
}
</style>
