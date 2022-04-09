<template>
  <NetworkGraph
    :nodes="nodes"
    :edges="edges"
    :configs="configs"
    :layouts="layouts"
    :layers="layers"
    @node-clicked="nodeClicked"
  />
  <NodePanel :node="node" />
</template>

<script lang="ts" setup>
import { reactive, ref } from "vue";
import NetworkGraph from "@/components/NetworkGraph/NetworkGraph.vue";
import NodePanel from "@/components/NodePanel.vue";
import * as vNG from "v-network-graph"; // @ is an alias to /src
// data
const node = ref(null);

// methods
const nodeClicked = (params: any) => {
  console.log(params);
  node.value = params;
  console.log("node updated");
};

// *** v-network-graph config ***
// interfaces
interface Node extends vNG.Node {
  size?: number;
  color: string;
  label?: boolean;
}
// props
const nodes: Record<string, Node> = {
  node1: { name: "Node 1", color: "white" },
  node2: { name: "Node 2", color: "white" },
  node3: { name: "Node 3", color: "white" },
  node4: { name: "Node 4", color: "white" },
};

let edges = ref<vNG.Edges>({
  edge1: { source: "node1", target: "node2" },
  edge2: { source: "node2", target: "node3" },
  edge3: { source: "node3", target: "node4" },
});

const layouts = ref<vNG.Layouts>({
  nodes: {
    node1: { x: 0, y: 100 },
    node2: { x: 250, y: 150 },
    node3: { x: 600, y: 100 },
    node4: { x: 900, y: 150 },
  },
});

const layers = {
  // {layername}: {position}
  badge: "nodes",
};

const configs: vNG.UserConfigs = reactive(
  vNG.defineConfigs({
    view: {
      scalingObjects: true,
      minZoomLevel: 0.1,
      maxZoomLevel: 16,
    },
    node: {
      selectable: 2,
      label: {
        color: "white",
        fontSize: 20,
      },
      normal: {
        type: "rect",
        width: 150,
        height: 150,
        color: (node) => node.color,
      },
      hover: {
        color: "white",
      },
      focusring: {
        color: "black",
      },
    },
  })
);
</script>

<style scoped></style>
