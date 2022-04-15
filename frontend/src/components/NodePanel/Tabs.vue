<template>
  <div id="tab-header-container">
    <div v-for="(tab, index) in tabList" :key="tab.title" class="tab-container">
      <div
        @click="changeTab($event, index)"
        :class="
          index == 0
            ? 'tab selected'
            : index == 1
            ? 'tab first-is-selected'
            : 'tab'
        "
      >
        {{ tab.title }}
      </div>
    </div>
  </div>
  <Tab ref="OverviewComponent">{{ node }} Overview Content</Tab>
  <Tab ref="BenchmarkComponent">{{ node }} Benchmark Content</Tab>
  <Tab ref="SettingsComponent">{{ node }} Settings Content</Tab>
</template>

<script setup lang="ts">
import { ref, onMounted, defineProps, watch } from "vue";
import Tab from "@/components/NodePanel/Tab.vue";

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
watch(props, () => {
  if (!props.nodePanelOpen) {
    console.log("close");
    timer = setTimeout(() => {
      resetTabClasses(null);
    }, 1500);
  } else if (props.nodePanelOpen) {
    console.log("open");
    clearTimeout(timer);
  }
});

onMounted(() => {
  tabList.value[0].ref.isActive = true;
});

const changeTab = (event: any, index: number) => {
  updateBorderRadius(index, event.target);
  tabList.value.forEach((tab, i) => {
    console.log(tab.ref.isActive);
    tab.ref.isActive = index === i;
  });
  selectedTab.value = {
    element: event.target,
    index: index,
    title: event.target.innerText,
  };
  console.log(tabList.value);
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
