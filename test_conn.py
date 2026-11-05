
from llm_client import create_azure_client, get_deployment_name


def main():
    client = create_azure_client()
    deployment = get_deployment_name()

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": "Reply with exactly: Azure connection successful",
            },
        ],
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
