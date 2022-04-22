from multiprocessing import parent_process
import pulumi
from pulumi_kubernetes.helm.v3 import (
    Release as HelmRelease,
    RepositoryOptsArgs
)
from pulumi_kubernetes import Provider
from pulumi_kubernetes.core.v1 import Namespace
from dataclasses import dataclass


@dataclass
class Jaeger:
    release: HelmRelease


class JaegerOperator(pulumi.ComponentResource):
    
    def __init__(self, namespace: str, crd_url: str, provider: Provider):
        super().__init__("kubernetes:operator", "jaeger")
        jaeger = self.create_resources(namespace, crd_url, provider)
        self.namespace: pulumi.Output = jaeger.release.namespace 

    def create_resources(self, 
                         namespace: str, 
                         crd_url: str, 
                         provider: Provider) -> Jaeger:
        
        
        cert_manager = HelmRelease(
            name="cert-manager",
            resource_name="cert-manager",
            chart="cert-manager",
            namespace=namespace,
            create_namespace=True,
            timeout=300,
            repository_opts=RepositoryOptsArgs(
                repo="https://charts.jetstack.io"
            ),
            version="v1.7.1",
            opts=pulumi.ResourceOptions(
                parent=self
            )
        )

        release = HelmRelease(
            name="jaeger",
            resource_name="jaeger",
            chart="jaeger-operator",
            namespace=namespace,
            repository_opts=RepositoryOptsArgs(repo=crd_url),
            opts=pulumi.ResourceOptions(
                parent=self,
                depends_on=cert_manager,
                provider=provider
            )
        )
        
        return Jaeger(release)
