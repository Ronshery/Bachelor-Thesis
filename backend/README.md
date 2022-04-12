# Backend

## Kubernetes Setup using kind
### Dependencies
- Docker 
- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
- [helm](https://helm.sh/docs/intro/install/)
- kubectl >= 1.14

### Setup dev cluster

Create a three node kind cluster using the command below:
```sh
./create_dev_cluster.sh
```

This builds the `perona-operator` Docker image, installs it into the dev Kubernetes cluster and also deploys a Prometheus stack for monitoring.

The perona-api will be available at `http://localhost:8000`.
Prometheus can be reached at `http://localhost:9090`.


## Running benchmarks

### Example benchmark execution

Using our Rest API, this can be accomplished as:
```sh
    $ curl -X 'POST' 'http://localhost:8000/benchmark/{bm_type}/{node_id}' -H 'accept: application/json' -d ''
```
where `bm_type` could be e.g. `disk-fio` or `cpu-sysbench`.
Note that for network benchmarks, it is required to specify a `client` and `server`.
You can do that by encoding this into `node_id` using `@@@` as separator, i.e. `node1@@@node2` would make `node1` be the client-node and `node2` the server-node.

