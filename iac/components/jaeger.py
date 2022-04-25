from dataclasses import dataclass
import pulumi
from pulumi_kubernetes import Provider
from pulumi_kubernetes.helm.v3 import (
    Release as HelmRelease,
    RepositoryOptsArgs
)


@dataclass
class Jaeger:
    """HelmRelease"""
    release: HelmRelease


class JaegerOperator(pulumi.ComponentResource):
    """JaeOperator component"""

    def __init__(self,
                 namespace: str,
                 provider: Provider,
                 opts: pulumi.ResourceOptions = None):

        super().__init__("kubernetes:helm-release", "jaeger")
        jaeger = self.create_resources(namespace, provider)
        self.namespace: pulumi.Output = jaeger.release.namespace

    def create_resources(self,
                         namespace: str,
                         crd_url: str,
                         provider: Provider,
                         opts: pulumi.ResourceOptions = None) -> Jaeger:

        release = HelmRelease(
            name="jaeger",
            resource_name="jaeger",
            chart="jaeger-operator",
            namespace=namespace,
            repository_opts=RepositoryOptsArgs(
                repo="https://jaegertracing.github.io/helm-charts"
            ),
            opts=pulumi.ResourceOptions(
                parent=self,
                depends_on=opts.depends_on if opts is not None else None,
                provider=provider
            )
        )

        return Jaeger(release)
