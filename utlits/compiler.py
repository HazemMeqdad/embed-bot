import json;
import re;
import jsonschema;
from typing import List, Union;
from .schema import videoSchema, embed_schema;

def video_compiler_json(strings: List[str]) -> Union[bool, dict]:
    combined_string = ''.join(strings)
    start = combined_string.find("{")
    end = combined_string.rfind("}")
    if start != -1 and end != -1 and end > start:
        json_string = combined_string[start:end+1]
        json_string = re.sub(r',\s*}', '}', json_string)
        json_string = re.sub(r'"([^"]*)"\s*:\s*"(https?://[^"]+)"', r'"\1": "\2"', json_string)
        json_string = re.sub(r'"([^"]*)"\s*:\s*"([^"]+)Z"', r'"\1": "\2"', json_string)
        try:
            json_data = json.loads(json_string)
            jsonschema.validate(instance=json_data, schema=videoSchema)
            return json_data
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", str(e))
            return False
        except jsonschema.exceptions.ValidationError as e:
            print("ValidationError", str(e))
            return False
        except ValueError as e:
            print("ValueError:", str(e))
            return False
    else:
        return False    


def json_compiler(strings: List[str], schema=None) -> Union[bool, dict]:
    combined_string = ''.join(strings);
    start = combined_string.find("{");
    end = combined_string.rfind("}");
    if start != -1 and end != -1 and end > start: 
        json_string = combined_string[start:end+1];
        json_string = re.sub(r',\s*}', '}', json_string);
        json_string = re.sub(r'"([^"]*)"\s*:\s*"(https?://[^"]+)"', r'"\1": "\2"', json_string);
        json_string = re.sub(r'"([^"]*)"\s*:\s*"([^"]+)Z"', r'"\1": "\2"', json_string);
        try:
            json_data = json.loads(json_string);
            if schema:
                jsonschema.validate(instance=json_data, schema=schema);
                return json_data
            else: 
                jsonschema.validate(instance=json_data, schema=embed_schema);
                return json_data
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", str(e));
            return False
        except ValueError as e:
            print("ValueError:", str(e));
            return False
        except jsonschema.exceptions.ValidationError as e:
            print("ValidationError", str(e));
            return False    
    return False

