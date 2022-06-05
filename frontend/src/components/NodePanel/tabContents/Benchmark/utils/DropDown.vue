<template>
  <select v-model="networkSelection">
    <option value="0" disabled>--server node--</option>
    <option
      v-for="node in nodes"
      :key="node.$getAttributes().id"
      :value="node.$getAttributes().id"
    >
      {{ node.$getAttributes().id }}
    </option>
  </select>
</template>

<script setup lang="ts">
import { ref, defineProps, watch, defineEmits, computed } from "vue";
import Node from "@/models/Node";

// vue data
const props = defineProps(["bmType", "nodeID"]);
const emit = defineEmits(["networkSelected"]);

// data
const networkSelection = ref("0");
const nodes = computed(() => Node.all());

// methods
watch(networkSelection, () => {
  emit("networkSelected", {
    bmType: props.bmType,
    value: networkSelection.value,
  });
});

watch(props, () => {
  networkSelection.value = "0";
  emit("networkSelected", {
    bmType: props.bmType,
    value: networkSelection.value,
  });
});
</script>

<style scoped>
select {
  border-radius: 8px;
  border: 1px solid white;
  background-color: #282935ff;
  padding: 5px;
  font-weight: bold;
  color: white;
  margin-left: 1em;
}

option {
  background-color: #282935ff;
  color: white;
  border-radius: 20px;
}
</style>
