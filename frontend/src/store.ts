import { createStore } from "vuex";
import { ActionTree, MutationTree, GetterTree, Module } from "vuex";
import VuexORM from "@vuex-orm/core";
import database from "@/database";

export interface RootState {
  graph: any;
}

const state = () =>
  ({
    graph: null,
    layouts: null,
  } as RootState);

const getters: GetterTree<RootState, RootState> = {
  graph(state: RootState) {
    return state.graph;
  },
};

const actions: ActionTree<RootState, RootState> = {
  initializeGraph({ commit }, graph) {
    commit("INITIALIZE_GRAPH", graph);
  },
};

const mutations: MutationTree<RootState> = {
  INITIALIZE_GRAPH(state: RootState, graph) {
    state.graph = graph;
  },
};

const store = createStore({
  plugins: [VuexORM.install(database)],
  state,
  getters,
  actions,
  mutations,
});

export default store;
