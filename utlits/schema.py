videoSchema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "video": {"type": "string", "format": "uri"},
        "width": {"type": "string"},
        "height": {"type": "string"},
        "image": {"type": "string", "format": "uri"}
    },
    "required": ["title", "description", "video", "width", "height", "image"]
}
embed_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "maxLength": 256},
        "description": {"type": "string", "maxLength": 2048},
        "url": {"type": "string", "format": "uri"},
        "color": {"type": "integer"},
        "fields": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "maxLength": 256},
                    "value": {"type": "string", "maxLength": 1024},
                    "inline": {"type": "boolean"}
                },
                "required": ["name", "value"],
                "additionalProperties": False
            }
        },
        "image": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "format": "uri"},
                "proxy_url": {"type": "string", "format": "uri"},
                "width": {"type": "integer"},
                "height": {"type": "integer"}
            },
            "required": ["url"],
            "additionalProperties": True
        },
        "thumbnail": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "format": "uri"},
                "proxy_url": {"type": "string", "format": "uri"},
                "width": {"type": "integer"},
                "height": {"type": "integer"}
            },
            "required": ["url"],
            "additionalProperties": True
        },
        "footer": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "maxLength": 2048},
                "icon_url": {"type": "string", "format": "uri"},
                "proxy_icon_url": {"type": "string", "format": "uri"}
            },
            "required": ["text"],
            "additionalProperties": True
        }
    },
    "required": ["title", "description"],
    "additionalProperties": True
}
