<template>
  <Overview :node="node" :nodePanelOpen="nodePanelOpen" />
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import Overview from "@/components/NodePanel/tabContents/Overview/Overview.vue";

// vue data
const props = defineProps(["node", "nodePanelOpen"]);
</script>

<style scoped></style>
