import { Model } from "@vuex-orm/core";
import { ActionTree, MutationTree, GetterTree, Module } from "vuex";
import { RootState } from "@/store";
import benchmarkService from "@/services/benchmark-service";
import { BmType } from "@/components/NodePanel/tabContents/Benchmark/utils/bm-utils";

export default class Benchmark extends Model {
  static entity = "benchmarks";

  static primaryKey = "id";

  static fields() {
    return {
      id: this.attr(null),
      type: this.attr(null),
      resource: this.attr(null),
      started: this.attr(null),
      metrics: this.attr(null),
      spec: this.attr(null),
      node: this.attr(null),
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
  async fetchBenchmarksByNode({ commit }, { nodeID }) {
    console.log(nodeID);
    benchmarkService
      .get(`/benchmarks/node=${nodeID}/results`)
      .then((response) => {
        console.log(`******* benchmarks ${nodeID} **********`);
        console.log(response.data);
        const benchmarks = response.data;
        for (let i = 0; i < response.data.length; i++) {
          benchmarks[i] = {
            ...benchmarks[i],
            node: nodeID,
          };
        }
        commit("insertBenchmark", benchmarks);
      });
  },
  async fetchBenchmarkById({ commit }, benchmark) {
    benchmarkService
      .get(`/benchmarks/name=${benchmark.id}/results`)
      .then((response) => {
        if (
          Object.keys(response.data).length > 0 &&
          Object.values(response.data.metrics)[0] != null
        ) {
          benchmark = { ...benchmark, ...response.data };
          commit("updateBenchmark", benchmark);
        }
      })
      .catch((error) => {
        if (error.response.status == 404) {
          console.log("results not ready, try again...");
        }
      });
  },
  async runBenchmark({ commit }, { benchmarkType, nodeID }) {
    benchmarkService
      .post(`/benchmark/${benchmarkType}/${nodeID}`)
      .then((response) => {
        console.log(response);
        const isNetworkBm =
          benchmarkType == BmType.NETWORK_IPERF3 ||
          benchmarkType == BmType.NETWORK_QPERF;

        const benchmark = {
          id: isNetworkBm ? response.data.id + "-client" : response.data.id,
          node: isNetworkBm ? nodeID.split("@@@")[0] : nodeID,
          type: benchmarkType.split("-")[0],
          resource: benchmarkType.split("-")[0],
          spec: response.data.spec,
        };
        commit("insertBenchmark", benchmark);
      });
  },
};

const mutations: MutationTree<BenchmarkState> = {
  insertBenchmark(state, payload) {
    console.log("mutation start - insertBenchmark");
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
