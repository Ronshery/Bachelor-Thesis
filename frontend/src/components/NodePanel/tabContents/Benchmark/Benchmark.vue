<template>
  <TabLayout>
    <div class="menu-wrapper">
      <Menu :items="menuItems" />
    </div>
    <BenchmarkChapter
      v-for="(bm, key) in availableBenchmarks"
      :key="key"
      :benchmark="key"
    >
      <div v-if="key == 'cpu'">
        <BenchmarkTypeCards :bmTypes="bm" :nodeID="props.node.name" />
      </div>
      <div v-if="key == 'network'">{{ bm }}</div>
      <div v-if="key == 'memory'">{{ bm }}</div>
      <div v-if="key == 'disk'">{{ bm }}</div>
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

const myfnc = () => {
  document
    .getElementById("cpu-benchmark")
    .scrollIntoView({ behavior: "smooth" });
};
</script>

<style scoped>
.menu-wrapper {
  position: absolute;
  right: 2em;
}
</style>
