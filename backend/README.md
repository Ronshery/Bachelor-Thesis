# Backend


## Kubernetes Setup using minikube

1. Start minikube. **We need Kubernetes version <1.22** since Kubestone uses some extensions which are not supported from Kubernetes v1.22 on. https://github.com/xridge/kubestone/issues/199

   ```sh
    $ minikube start --kubernetes-version=v1.21.11
   ```

2. To use the appropriate kubectl version, we can alias it in our shell session:

   ```sh
    $ alias kubectl=minikube kubectl --
   ```

3. Configure Kubestone (https://kubestone.io/en/latest/quickstart/)

   ```sh
    $ kustomize build github.com/xridge/kubestone/config/default?ref=v0.5.0 | sed "s/kubestone:latest/kubestone:v0.5.0/" | kubectl create -f -
   ```

4. Launch a minikube proxy so we can access the API without further authentication. I did not succeed in finding a way to connect to the Kubernetes API directly, which is why i chose to use a proxy instead.<br>
This example uses plain HTTP on Port 8080 ([helpful SO thread](https://stackoverflow.com/questions/40720979/how-to-access-kubernetes-api-when-using-minkube)):

    ```sh
     $ kubectl proxy --port=8080
    ```

    Now, the only authentication option we need to pass is `server`, which is configured in [`bm_operator/operator_config.py`](bm_operator/operator_config.py):

    ```
    KUBERNETES_SERVER = "http://localhost:8080"
    ```

## Running benchmarks

### Sysbench - https://kubestone.io/en/latest/benchmarks/sysbench/

```sh
    $ kubectl create --namespace kubestone -f https://raw.githubusercontent.com/xridge/kubestone/master/config/samples/perf_v1alpha1_sysbench.yaml
```
Using our Rest API, this can be accomplished as:
```sh
    $ curl -X 'POST' 'http://localhost:8000/benchmark/{bm_type}/{node_id}' -H 'accept: application/json' -d ''
```
where `bm_type` could be e.g. `disk-fio` or `cpu-sysbench`.
Note that for network benchmarks, it is required to specify a `client` and `server`.
You can do that by encoding this into `node_id` using `@@@` as separator, i.e. `node1@@@node2` would make `node1` be the client-node and `node2` the server-node.

## Resources
[Custom Resource Definition](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)

[Kopf Sample Problem](https://kopf.readthedocs.io/en/stable/walkthrough/problem/)

