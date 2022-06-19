import { Model } from "@vuex-orm/core";
import { ActionTree, MutationTree, GetterTree, Module } from "vuex";
import { RootState } from "@/store";
import benchmarkService from "@/services/benchmark-service";
export default class Node extends Model {
  static entity = "nodes";

  static primaryKey = "id";

  static fields() {
    return {
      id: this.attr(null),
      name: this.attr(""),
      color: this.attr("white"),
      apiVersion: this.attr(null),
      kind: this.attr(null),
      metadata: this.attr(null),
      spec: this.attr(null),
      status: this.attr(null),
      show: this.attr(false),
      bmScore: this.attr(10),
      metrics: this.attr(null),
      scores: this.attr(null),
    };
  }
}

//Nodes Module

/**
 * dispatch examples:
 *  store.$db().model("nodes").dispatch("actionName");
 *  Node.dispatch("actionName");
 *
 * get store content:
 *   store.state.entities.moduleName.keyName
 *   store.getters["entities/moduleName/keyName"]
 *   const NodeModel = store.$db().model("nodes");
 *   NodeModel.query().*       *: all(), find(), where().get(), has(), with() ..
 *   Node.query().*
 */

interface NodeState {
  isLoading: boolean;
}

const state = () =>
  ({
    isLoading: false,
  } as NodeState);

const getters: GetterTree<NodeState, RootState> = {
  loadingState(state: NodeState) {
    console.log("getter loadingState");
    return state.isLoading;
  },
};

const actions: ActionTree<NodeState, RootState> = {
  async fetchNodes({ commit }) {
    // benchmark-service getNodes call
    console.log("action start - benchmark backend fetch nodes");
    const params = {
      key: "value",
    };
    await benchmarkService.get("nodes", { params });
    commit("setLoading", true);
    const nodesResponse = await benchmarkService.get("/nodes");
    console.log("******* nodes **********");
    console.log(nodesResponse.data);
    const nodes = nodesResponse.data;
    for (const node of nodes) {
      const index: number = nodes.indexOf(node);
      nodes[index] = {
        ...node,
        id: node.metadata.name,
        name: node.metadata.name,
        bmScore: index + 2,
      };
    }
    /*    const bmData = [
      { id: 1, name: "node1", color: "white", bmScore: 2.75 },
      { id: 2, name: "node2", color: "white", bmScore: 8 },
      { id: 3, name: "node3", color: "white", bmScore: 4 },
      { id: 4, name: "node4", color: "white", bmScore: 6 },
    ];*/

    // insert fetched data into vuex store
    commit("insertNodes", nodes);
    commit("setLoading", false);
    return "action get Node worked";
  },
  async fetchMetricsById({ commit }, { node, timeDelta }) {
    const metricsResponse = await benchmarkService
      .get(`/metrics/${node.id}/${timeDelta}`)
      .then((data) => {
        const updatedNode = { ...node, metrics: data.data };
        commit("updateNode", updatedNode);
      });
  },
  async fetchScore({ commit }, node) {
    await benchmarkService.get(`/scores/${node.id}`).then((response) => {
      console.log("************************asd");
      console.log(response.data);
      const updatedNode = { ...node, scores: response.data };
      commit("updateNode", updatedNode);
    });
  },
};

const mutations: MutationTree<NodeState> = {
  setLoading(state, isLoading) {
    state.isLoading = isLoading;
  },
  insertNodes(state, payload) {
    console.log("mutation start - insertNodes");
    Node.insert({
      data: payload,
    }).then(() => {
      console.log("mutation end - store filled");
    });
  },
  updateNode(state, payload) {
    console.log(`mutation start - update node '${payload.id}'`);
    Node.update(payload).then((r) =>
      console.log(`mutation end - node '${payload.id}' updated`)
    );
  },
};

export const nodes: Module<NodeState, RootState> = {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
