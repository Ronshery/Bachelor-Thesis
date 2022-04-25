<template>
  <div class="two-column-layout-container">
    <div class="left">My Page Layout Column 1</div>
    <div class="right">My Page Layout Column 2</div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.two-column-layout-container {
  display: flex;
  flex-direction: row;
}

.container > div {
  flex-basis: 50%;
}

.left {
  background-color: #6753e1;
}
.right {
  background-color: #ff6955;
}
</style>
