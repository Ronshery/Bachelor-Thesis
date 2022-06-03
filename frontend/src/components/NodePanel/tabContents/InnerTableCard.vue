<template>
  <div class="wrapper">
    <div class="row" v-for="(value, index) in listAsObject" :key="value">
      <div class="row-element-left" :style="cssStyleLeft">
        {{ mappings[index] }}
      </div>
      <div class="row-element-right" :style="cssStyleRight">
        {{ value }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";

// vue data
const props = defineProps([
  "listAsObject",
  "cssStyleLeft",
  "cssStyleRight",
  "mappings",
]);

// data
</script>

<style scoped>
.row {
  display: flex;
  padding: 0.25vw;
}

.row-element-left {
  width: 50%;
}

.row-element-right {
  width: 50%;
  color: #006fff;
}

.wrapper {
  background-color: #efefef;
  border-radius: 7px;
  box-shadow: 0 2px 2px 2px rgba(0, 0, 0, 0.29);
  padding: 0.25vw 0 0.25vw 0.5vw;
}
</style>
