#!/bin/bash

IMAGE_NAME="perona-operator:dev"

# delete old cluster
kind delete cluster --name benchmark-operator
# build docker image
docker build --network=host -t $IMAGE_NAME .
# create kind cluster
kind create cluster --config=ci_dev/kind-config.yml
# add docker image to kind cluster
kind --name benchmark-operator load docker-image $IMAGE_NAME
# deploy kubestone-operator
kubectl kustomize github.com/xridge/kubestone/config/default?ref=v0.5.0 | sed "s/kubestone:latest/kubestone:v0.5.0/" | kubectl create -f -
# deploy spark-operator
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
helm repo update
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
# deploy flink-operator
helm repo add flink-operator https://downloads.apache.org/flink/flink-kubernetes-operator-0.1.0/
helm repo update
helm install \
    --version 0.1.0 \
    --namespace flink-operator \
    --create-namespace \
    --set webhook.create=false \
    --set metrics.port=9999 \
    flink flink-operator/flink-kubernetes-operator
# deploy perona-operator
kubectl apply -f ci_dev/operator-deployment.yml
# deploy prometheus monitoring stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
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
kubectl apply -f ci_dev/monitoring-settings.yml