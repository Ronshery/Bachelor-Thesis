<template>
  <router-view />
</template>

<script setup lang="ts"></script>
<style>
* {
  margin: 0;
}

body {
  overflow: hidden;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}

::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-thumb {
  background: white;
  border-radius: 100px;
}

::-webkit-scrollbar-thumb:hover {
  background: lightgray;
}
</style>
