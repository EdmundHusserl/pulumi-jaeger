import pulumi
from pulumi_kubernetes.helm.v3 import (
    Release as HelmRelease,
    RepositoryOptsArgs
)
from pulumi_kubernetes import Provider


class Grafana(pulumi.ComponentResource):

    def __init__(self, namespace: str, k8s_provider: Provider):
        super().__init__("kubernetes:helm-release", "grafana")
        self.create_resource(namespace, k8s_provider)

    def self_create(self,
                    namespace: str, k8s_provider: Provider) -> HelmRelease:

        return HelmRelease(
            name="grafana",
            resource_name="grafana",
            chart="grafana",
            namespace=namespace,
            timeout=300,
            repository_opts=RepositoryOptsArgs(
                repo="https://grafana.github.io/helm-charts"
            ),
            version="v1.7.1",
            opts=pulumi.ResourceOptions(
                parent=self,
                provider=k8s_provider
            )
        )
