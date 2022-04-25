import pulumi
from components.jaeger import (
    JaegerOperator,
    CertManager
)
from pulumi_kubernetes import (
    Namespace,
    Grafana,
    Provider as K8sProvider,
)

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


observability = Namespace("observability",
                          opts=pulumi.ResourceOptions(
                              provider=k8s_provider
                          ))

cert_manager = CertManager("observability", k8s_provider)
jaeger = JaegerOperator(
    "observability",
    k8s_provider,
    opts=pulumi.ResourceOptions(
        depends_on=[
            observability.id,
            cert_manager
        ]
    )
)
grafana = Grafana("observabiity", k8s_provider)
