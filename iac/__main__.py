import pulumi
from components.jaeger import JaegerOperator
from components.cert_manager import CertManager
from components.grafana import Grafana
from pulumi_kubernetes.core.v1 import (
    Namespace,
    NamespaceInitArgs
)
from pulumi_kubernetes import Provider as K8sProvider
from os import environ

# Config
KUBE_CONFIG = "k3s.yaml"
CLUSTER_NAME = CONTEXT_NAME = "default"
OBSERVABILITY = "observability"
environ["KUBE_CONFIG"] = KUBE_CONFIG


with open(KUBE_CONFIG, "r") as kubeconfig:
    k8s_provider = K8sProvider(
        resource_name="k8s-provider",
        kubeconfig=kubeconfig.read(),
        cluster=CLUSTER_NAME,
        context=CONTEXT_NAME
    )
    kubeconfig.close()


observability_namespace = Namespace(
    OBSERVABILITY,
    args=NamespaceInitArgs(metadata={"name": "observability"}),
    opts=pulumi.ResourceOptions(
        provider=k8s_provider
    )
)

cert_manager = CertManager(
    OBSERVABILITY,
    opts=pulumi.ResourceOptions(
        provider=k8s_provider,
        depends_on=[observability_namespace]
    )
)
JaegerOperator(
    OBSERVABILITY,
    opts=pulumi.ResourceOptions(
        provider=k8s_provider,
        depends_on=[observability_namespace, cert_manager]
    )
)
Grafana(
    OBSERVABILITY,
    opts=pulumi.ResourceOptions(
        provider=k8s_provider,
        depends_on=[observability_namespace]
    )
)
