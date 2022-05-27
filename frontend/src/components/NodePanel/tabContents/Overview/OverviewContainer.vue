<template>
  <div class="node-name-wrapper">
    <span class="node-name">
      {{ nodeName }}
    </span>
  </div>
  <Overview :node="node" :nodePanelOpen="nodePanelOpen" />
</template>

<script setup lang="ts">
import { computed, defineProps, ref } from "vue";
import Overview from "@/components/NodePanel/tabContents/Overview/Overview.vue";
import { useStore } from "vuex";

// vue data
const props = defineProps(["node", "nodePanelOpen"]);
const store = useStore();

// data
const NodeModel = computed(() => store.$db().model("nodes"));
const updatedNode = ref();

/*watch(props, async () => {
  await NodeModel.value.dispatch("fetchMetricsById", {
    node: props.node,
    timeDelta: 100,
  });
  updatedNode.value = NodeModel.value.find(props.node.id);
});*/

// methods
const nodeName = computed(() => {
  if (props.node) {
    return props.node.name;
  } else {
    return "";
  }
});
</script>

<style scoped>
.node-name-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 1em;
}

.node-name {
  background-color: white;
  border-radius: 8px;
  padding: 5px;
  font-weight: bold;
}
</style>

<style>
.blink_me {
  animation: blinker 1s linear infinite;
}

@keyframes blinker {
  50% {
    opacity: 0;
  }
}
</style>
