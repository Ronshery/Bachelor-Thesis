import { Model } from "@vuex-orm/core";
import { ActionTree, MutationTree, GetterTree, Module } from "vuex";
import { RootState } from "@/store";
import benchmarkService from "@/services/benchmark-service";
import bmUtils from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";
export default class Benchmark extends Model {
  static entity = "benchmarks";

  static primaryKey = "id";

  static fields() {
    return {
      id: this.attr(null),
      spec: this.attr(null),
      node: this.attr(null),
      results: this.attr(null),
    };
  }
}

interface BenchmarkState {
  isLoading: boolean;
}

const state = () =>
  ({
    isLoading: false,
  } as BenchmarkState);

const getters: GetterTree<BenchmarkState, RootState> = {};

const actions: ActionTree<BenchmarkState, RootState> = {
  async runBenchmark({ commit }, { benchmarkType, nodeID }) {
    benchmarkService
      .post(`/benchmark/${benchmarkType.split("_").join("-")}/${nodeID}`)
      .then((response) => {
        const bmDuration =
          parseInt(bmUtils.getBMDuration(response.data.spec.spec.options)) *
          1000;
        const benchmark = {
          id: response.data.id,
          spec: response.data.spec,
          node: nodeID,
          results: undefined,
        };

        let intervalID = 0;
        const fetchResults = () => {
          benchmarkService
            .get(`/benchmarks/name=${benchmark.id}/results`)
            .then((response) => {
              if (Object.keys(response.data).length > 0) {
                clearInterval(intervalID);
                benchmark.results = response.data;
                commit("updateBenchmark", benchmark);
              }
            })
            .catch((error) => {
              console.log(error);
            });
        };
        // fetch results when benchmark ends
        setTimeout(() => {
          // do it again until results are ready
          intervalID = setInterval(() => {
            fetchResults();
          }, 1000);
        }, bmDuration);
        commit("insertBenchmark", benchmark);
        console.log("test");
      });
  },
};

const mutations: MutationTree<BenchmarkState> = {
  insertBenchmark(state, payload) {
    console.log("mutation start - insertBenchmark");
    console.log(state);
    Benchmark.insert({
      data: payload,
    }).then(() => {
      console.log("mutation end - insertBenchmark");
    });
  },
  updateBenchmark(state, payload) {
    console.log(`mutation start - update benchmark '${payload.id}'`);
    Benchmark.update(payload).then((r) => {
      console.log(`mutation end - update benchmark '${payload.id}'`);
    });
  },
};
export const benchmarks: Module<BenchmarkState, RootState> = {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
