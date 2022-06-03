<template>
  <span class="icon-wrapper" @click="toggleIcon">
    <HamburgerIcon class="hamburger" :hamburgerOpen="menuOpen" />
  </span>
  <div id="menu">
    <div class="menu-items-wrapper">
      <span
        @click="itemClicked(item)"
        class="menu-item"
        v-for="item in items"
        :key="item"
      >
        {{ item }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from "vue";
import HamburgerIcon from "@/components/utils/HamburgerIcon.vue";

// vue data
const props = defineProps(["items"]);
const emit = defineEmits(["itemClicked"]);
// data
const menuOpen = ref(false);

// methods
const toggleIcon = () => {
  menuOpen.value = !menuOpen.value;
  toggleDisplayCSS();
};

const itemClicked = (item: string) => {
  emit("itemClicked", item);
};

const toggleDisplayCSS = () => {
  const menu = document.getElementById("menu");
  if (menu) {
    if (menuOpen.value) {
      menu.style.visibility = "visible";
      menu.style.opacity = "1";
    } else {
      menu.style.opacity = "0";
      setTimeout(() => {
        menu.style.visibility = "hidden";
      }, 500);
    }
  }
};
</script>

<style scoped>
#menu {
  background-color: rgb(76, 79, 105);
  border: 1px solid #191824;
  color: white;
  border-radius: 20px;
  padding: 0.75em 1em 1em 1em;
  opacity: 0;
  visibility: hidden;
  transition: opacity 500ms;
  position: relative;
}

.menu-items-wrapper {
  margin: 0 3.5em 0 0;
}

.menu-item {
  display: flex;
  flex-direction: column;
  cursor: pointer;
  margin: 2px;
}

.menu-item:hover {
  color: lightgray;
}

.icon-wrapper {
  position: absolute;
  background-color: white;
  border-radius: 50%;
  padding: 11px;
  right: 1em;
  margin-top: 0.5em;
  z-index: 10;
  cursor: pointer;
}

.hamburger {
  float: right;
}
</style>
