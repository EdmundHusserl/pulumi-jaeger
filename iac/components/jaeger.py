from dataclasses import dataclass
import pulumi
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
                 opts: pulumi.ResourceOptions = None):

        super().__init__("kubernetes:helm-release", "jaeger")
        jaeger = self.create_resources(namespace, opts)
        self.namespace: pulumi.Output = jaeger.release.namespace

    def create_resources(self,
                         namespace: str,
                         opts: pulumi.ResourceOptions = None) -> Jaeger:

        opts.parent = self
        release = HelmRelease(
            name="jaeger",
            resource_name="jaeger",
            chart="jaeger-operator",
            namespace=namespace,
            repository_opts=RepositoryOptsArgs(
                repo="https://jaegertracing.github.io/helm-charts"
            ),
            opts=opts
        )

        return Jaeger(release)
