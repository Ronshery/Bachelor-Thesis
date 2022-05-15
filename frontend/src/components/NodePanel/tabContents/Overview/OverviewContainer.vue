<template>
  <Overview :node="updatedNode" :nodePanelOpen="nodePanelOpen" />
</template>

<script setup lang="ts">
import { computed, defineProps, watch, ref } from "vue";
import Overview from "@/components/NodePanel/tabContents/Overview/Overview.vue";
import { useStore } from "vuex";

// vue data
const props = defineProps(["node", "nodePanelOpen"]);
const store = useStore();

// data
const NodeModel = computed(() => store.$db().model("nodes"));
const updatedNode = ref();

watch(props, async () => {
  await NodeModel.value.dispatch("fetchMetricsById", {
    node: props.node,
    timeDelta: 100,
  });
  updatedNode.value = NodeModel.value.find(props.node.id);
});
</script>

<style scoped></style>
