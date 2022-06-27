<template>
  <div class="card" :style="props.cssStyle">
    <div class="card-child">
      <div class="card-title">
        <slot name="title"></slot>
      </div>
      <div class="card-content-wrapper">
        <slot name="default" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, withDefaults, ref } from "vue";

interface Props {
  cssStyle?: { [key: string]: string };
  isSVG?: boolean;
}

// vue data
const props = withDefaults(defineProps<Props>(), {
  isSVG: false,
});

// data
const marginLeft = ref<string>("");
const marginBottomTitle = ref<string>("");
if (!props.isSVG) {
  marginLeft.value = "1em 1.25em 1em 1.25em";
  marginBottomTitle.value = "0.75em";
}
if (props.isSVG) {
  marginLeft.value = "0 0.75em 0 0.25em";
}
</script>

<style>
.card-child {
  padding: v-bind(marginLeft);
}
.card {
  border-radius: 20px;
  margin-bottom: 16px;
  width: 49%;
  background-color: white;
  min-width: 500px;
}

.card-title {
  font-weight: bold !important;
  margin-bottom: v-bind(marginBottomTitle);
}

.card:nth-child(odd) {
  margin-right: 10px;
}
.card:nth-child(even) {
  position: relative;
  left: 15px;
}

@media screen and (max-width: 1427px) {
  .card {
    width: 100%;
    left: 0 !important;
    margin-right: 2% !important;
    margin-left: 15px;
  }
}
</style>
