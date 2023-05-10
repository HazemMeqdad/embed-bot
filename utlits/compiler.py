import json
from handler.types import Embed
import re
from typing import List, Union
import re
import json
from typing import List, Union

#a better compiler that can get all the json data from strings so you don't need a json code block to get a json data 

def compiler_json_data(strings: List[str]) -> Union[bool, dict]:
    combined_string = ''.join(strings)
    start = combined_string.find("{")
    end = combined_string.rfind("}")
    
    if start != -1 and end != -1 and end > start:
        json_string = combined_string[start:end+1]
        json_string = re.sub(r',\s*}', '}', json_string)
        json_string = re.sub(r'"([^"]*)"\s*:\s*"(https?://[^"]+)"', r'"\1": "\2"', json_string)
        json_string = re.sub(r'"([^"]*)"\s*:\s*"([^"]+)Z"', r'"\1": "\2"', json_string)
        print(json_string)
        try:
            json_data = json.loads(json_string)
            Embed.from_dict(json_data)
            return json_data
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", str(e))
            return False
        except ValueError as e:
            print("ValueError:", str(e))
            return False
    else:
        return False

## a better compiler that use a RegExp to get the embed  but it's need a better regexp

# def compiler_json_data(strings: List[str]) -> Union[bool, dict]:
#     combined_string = ''.join(strings)
#     pattern = r"\{[^{}]*\}"
#     match = re.search(pattern, combined_string, re.DOTALL)

#     if match:
#         json_string = match.group()
#         json_string = re.sub(r',\s*}', '}', json_string)
#         json_string = re.sub(r'"([^"]*)"\s*:\s*"(https?://[^"]+)"', r'"\1": "\2"', json_string)
#         try:
#             json_data = json.loads(json_string)
#             Embed.from_dict(json_data)
#             return json_data
#         except json.JSONDecodeError as e:
#             print("JSONDecodeError:", str(e))
#             return False
#         except ValueError as e:
#             print("ValueError:", str(e))
#             return False
#     else:
#         return False


# def compiler_json_data(data: str) -> t.Union[bool, dict]:
#     # Remove prefix and suffix
#     if data.startswith("```json") or data.startswith("```"):
#         data = data.removeprefix("```json")
#         data = data.removeprefix("```")
#     if data.endswith("```"):
#         data = data.removesuffix("```")
    
#     # Check if data is a json & it can be a embed
#     # try:
#     #     Embed.from_dict(json.loads(data))
#     # except:
#     #     return False
#     return json.loads(data)
