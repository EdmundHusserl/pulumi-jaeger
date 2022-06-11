import yaml
from pulumi import (
    ComponentResource,
    ResourceOptions
)
from pulumi_kubernetes.apps.v1 import Deployment


class FrontEndApp(ComponentResource):
    def __init__(self,
                 name: str,
                 file_name: str,
                 opts: ResourceOptions = None):

        super.__init__("app:frontend", name)
        opts.update({"parent": self})

        with open(file_name, "r") as file:
            props = yaml.safe_load(file)

            Deployment(
                name,
                api_version="apps/v1",
                kind="Deployment",
                metadata=props.get("metadata"),
                spec=props.get("spec"),
                opts=opts
            )
            file.close()
