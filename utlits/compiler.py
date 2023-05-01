import typing as t
import json
from handler.types import Embed


def compiler_json_data(data: str) -> t.Union[bool, dict]:
    # Remove prefix and suffix
    if data.startswith("```json") or data.startswith("```"):
        data = data.removeprefix("```json")
        data = data.removeprefix("```")
    if data.endswith("```"):
        data = data.removesuffix("```")
    
    # Check if data is a json & it can be a embed
    try:
        Embed.from_dict(json.loads(data))
    except:
        return False
    return json.loads(data)
