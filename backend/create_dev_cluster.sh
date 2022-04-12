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
# deploy kubestone
kubectl kustomize github.com/xridge/kubestone/config/default?ref=v0.5.0 | sed "s/kubestone:latest/kubestone:v0.5.0/" | kubectl create -f -
# deploy operator
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
    --set prometheus.service.type=NodePort \
    --set prometheus.service.nodePort=30090 \
    --set prometheus.service.targetPort=9090 \
    --set prometheus.service.port=9090 \
    prometheus prometheus-community/kube-prometheus-stack
