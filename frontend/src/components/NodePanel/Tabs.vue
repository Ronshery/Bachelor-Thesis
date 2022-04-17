<template>
  <div id="tab-header-container">
    <div v-for="(tab, index) in tabList" :key="tab.title" class="tab-container">
      <div
        @click="nodePanelAnimationDone ? changeTab($event, index) : () => {}"
        class="tab"
        :class="{
          selected: index == 0,
          'first-is-selected': index == 1,
          disabled: !nodePanelAnimationDone,
        }"
      >
        {{ tab.title }}
      </div>
    </div>
  </div>
  <div v-if="!nodePanelAnimationDone">Loading ...</div>
  <div v-else>
    <Tab ref="OverviewComponent"
      >{{ node }}
      Overview Content
      <div style="height: 600px; width: 80%; border: 2px solid red"></div>
      <div style="height: 600px; width: 80%; border: 2px solid red"></div>
    </Tab>
    <Tab ref="BenchmarkComponent">{{ node }} Benchmark Content</Tab>
    <Tab ref="SettingsComponent">{{ node }} Settings Content</Tab>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, watch, nextTick } from "vue";
import Tab from "@/components/NodePanel/Tab.vue";
import LoadingAnimation from "@/components/LoadingAnimation.vue";

interface ITab {
  element: HTMLElement;
  index: number;
  title: string;
}

// vue data
const props = defineProps(["node", "nodePanelOpen", "nodePanelAnimationDone"]);

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
let animationDoneSet = false;
//methods
let timer: number;
watch(props, () => {
  if (!props.nodePanelOpen) {
    console.log("close");
    timer = setTimeout(() => {
      resetTabClasses(null);
      changeTab(document.getElementsByClassName("tab")[0], 0);
    }, 1500);
  } else if (props.nodePanelOpen) {
    console.log("open");
    clearTimeout(timer);
  }
  if (props.nodePanelAnimationDone && !animationDoneSet) {
    animationDoneSet = true;
    nextTick(() => {
      tabList.value[0].ref.isActive = true;
    });
  }
});

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
  background-color: #6753e1;
  color: black;
  font-weight: bold;
}

.tab {
  background-color: white;
  line-height: v-bind(tabHeight);
  text-align: center;
  padding: 0 30px 0 30px;
  cursor: pointer;
}

.selected {
  background-color: #6753e1;
  color: white;
}

.disabled {
  cursor: unset;
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
