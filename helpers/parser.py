import re
import json


MATCH_SELECTOR = re.compile(r'```json\s*(\[\s*"[^"]*"(?:\s*,\s*"[^"]*")*\s*])\s*```')


def parse_selector_response(response: str) -> list[str]:
    match = MATCH_SELECTOR.search(response)
    if match:
        return json.loads(match.group(1))
    else:
        raise ValueError("Invalid selector response format")


