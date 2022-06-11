from dataclasses import dataclass
import pulumi
from pulumi_kubernetes.helm.v3 import (
    Release as HelmRelease,
    RepositoryOptsArgs
)
from typing import List


@dataclass
class Jaeger:
    """HelmRelease"""
    releases: List[HelmRelease]
    namespace: pulumi.Output[str]


class JaegerOperator(pulumi.ComponentResource):
    """JaegerOperator component"""

    def __init__(self,
                 namespace: str,
                 opts: pulumi.ResourceOptions = None):

        super().__init__("kubernetes:helm-release", "jaeger")
        jaeger = self.create_resources(namespace, opts)
        self.namespace: pulumi.Output = jaeger.namespace

    def create_resources(self,
                         namespace: str,
                         opts: pulumi.ResourceOptions = None) -> Jaeger:

        opts.parent = self

        app = HelmRelease(
            name="jaeger",
            resource_name="jaeger",
            version="0.56.1",
            chart="jaeger",
            namespace=namespace,
            values={"installCRDs": True},
            repository_opts=RepositoryOptsArgs(
                repo="https://jaegertracing.github.io/helm-charts"
            ),
            opts=opts
        )

        operator = HelmRelease(
            name="jaeger-operator",
            resource_name="jaeger-operator",
            chart="jaeger-operator",
            version="2.30.0",
            namespace=namespace,
            values={"installCRDs": True},
            repository_opts=RepositoryOptsArgs(
                repo="https://jaegertracing.github.io/helm-charts"
            ),
            opts=opts
        )

        return Jaeger(
            releases=[app, operator],
            namespace=app.namespace
        )
