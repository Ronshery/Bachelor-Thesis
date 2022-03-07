import { Database } from "@vuex-orm/core";
import Node, { nodes } from "./models/Node";

const database = new Database();

database.register(Node, nodes);

export default database;
