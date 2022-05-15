<template>
  <div class="card" :style="props.cssStyle">
    <div class="card-child">
      <div class="card-title">
        <slot name="title"></slot>
      </div>
      <slot name="default" />
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
</script>

<style scoped>
.card > .card-child {
  padding: v-bind(marginLeft);
}
.card {
  border-radius: 20px;
  margin-bottom: 16px;
  width: 49%;
  background-color: white;
}

.card-title {
  font-weight: bold !important;
  margin-bottom: v-bind(marginBottomTitle);
}

.card:nth-child(even) {
  margin-right: 10px;
}
.card:nth-child(odd) {
  position: relative;
  left: 6px;
}
</style>
