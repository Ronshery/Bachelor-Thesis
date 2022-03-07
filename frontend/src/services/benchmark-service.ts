import axios, { AxiosInstance, AxiosRequestConfig } from "axios";

const config: AxiosRequestConfig = {
  baseURL: process.env.VUE_APP_BENCHMARK_SERVICE_URL,
  headers: {},
};

const benchmarkService: AxiosInstance = axios.create(config);

export default benchmarkService;
