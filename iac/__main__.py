import pulumi
from components.jaeger import JaegerOperator
from pulumi_kubernetes import Provider as K8sProvider


# Config
KUBE_CONFIG = "k3s.yaml"  
CLUSTER_NAME = CONTEXT_NAME = "default"


with open(KUBE_CONFIG, "r") as kubeconfig:
    k8s_provider = K8sProvider(
        resource_name="k8s-provider",
        kubeconfig=kubeconfig.read()
    )
    kubeconfig.close()

jaeger = JaegerOperator(
    "observability",
    "https://jaegertracing.github.io/helm-charts",
    k8s_provider
)


pulumi.export("namespace", jaeger.namespace)