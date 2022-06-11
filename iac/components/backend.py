import yaml
from pulumi import (
    ComponentResource,
    ResourceOptions
)
from pulumi_kubernetes.apiextensions.v1 import CustomResourceDefinition
from pulumi_kubernetes.core.v1 import Service
from pulumi_kubernetes.apps.v1 import Deployment
from typing import Any


class BackendApp(ComponentResource):
    def __init__(self,
                 name: str,
                 values_file: str,
                 opts: ResourceOptions = None):

        super.__init__("app:backend", name)
        values: Any = {}

        opts.update({"parent": self})
        with open(values_file, 'r') as file:
            values = yaml.safe_load_all(file)

            jaeger_values = [el for el in filter(
                lambda x: x.get("kind") == "Jaeger",
                values
            )][0]

            deployment_values = [el for el in filter(
                lambda x: x.get("kind") == "Deployment",
                values
            )][0]

            service_values = [el for el in filter(
                lambda x: x.get("kind") == "Service"
            )][0]

            CustomResourceDefinition(
                name,
                api_version=jaeger_values.get("apiVersion"),
                kind="Jaeger",
                metadata=jaeger_values.get("metadata"),
                opts=opts
            )

            Deployment(
                name,
                api_version=deployment_values.get("apiVersion"),
                kind="Deployment",
                metadata=deployment_values.get("metadata"),
                spec=deployment_values.get("spec"),
                opts=opts
            )

            Service(
                name,
                api_version=service_values.get("apiVersion"),
                kind="Service",
                metadata=service_values.get("metadata"),
                spec=service_values.get("spec")
            )

            file.close()
