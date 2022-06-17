import { createStore } from "vuex";
import { ActionTree, MutationTree, GetterTree } from "vuex";
import VuexORM from "@vuex-orm/core";
import database from "@/database";
import VuexPersistence from "vuex-persist";

const vuexLocal = new VuexPersistence<RootState>({
  storage: window.sessionStorage,
});

export interface RootState {
  graph: any;
}

const state = () =>
  ({
    graph: null,
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
  plugins: [VuexORM.install(database), vuexLocal.plugin],
  state,
  getters,
  actions,
  mutations,
});

export default store;
