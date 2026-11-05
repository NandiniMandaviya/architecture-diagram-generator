
EXTRACTION_PROMPT = """
You are an architecture analysis assistant.

Your task is to analyse a natural-language software
architecture description and extract its architecture information.

Extract the following six categories:

1. NODES
   Physical or virtual environments where software runs.
   Examples: Virtual Machines, Containers, Cloud Servers,
   Kubernetes Clusters.

2. COMPONENTS
   Logical software building blocks.
   Examples: Applications, APIs, Microservices,
   Authentication Services.

3. ARTIFACTS
   Software deliverables and deployable files.
   Examples: Executables, JAR files, Docker Images,
   Python Packages, Configuration Files.

4. DEPENDENCIES
   Relationships describing which elements rely on other
   elements to function.

5. DEPLOYMENT SPECIFICATIONS
   Configuration and environment details.
   Examples: Operating System, Runtime, Programming Language,
   Framework Version, CPU, Memory, Deployment Region.

6. COMMUNICATION PATHS
   Connections and information exchange between elements.
   Examples: REST, HTTPS, SOAP, NFS, SMB,
   Message Queues and Database Connections.

ADDITIONAL EXTRACTION RULES:

- Preserve explicitly stated information.
- Do not invent technologies, services or infrastructure.
- Distinguish explicit information from reasonable inferences.
- Record the original text supporting each extracted element.
- If information is unavailable, leave the field empty
  or record it under missing_information.
- Do not treat an unspecified value as an architectural default.
- Extract dependencies and communication paths separately.
- Identify the source and destination of relationships.
- Extract visual instructions separately from architecture.

INPUT:
{architecture_description}

Return the result using the supplied ArchitectureModel schema.

SCHEMA COMPLIANCE RULES:

- Follow the supplied JSON schema exactly.
- Use the exact field names specified in the schema.
- Every required field must be present.
- Do not replace a required field with a differently named field.
- For DeploymentSpecification:
  - target identifies the architecture element.
  - specification identifies the configuration type.
  - value contains the specified configuration value.
- For CommunicationPath:
  - source identifies the originating element.
  - destination identifies the receiving element.
- If a string value is unknown, use an empty string.
- If a list has no applicable entries, return an empty list.
"""
