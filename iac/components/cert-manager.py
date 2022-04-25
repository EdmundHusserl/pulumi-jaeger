import pulumi
from pulumi_kubernetes.helm.v3 import (
    Release as HelmRelease,
    RepositoryOptsArgs
)
from pulumi_kubernetes import Provider


class CertManager(pulumi.ComponentResource):

    def __init__(self, namespace: str, k8s_provider: Provider):
        super().__init__("kubernetes:helm-release", "cert-manager")
        self.create_resources(namespace, k8s_provider)

    def create_resources(self,
                         namespace: str,
                         k8s_provider: Provider) -> HelmRelease:

        return HelmRelease(
            name="cert-manager",
            resource_name="cert-manager",
            chart="cert-manager",
            namespace=namespace,
            timeout=300,
            repository_opts=RepositoryOptsArgs(
                repo="https://charts.jetstack.io"
            ),
            version="v1.7.1",
            opts=pulumi.ResourceOptions(
                parent=self,
                provider=k8s_provider
            )
        )
