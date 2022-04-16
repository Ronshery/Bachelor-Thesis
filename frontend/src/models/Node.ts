import { Model } from "@vuex-orm/core";
import { ActionTree, MutationTree, GetterTree, Module } from "vuex";
import { RootState } from "@/store";
import * as vNG from "v-network-graph";
import benchmarkService from "@/services/benchmark-service";
//import benchmarkService from "@/services/benchmark-service";

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
    /*    const params = {
      key: "value",
    };
    await benchmarkService.get("nodes", { params });*/
    commit("setLoading", true);
    /*    const { data } = await benchmarkService.get("/nodes");
    console.log("******* data **********");
    console.log(data);
        data[0] = {
      ...data[0],
      name: data[0].metadata.name,
    };*/
    const bmData = [
      { id: 1, name: "node1", color: "white" },
      { id: 2, name: "node2", color: "white" },
      { id: 3, name: "node3", color: "white" },
      { id: 4, name: "node4", color: "white" },
    ];
    // insert fetched data into vuex store
    commit("insertNodes", bmData);
    commit("setLoading", false);
    return "action get Node worked";
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
};

export const nodes: Module<NodeState, RootState> = {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
