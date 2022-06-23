import axios, { AxiosInstance, AxiosRequestConfig } from "axios";

const config: AxiosRequestConfig = {
  baseURL: "http://localhost:8000",
  headers: {},
};

const benchmarkService: AxiosInstance = axios.create(config);

export default benchmarkService;
