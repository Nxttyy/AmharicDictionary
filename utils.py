import re


def format_result(amh_en_text):
    # Split Amharic and English parts
    parts = amh_en_text.split("n., adj., & v.")
    amh_part = parts[0].strip()
    en_part = "n., adj., & v." + parts[1].strip() if len(parts) > 1 else ""

    # Split Amharic numbered meanings
    amh_items = re.findall(r"\d+\s*([^0-9]+)", amh_part)
    amh_formatted = [item.strip() for item in amh_items if item.strip()]

    # English part – split by numbering or grammar symbols
    en_lines = en_part.split("--")
    grammar_part = en_lines[0].strip()
    definitions = [f"--{line.strip()}" for line in en_lines[1:]]

    return amh_formatted, grammar_part, definitions


def split_english_definition(en_text):
    # Clean leading "EN:" or other prefixes
    en_text = re.sub(r"^EN:\s*", "", en_text.strip())

    # Step 1: Split at major numbering like 1, 2, 3 etc. but keep the numbers
    parts = re.split(r"(?=\b\d+\s*[a-z]?\b)", en_text)

    # Step 2: If a part has multiple sub-parts like "a ..." and "b ...", split further
    final_parts = []
    for part in parts:
        subparts = re.split(r"(?=\s*[a-z]\s)", part.strip())
        final_parts.extend([p.strip() for p in subparts if p.strip()])

    # Step 3: Filter out extremely short junk fragments
    final_parts = [p for p in final_parts if len(p) > 3]

    return final_parts
