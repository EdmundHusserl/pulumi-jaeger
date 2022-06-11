import pulumi
from pulumi_kubernetes.helm.v3 import (
    Release as HelmRelease,
    RepositoryOptsArgs
)


class CertManager(pulumi.ComponentResource):

    def __init__(self,
                 namespace: str,
                 opts: RepositoryOptsArgs = None):
        super().__init__("kubernetes:helm-release", "cert-manager")
        self.create_resources(namespace, opts)

    def create_resources(self,
                         namespace: str,
                         opts: pulumi.ResourceOptions = None) -> HelmRelease:

        opts.parent = self
        return HelmRelease(
            name="cert-manager",
            resource_name="cert-manager",
            chart="cert-manager",
            namespace=namespace,
            values={
                "installCRDs": True
            },
            timeout=300,
            repository_opts=RepositoryOptsArgs(
                repo="https://charts.jetstack.io"
            ),
            version="v1.7.1",
            opts=opts
        )
