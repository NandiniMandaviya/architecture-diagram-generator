
from pathlib import Path

from extractor import extract_architecture
from diagram_generator import generate_mermaid


def main():
    # Step 1: Read input
    sample_path = Path("samples/sample_input.txt")

    architecture_description = sample_path.read_text(
        encoding="utf-8"
    )

    # Step 2: Extract architecture using Azure LLM
    print("\n[1/4] Extracting architecture information...")

    architecture = extract_architecture(
        architecture_description
    )

    print("Extraction completed.")

    # Step 3: Save structured architecture JSON
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "extracted_architecture.json"

    json_path.write_text(
        architecture.model_dump_json(indent=4),
        encoding="utf-8",
    )

    print(f"JSON saved: {json_path}")

    # Step 4: Generate Mermaid diagram
    print("\n[2/4] Generating Mermaid diagram...")

    mermaid_code = generate_mermaid(architecture)

    mermaid_path = output_dir / "architecture_diagram.mmd"

    mermaid_path.write_text(
        mermaid_code,
        encoding="utf-8",
    )

    print(f"Mermaid file saved: {mermaid_path}")

    print("\n[3/4] Architecture extraction and diagram generation completed.")

    print("\n[4/4] Ready for diagram rendering.")

    print("\nGenerated Mermaid code:\n")
    print(mermaid_code)


if __name__ == "__main__":
    main()
