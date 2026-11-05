
from typing import Literal
from pydantic import BaseModel, Field


# Common metadata for extracted information
class ExtractedElement(BaseModel):
    name: str
    description: str = ""
    element_type: str = ""

    # Where did this information come from?
    source_text: str = ""

    # Was it explicitly stated or inferred?
    status: Literal["specified", "inferred"] = "specified"


# 1. Nodes: Where software runs or exists
class Node(ExtractedElement):
    hosting_environment: str = ""


# 2. Components: Logical software building blocks
class Component(ExtractedElement):
    responsibility: str = ""


# 3. Artifacts: Deployable software or files
class Artifact(ExtractedElement):
    artifact_format: str = ""


# 4. Dependencies: What depends on what
class Dependency(BaseModel):
    source: str
    target: str
    dependency_type: str = ""
    description: str = ""
    source_text: str = ""


# 5. Deployment specifications
class DeploymentSpecification(BaseModel):
    target: str
    specification: str
    value: str
    source_text: str = ""
    status: Literal["specified", "inferred"] = "specified"


# 6. Communication paths: How elements communicate
class CommunicationPath(BaseModel):
    source: str
    destination: str
    protocol: str = ""
    communication_type: str = ""
    direction: str = ""
    description: str = ""
    source_text: str = ""


# Visual requirements are kept separate from architecture
class VisualSpecification(BaseModel):
    layout: str = ""
    orientation: str = ""
    background: str = ""
    color_requirements: list[str] = Field(default_factory=list)
    icon_requirements: list[str] = Field(default_factory=list)
    boundary_requirements: list[str] = Field(default_factory=list)
    connector_requirements: list[str] = Field(default_factory=list)
    other_instructions: list[str] = Field(default_factory=list)


# Complete architecture extraction result
class ArchitectureModel(BaseModel):
    architecture_name: str = ""
    architecture_description: str = ""

    nodes: list[Node] = Field(default_factory=list)
    components: list[Component] = Field(default_factory=list)
    artifacts: list[Artifact] = Field(default_factory=list)
    dependencies: list[Dependency] = Field(default_factory=list)
    deployment_specifications: list[DeploymentSpecification] = Field(
        default_factory=list
    )
    communication_paths: list[CommunicationPath] = Field(default_factory=list)

    visual_specification: VisualSpecification = Field(
        default_factory=VisualSpecification
    )

    missing_information: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
