<template>
  <TabLayout>
    <div class="menu-wrapper">
      <Menu :items="menuItems" @itemClicked="itemClicked" />
    </div>
    <BenchmarkChapter
      v-for="(bm, key) in availableBenchmarks"
      :key="key"
      :benchmark="key"
    >
      <div v-if="key === 'cpu'">
        <BenchmarkTypeCards :bmTypes="bm" :nodeID="props.node.name" :key="bm" />
      </div>
      <div v-if="key === 'network'">
        <BenchmarkTypeCards :bmTypes="bm" :nodeID="props.node.name" :key="bm" />
      </div>
      <div v-if="key === 'memory'">
        <BenchmarkTypeCards :bmTypes="bm" :nodeID="props.node.name" :key="bm" />
      </div>
      <div v-if="key === 'disk'">
        <BenchmarkTypeCards :bmTypes="bm" :nodeID="props.node.name" :key="bm" />
      </div>
    </BenchmarkChapter>
  </TabLayout>
</template>

<script setup lang="ts">
import { computed, defineProps } from "vue";
import TabLayout from "@/components/NodePanel/tabContents/TabLayout.vue";
import Menu from "@/components/utils/Menu.vue";
import BenchmarkChapter from "@/components/NodePanel/tabContents/Benchmark/BenchmarkChapter.vue";
import BenchmarkTypeCards from "@/components/NodePanel/tabContents/Benchmark/benchmarkTypes/BenchmarkTypeCards.vue";
import bmScript from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";

// vue data
const props = defineProps(["node", "nodePanelOpen", "availableBenchmarks"]);

// data
// methods
const menuItems = computed(() => {
  let list = Object.keys(props.availableBenchmarks);
  for (let i = 0; i < list.length; i++) {
    list[i] = bmScript.benchmarkNameMapper(list[i]);
  }
  return list;
});

const itemClicked = (param: string) => {
  let chapterID = param.toLowerCase().split(" ")[0] + "-chapter";
  const chapterElement = document.getElementById(chapterID);
  if (chapterElement) {
    chapterElement.scrollIntoView({ behavior: "smooth" });
  }
};
</script>

<style scoped>
.menu-wrapper {
  position: absolute;
  right: 2em;
}
</style>
