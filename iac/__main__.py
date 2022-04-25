import pulumi
from components.jaeger import JaegerOperator
from components.cert_manager import CertManager
from components.grafana import Grafana
from pulumi_kubernetes.core.v1 import (
    Namespace,
    NamespaceInitArgs
)
from pulumi_kubernetes import Provider as K8sProvider

# Config
KUBE_CONFIG = "k3s.yaml"
CLUSTER_NAME = CONTEXT_NAME = "default"


with open(KUBE_CONFIG, "r") as kubeconfig:
    k8s_provider = K8sProvider(
        resource_name="k8s-provider",
        kubeconfig=kubeconfig.read(),
        cluster=CLUSTER_NAME,
        context=CONTEXT_NAME
    )
    kubeconfig.close()


observability = Namespace(
    "observability",
    args=NamespaceInitArgs(metadata={"name": "observability"}),
    opts=pulumi.ResourceOptions(
        provider=k8s_provider
    )
)

cert_manager = CertManager(
    "observability",
    opts=pulumi.ResourceOptions(
        provider=k8s_provider,
        depends_on=[observability]
    )
)
jaeger = JaegerOperator(
    "observability",
    opts=pulumi.ResourceOptions(
        provider=k8s_provider,
        depends_on=[observability, cert_manager]
    )
)
grafana = Grafana(
    "observability",
    opts=pulumi.ResourceOptions(
        provider=k8s_provider,
        depends_on=[observability]
    )
)
