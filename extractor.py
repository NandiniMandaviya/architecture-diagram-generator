
import json

from openai import APIError

from llm_client import create_azure_client, get_deployment_name
from models import ArchitectureModel
from prompts import EXTRACTION_PROMPT


def extract_architecture(
    architecture_description: str,
) -> ArchitectureModel:
    """
    Extract architecture information from a natural-language
    description using the Azure-hosted LLM.

    Returns:
        ArchitectureModel: Validated architecture information.
    """

    # 1. Initialize Azure client and deployment
    client = create_azure_client()
    deployment = get_deployment_name()

    # 2. Generate the JSON schema from the Pydantic model
    schema = ArchitectureModel.model_json_schema()

    # 3. Construct the extraction prompt
    prompt = EXTRACTION_PROMPT.format(
        architecture_description=architecture_description
    )

    prompt += f"""

IMPORTANT: Follow this JSON schema exactly.

JSON SCHEMA:
{json.dumps(schema, indent=2)}

SCHEMA COMPLIANCE RULES:
- Use the exact field names specified in the schema.
- Include every required field.
- Do not introduce additional fields.
- Do not replace required fields with differently named fields.
- For unknown string values, use an empty string.
- For empty collections, use an empty list.
- Preserve explicitly stated architecture information.
- Do not invent technologies or infrastructure.
- Return only a valid JSON object.
- Do not include Markdown code fences or explanations.
"""

    # 4. Send request to Azure-hosted model
    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert software architecture "
                        "analysis assistant. Extract architecture "
                        "information accurately and follow the "
                        "provided JSON schema."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
        )

    except APIError as error:
        raise RuntimeError(
            f"Azure LLM request failed: {error}"
        ) from error

    # 5. Retrieve model response
    result = response.choices[0].message.content

    if not result:
        raise ValueError("The LLM returned an empty response.")

    result = result.strip()

    # 6. Handle Markdown code fences if present
    if result.startswith("```"):
        result = result.removeprefix("```json")
        result = result.removeprefix("```")
        result = result.removesuffix("```").strip()

    # 7. Parse JSON
    try:
        extracted_data = json.loads(result)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"The LLM returned invalid JSON: {error}\n"
            f"Raw response:\n{result}"
        ) from error

    # 8. Validate using Pydantic
    try:
        architecture = ArchitectureModel.model_validate(
            extracted_data
        )

    except Exception as error:
        raise ValueError(
            f"The LLM response does not match "
            f"ArchitectureModel:\n{error}\n"
            f"Raw response:\n{json.dumps(extracted_data, indent=2)}"
        ) from error

    return architecture
