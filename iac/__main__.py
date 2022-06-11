from components.jaeger import Jaeger
from components.backend import BackendApp
from components.frontend import FrontEndApp
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

    Jaeger(
        name="jaeger",
        file_name="components/values/jaeger.yaml"
    )

    FrontEndApp(
        name="frontend-app",
        file_name="components/values/frontend.yaml"
    )

    BackendApp(
        name="backend-app",
        file_name="components/values/backend.yaml"
    )
