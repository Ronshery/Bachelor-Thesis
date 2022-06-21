#!/bin/bash

IMAGE_NAME="perona-operator:dev"

printf "\n##### Delete old Kind cluster, if any...\n"
kind delete cluster --name benchmark-operator &>/dev/null

printf "\n##### Build Docker Image...\n"
docker build --network=host -t $IMAGE_NAME . &>/dev/null

printf "\n##### Create Kind cluster...\n"
NODE_NUM=3
CONFIG_FILE=ci_dev/kind-config.yml
KIND_IMAGE=kindest/node:v1.21.10@sha256:84709f09756ba4f863769bdcabe5edafc2ada72d3c8c44d6515fc581b66b029c
DATA_DIR=""

cat <<EOF > ${CONFIG_FILE}
kind: Cluster
name: benchmark-operator
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
# the control plane node config
- role: control-plane
  image: ${KIND_IMAGE}
  extraPortMappings:
  # perona operator
  - containerPort: 31313
    hostPort: 8000
    listenAddress: "127.0.0.1"
    protocol: TCP
  # prometheus
  - containerPort: 30090
    hostPort: 9090
    listenAddress: "127.0.0.1"
    protocol: TCP
  # dashboard
  - containerPort: 31113
    hostPort: 8001
    listenAddress: "127.0.0.1"
    protocol: TCP
  # chaos dashboard
  - containerPort: 31333
    hostPort: 8333
    listenAddress: "127.0.0.1"
    protocol: TCP
  extraMounts:
  - hostPath: ${DATA_DIR}/perona-cluster-plane/
    containerPath: /var/local-path-provisioner
    readOnly: false
# the workers
EOF

for ((i=1;i<NODE_NUM;i++))
do
    cat <<EOF >>  ${CONFIG_FILE}
- role: worker
  image: ${KIND_IMAGE}
  extraMounts:
  - hostPath: ${DATA_DIR}/perona-cluster-worker-${i}/
    containerPath: /var/local-path-provisioner
    readOnly: false
EOF
done

kind create cluster --config=${CONFIG_FILE}
kind --name benchmark-operator load docker-image $IMAGE_NAME &>/dev/null

printf "\n##### Deploy Kubestone Operator...\n"
kubectl kustomize github.com/xridge/kubestone/config/default?ref=v0.5.0 | sed "s/kubestone:latest/kubestone:v0.5.0/" | kubectl create -f -

printf "\n##### Deploy Spark Operator...\n"
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator &>/dev/null
helm repo update &>/dev/null
helm install \
    --version 1.1.20 \
    --namespace spark-operator \
    --create-namespace \
    --set rbac.create=true \
    --set rbac.createClusterRole=true \
    --set rbac.createRole=true \
    --set serviceAccounts.spark.create=true \
    --set serviceAccounts.spark.name=spark \
    --set serviceAccounts.sparkoperator.create=true \
    --set serviceAccounts.sparkoperator.name=spark-operator \
    spark spark-operator/spark-operator

printf "\n##### Deploy Flink Operator...\n"
helm repo add flink-operator https://downloads.apache.org/flink/flink-kubernetes-operator-0.1.0/ &>/dev/null
helm repo update &>/dev/null
helm install \
    --version 0.1.0 \
    --namespace flink-operator \
    --create-namespace \
    --set webhook.create=false \
    --set metrics.port=9999 \
    flink flink-operator/flink-kubernetes-operator

printf "\n##### Deploy Perona Operator...\n"
kubectl apply -f ci_dev/operator-deployment.yml

printf "\n##### Deploy Prometheus Operator and Monitoring Stack...\n"
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts &>/dev/null
helm repo update &>/dev/null
helm install \
    --version 34.9.0 \
    --namespace prometheus \
    --create-namespace \
    --set grafana.enabled=false \
    --set alertmanager.enabled=false \
    --set prometheus.serviceMonitor.selfMonitor=false \
    --set prometheus.service.type=NodePort \
    --set prometheus.service.nodePort=30090 \
    --set prometheus.service.targetPort=9090 \
    --set prometheus.service.port=9090 \
    prometheus prometheus-community/kube-prometheus-stack
# customize monitoring settings
kubectl apply -f ci_dev/monitoring-settings.yml &>/dev/null

printf "\n##### Deploy Chaos Mesh...\n"
helm repo add chaos-mesh https://charts.chaos-mesh.org &>/dev/null
helm repo update &>/dev/null
kubectl create ns chaos-testing
helm install \
    --version 2.2.0 \
    --namespace chaos-testing \
    --set chaosDaemon.runtime=containerd \
    --set chaosDaemon.socketPath=/run/containerd/containerd.sock \
    --set dashboard.create=true \
    --set dashboard.securityMode=false \
    --set dashboard.service.type=NodePort \
    --set dashboard.service.nodePort=31333 \
    chaos-mesh chaos-mesh/chaos-mesh
# use 'wait' to check for Available status in .status.conditions[]
kubectl wait deployment -n chaos-testing chaos-controller-manager --for condition=Available=True --timeout=120s
# create chaos schedules
kubectl apply -f ci_dev/chaos-stress-cpu.yml

printf "\n##### Deploy Kubernetes Dashboard...\n"
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/ &>/dev/null
helm repo update &>/dev/null
helm install \
    --version 5.4.1 \
    --namespace kubernetes-dashboard \
    --create-namespace \
    --set service.type=NodePort \
    --set service.nodePort=31113 \
    --set protocolHttp=true \
    --set "extraArgs={--enable-insecure-login}" \
    kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard
# create serviceaccount and permissions
kubectl apply -f ci_dev/dashboard-settings.yml &>/dev/null
SECRET_NAME=$(kubectl -n kubernetes-dashboard get sa/admin-user -o jsonpath="{.secrets[0].name}")
SECRET_TOKEN=$(kubectl -n kubernetes-dashboard get secret $SECRET_NAME -o go-template="{{.data.token | base64decode}}")
printf "\nLogin-Token for dashboard (http://localhost:8001/#/login): $SECRET_TOKEN"
