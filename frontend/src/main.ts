import { createApp } from "vue";
import App from "./App.vue";
import router from "@/router";
import store from "@/store";
import VNetworkGraph from "v-network-graph";
import "v-network-graph/lib/style.css";
import VueApexCharts from "vue3-apexcharts";

createApp(App)
  .use(VueApexCharts)
  .use(VNetworkGraph)
  .use(store)
  .use(router)
  .mount("#app");
