import { Database } from "@vuex-orm/core";
import Node, { nodes } from "./models/Node";
import Benchmark, { benchmarks } from "@/models/Benchmark";
const database = new Database();

database.register(Node, nodes);
database.register(Benchmark, benchmarks);

export default database;
