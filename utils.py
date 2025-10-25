import re


def parse_amharic_definitions(text):
    """
    Parse Amharic definitions formatted like:
    '1 ጥሩ 2 ተስማሚ 3 ጎበዝ ...'
    """
    pattern = r"(?<!\d)(\d+)\s"  # match numbers followed by space
    matches = list(re.finditer(pattern, text))

    if not matches:
        return {"1": text.strip()}  # fallback if no numbers found

    result = {}
    for i, match in enumerate(matches):
        num = match.group(1)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        definition = text[start:end].strip()
        if definition:
            result[num] = definition

    return result


def parse_dictionary_entry(text):
    # Extract sections based on POS markers like --n. or --v.
    sections = re.finditer(r"--([a-z.]+)\s", text)
    entry = {}
    last_end = 0
    last_pos = None

    for match in sections:
        pos = match.group(1).strip(".")
        if last_pos:
            section_text = text[last_end : match.start()].strip()
            entry[last_pos] = extract_numbered_definitions(section_text)
        last_pos = pos
        last_end = match.end()

    # final section
    if last_pos:
        section_text = text[last_end:].strip()
        entry[last_pos] = extract_numbered_definitions(section_text)

    return normalize_definitions(entry)


def normalize_definitions(defs):
    """
    Convert all lists of strings into list of dicts with numbers as keys
    """
    normalized = {}
    for pos, content in defs.items():
        new_list = []
        if all(isinstance(d, str) for d in content):
            # convert strings to numbered dicts
            for i, text in enumerate(content, start=1):
                new_list.append({str(i): text})
        else:
            # already list of dicts
            new_list = content
        normalized[pos] = new_list
    return normalized


def extract_numbered_definitions(section_text):
    """Extract numbered definitions only (ignore a, b, etc.)."""
    defs = []
    numbered = list(re.finditer(r"(?<!\d)(\d+)\s", section_text))
    if not numbered:
        return [section_text.strip()]

    for i, num_match in enumerate(numbered):
        num = num_match.group(1)
        start = num_match.end()
        end = numbered[i + 1].start() if i + 1 < len(numbered) else len(section_text)
        definition_text = section_text[start:end].strip().rstrip(".")
        defs.append({num: definition_text})
    return defs
