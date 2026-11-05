
import os

from dotenv import load_dotenv
from openai import AzureOpenAI


load_dotenv()


def create_azure_client() -> AzureOpenAI:
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    if not endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT is missing.")

    if not api_key:
        raise ValueError("AZURE_OPENAI_API_KEY is missing.")

    if not api_version:
        raise ValueError("AZURE_OPENAI_API_VERSION is missing.")

    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
    )


def get_deployment_name() -> str:
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    if not deployment_name:
        raise ValueError("AZURE_OPENAI_DEPLOYMENT is missing.")

    return deployment_name
