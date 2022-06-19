<template>
  <input
    v-model="networkSelection"
    list="nodes"
    name="nodes"
    placeholder="---server node---"
  />
  <datalist id="nodes">
    <option v-for="node in nodes" :key="node" :value="node">
      {{ node }}
    </option>
  </datalist>
</template>

<script setup lang="ts">
import { ref, defineProps, watch, defineEmits, computed } from "vue";
import Node from "@/models/Node";

// vue data
const props = defineProps(["bmType", "nodeID"]);
const emit = defineEmits(["networkSelected"]);

// data
const networkSelection = ref("");
const nodes = computed(() => Node.all().map((node: Node) => node.$id));

// methods
watch(networkSelection, () => {
  if (nodes.value.indexOf(networkSelection.value) != -1) {
    emit("networkSelected", {
      bmType: props.bmType,
      value: networkSelection.value,
    });
  } else {
    emit("networkSelected", {
      bmType: props.bmType,
      value: "",
    });
  }
});

watch(props, () => {
  networkSelection.value = "";
  emit("networkSelected", {
    bmType: props.bmType,
    value: networkSelection.value,
  });
});
</script>

<style scoped>
input {
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
