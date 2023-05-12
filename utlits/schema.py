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