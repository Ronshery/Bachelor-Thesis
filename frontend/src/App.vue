<template>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </nav>
  <router-view />
</template>

<script setup lang="ts">
import { useStore } from "vuex";
import Node from "@/models/Node";

const store = useStore();
const NodeModel = store.$db().model("nodes");
console.log(typeof NodeModel);
console.log("fetching nodes loading: " + store.state.entities.nodes.isLoading);
NodeModel.dispatch("fetchNodes");
console.log("fetching nodes loading: " + store.state.entities.nodes.isLoading);
console.log(
  "another way to get loadingState " +
    store.getters["entities/nodes/loadingState"]
);

console.log("****************");
console.log(store.getters);
console.log(Node.query().all());
console.log(NodeModel.query().where("name", "myfirstnode").get());
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
