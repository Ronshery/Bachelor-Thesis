<template>
  <div class="hamburger">
    <div
      class="item item-first"
      :class="{ 'hamburger-is-open': hamburgerOpen }"
    ></div>
    <div
      class="item item-middle"
      :class="{ 'hamburger-is-open': hamburgerOpen }"
    ></div>
    <div
      class="item item-last"
      :class="{ 'hamburger-is-open': hamburgerOpen }"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";

// vue data
const props = defineProps(["hamburgerOpen"]);
</script>

<style scoped>
.hamburger {
  height: 18px;
  width: 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}
.hamburger:hover {
  cursor: pointer;
}

.item {
  height: 3px;
  width: 100%;
  background: black;
  transition: transform 300ms cubic-bezier(0.445, 0.05, 0.55, 0.95),
    opacity 300ms linear;
}

.item-first.hamburger-is-open {
  transform: translate(0, 5px) rotate(45deg);
}
.item-middle.hamburger-is-open {
  opacity: 0;
}
.item-last.hamburger-is-open {
  transform: translate(0, -7px) rotate(-45deg);
}
</style>
