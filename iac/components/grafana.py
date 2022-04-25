import pulumi
from pulumi_kubernetes.helm.v3 import (
    Release as HelmRelease,
    RepositoryOptsArgs
)


class Grafana(pulumi.ComponentResource):

    def __init__(self,
                 namespace: str,
                 opts: pulumi.ResourceOptions = None):
        super().__init__("kubernetes:helm-release", "grafana")
        self.create_resources(namespace, opts)

    def create_resources(self,
                         namespace: str,
                         opts: pulumi.ResourceOptions = None) -> HelmRelease:

        opts.parent = self
        return HelmRelease(
            name="grafana",
            resource_name="grafana",
            chart="grafana",
            namespace=namespace,
            timeout=300,
            repository_opts=RepositoryOptsArgs(
                repo="https://grafana.github.io/helm-charts"
            ),
            opts=opts
        )
