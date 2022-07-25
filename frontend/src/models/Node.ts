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
      };
    }
    /*
    const bmData = [
      { id: 1, name: "node1", color: "white", bmScore: 5 },
      { id: 2, name: "node2", color: "white", bmScore: 8 },
      { id: 3, name: "node3", color: "white", bmScore: 4 },
      { id: 4, name: "node4", color: "white", bmScore: 6 },
      { id: 5, name: "node5", color: "white", bmScore: 6 },
      { id: 6, name: "node6", color: "white", bmScore: 6 },
      { id: 7, name: "node7", color: "white", bmScore: 6 },
      { id: 8, name: "node8", color: "white", bmScore: 6 },
      { id: 9, name: "node9", color: "white", bmScore: 6 },
      { id: 10, name: "node10", color: "white", bmScore: 6 },
      { id: 11, name: "node11", color: "white", bmScore: 6 },
      { id: 12, name: "node12", color: "white", bmScore: 6 },
      { id: 13, name: "node13", color: "white", bmScore: 6 },
      { id: 14, name: "node14", color: "white", bmScore: 6 },
      { id: 15, name: "node15", color: "white", bmScore: 6 },
      { id: 16, name: "node16", color: "white", bmScore: 6 },
      { id: 17, name: "node17", color: "white", bmScore: 6 },
      { id: 18, name: "node18", color: "white", bmScore: 6 },
      { id: 19, name: "node19", color: "white", bmScore: 6 },
      { id: 20, name: "node20", color: "white", bmScore: 6 },
      { id: 21, name: "node21", color: "white", bmScore: 6 },
      { id: 22, name: "node22", color: "white", bmScore: 6 },
      { id: 23, name: "node23", color: "white", bmScore: 6 },
      { id: 24, name: "node24", color: "white", bmScore: 6 },
      { id: 25, name: "node25", color: "white", bmScore: 6 },
    ];
*/
    // insert fetched data into vuex store
    commit("insertNodes", nodes);
    for (const node of nodes) {
      const index: number = nodes.indexOf(node);
      await Node.dispatch("fetchScore", nodes[index]);
    }
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
    return new Promise((resolve, reject) => {
      benchmarkService
        .get(`/scores/${node.id}/cluster`)
        .then((response) => {
          console.log(response.data);
          const updatedNode = { ...node, scores: response.data };
          resolve(response.data);
          commit("updateNode", updatedNode);
        })
        .catch((error) => {
          if (error.response.status == 500) {
            console.error(error.response.data.detail);
            reject(error.response.data.detail);
          }
        });
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
    Node.update(payload).then((r) => {
      console.log(`mutation end - node '${payload.id}' updated`);
    });
  },
};

export const nodes: Module<NodeState, RootState> = {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
