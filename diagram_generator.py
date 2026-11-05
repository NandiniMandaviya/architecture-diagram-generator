
import re

from models import ArchitectureModel


def create_node_id(name: str) -> str:
    """Create a valid Mermaid identifier."""
    identifier = re.sub(r"[^a-zA-Z0-9_]", "_", name)

    if not identifier or identifier[0].isdigit():
        identifier = f"element_{identifier}"

    return identifier


def clean_label(value: str) -> str:
    """Clean text for use inside Mermaid labels."""
    return (
        value.replace('"', "'")
        .replace("\n", " ")
        .replace("|", "/")
    )


def generate_mermaid(architecture: ArchitectureModel) -> str:
    """Convert an ArchitectureModel into Mermaid flowchart syntax."""

    lines = ["flowchart LR"]

    elements = {}

    # 1. Add nodes
    for node in architecture.nodes:
        elements[node.name] = {
            "id": create_node_id(node.name),
            "type": "node",
        }

    # 2. Add components
    for component in architecture.components:
        elements[component.name] = {
            "id": create_node_id(component.name),
            "type": "component",
        }

    # 3. Add artifacts
    for artifact in architecture.artifacts:
        elements[artifact.name] = {
            "id": create_node_id(artifact.name),
            "type": "artifact",
        }

    # 4. Add deployment information to element labels
    deployment_info = {}

    for spec in architecture.deployment_specifications:
        deployment_info.setdefault(spec.target, []).append(
            f"{spec.specification}: {spec.value}"
        )

    # 5. Generate element definitions
    for name, element in elements.items():
        label = clean_label(name)

        specifications = deployment_info.get(name, [])

        if specifications:
            label += "<br/>" + "<br/>".join(
                clean_label(item) for item in specifications
            )

        element_id = element["id"]

        if element["type"] == "node":
            lines.append(f'    {element_id}["{label}"]')

        elif element["type"] == "component":
            lines.append(f'    {element_id}("{label}")')

        else:
            lines.append(f'    {element_id}[["{label}"]]')

    # 6. Add external communication endpoints
    for path in architecture.communication_paths:
        for endpoint in [path.source, path.destination]:

            if endpoint not in elements:
                external_id = create_node_id(endpoint)

                elements[endpoint] = {
                    "id": external_id,
                    "type": "external",
                }

                lines.append(
                    f'    {external_id}(["{clean_label(endpoint)}"])'
                )

    # 7. Add dependencies
    for dependency in architecture.dependencies:
        source = elements.get(dependency.source)
        target = elements.get(dependency.target)

        if source and target:
            label = clean_label(dependency.dependency_type)

            lines.append(
                f'    {source["id"]} -. "{label}" .-> {target["id"]}'
            )

    # 8. Add communication paths
    for path in architecture.communication_paths:
        source = elements.get(path.source)
        target = elements.get(path.destination)

        if source and target:
            labels = [
                path.communication_type,
                path.protocol,
            ]

            label = " / ".join(
                clean_label(item)
                for item in labels if item
            )

            if path.direction == "bidirectional":
                arrow = "<-->"

            else:
                arrow = "-->"

            if label:
                lines.append(
                    f'    {source["id"]} {arrow}|"{label}"| {target["id"]}'
                )
            else:
                lines.append(
                    f'    {source["id"]} {arrow} {target["id"]}'
                )

    return "\n".join(lines)
