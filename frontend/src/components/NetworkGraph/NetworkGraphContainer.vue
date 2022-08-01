<template>
  <NetworkGraph
    :nodes="nodes"
    :configs="configs"
    :layers="layers"
    :networkGraphRight="networkGraphRight"
    @node-clicked="nodeClicked"
    @close-panel="triggerClosePanel"
  />
  <NodePanel
    :selectedNode="selectedNode"
    :closePanel="closePanel"
    @updatePanelRight="triggerNetworkGraphRight"
  />
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted, computed } from "vue";
import NetworkGraph from "@/components/NetworkGraph/NetworkGraph.vue";
import * as vNG from "v-network-graph"; // @ is an alias to /src
import { useStore } from "vuex";
import NodePanel from "@/components/NodePanel/NodePanel.vue";
import Node from "@/models/Node";

// vue data
const store = useStore();

// data
const selectedNode = ref<Node | null>(null);
const NodeModel = computed(() => store.$db().model("nodes"));
const nodes = computed(() => {
  console.log("nodes query");
  let nodesList = Node.all();

  // convert fetched nodes to v-network-graph format
  let convertedNodesList: Record<string, any> = {};
  nodesList.forEach((node: Record<string, any>) => {
    convertedNodesList[node.name] = node;
  });
  console.log(convertedNodesList);

  return convertedNodesList;
});
let lastSelectedNode = ref();
lastSelectedNode.value = null;

// methods
onMounted(async () => {
  console.log("NetworkGraphContainer mounted");
  await NodeModel.value.dispatch("fetchNodes");
});

const nodeClicked = (params: any) => {
  if (params != null) {
    if (lastSelectedNode.value == null) {
      lastSelectedNode.value = params;
    }
    params.show = true;
    const newScores = Node.find(lastSelectedNode.value.id)?.$getAttributes()
      .scores;
    if (newScores != null) {
      Node.update({
        ...lastSelectedNode.value,
        color: "white",
        scores: newScores,
      });
    } else {
      Node.update({
        ...lastSelectedNode.value,
        color: "white",
      });
    }

    Node.update({ ...params, show: true, color: "#afafaf" });

    selectedNode.value = Node.find(params.id);
    lastSelectedNode.value = params;
  } else {
    if (lastSelectedNode.value == null) {
      return;
    }
    lastSelectedNode.value.show = false;
    lastSelectedNode.value.color = "white";
    const newScores = Node.find(lastSelectedNode.value.id)?.$getAttributes()
      .scores;
    if (newScores != null) {
      NodeModel.value.update({
        ...lastSelectedNode.value,
        show: false,
        color: "white",
        scores: newScores,
      });
    } else {
      NodeModel.value.update({
        ...lastSelectedNode.value,
        show: false,
        color: "white",
      });
    }

    // trigger events again with copy of object
    selectedNode.value = JSON.parse(JSON.stringify(lastSelectedNode.value));
  }
};

const networkGraphRight = ref();
const triggerNetworkGraphRight = (nodePanelRightPercent: number) => {
  networkGraphRight.value = nodePanelRightPercent;
};

const closePanel = ref();
const triggerClosePanel = (close: boolean) => {
  closePanel.value = close;
};

// *** v-network-graph config ***
const layers = {
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
        visible: false,
      },
      normal: {
        type: "rect",
        width: 150,
        height: 150,
        color: (node) => node.color,
        borderRadius: 15,
      },
      hover: {
        color: (node) => node.color,
      },
      focusring: {
        color: "#393b54",
      },
    },
  })
);
</script>

<style scoped></style>
