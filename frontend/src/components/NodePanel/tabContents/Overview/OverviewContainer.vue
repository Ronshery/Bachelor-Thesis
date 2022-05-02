<template>
  <Overview :node="props.node" />
</template>

<script setup lang="ts">
import { defineProps } from "vue";
import Overview from "@/components/NodePanel/tabContents/Overview/Overview.vue";

// vue data
const props = defineProps(["node"]);
</script>

<style scoped></style>
