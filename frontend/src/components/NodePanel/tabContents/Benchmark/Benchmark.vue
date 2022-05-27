<template>
  <TabLayout>
    <span style="float: right; margin-right: 2.25em">
      <span class="icon-wrapper">
        <HamburgerIcon class="hamburger" />
      </span>
    </span>

    <div
      class="play"
      v-for="benchmark in availableBenchmarks"
      :key="benchmark"
      @click="runBenchmark(benchmark)"
    >
      <span style="background-color: blue; color: white"
        >play {{ benchmark }}</span
      >
    </div>
  </TabLayout>
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import benchmarkService from "@/services/benchmark-service";
import TabLayout from "@/components/NodePanel/tabContents/TabLayout.vue";
import HamburgerIcon from "@/components/utils/HamburgerIcon.vue";

const props = defineProps(["node", "nodePanelOpen", "availableBenchmarks"]);

// methods
const runBenchmark = (benchmark: string) => {
  console.log(benchmark);
  benchmarkService
    .post(`/benchmark/${benchmark.split("_").join("-")}/${props.node.name}`)
    .then((response) => {
      console.log(response.data);
    });
};

const myfnc = () => {
  document
    .getElementById("cpu-benchmark")
    .scrollIntoView({ behavior: "smooth" });
};
</script>

<style scoped>
.play {
  cursor: pointer;
}
.icon-wrapper {
  position: absolute;
  background-color: white;
  border-radius: 17px;
  padding: 19px;
}

.hamburger {
  position: absolute;
  left: 50%;
  top: 50%;
  -webkit-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}
</style>
