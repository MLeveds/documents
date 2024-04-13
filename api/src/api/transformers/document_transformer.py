from src.api.transformers.base_transformer import BaseTransformer
import json


class DocumentTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.available_includes = []
        self.default_includes = []

    def transform(self, document):
        return {
            "id": document.id,
            "type_id": document.type_id,
            "type": document.type.name if document.type else None,
            "confidence": document.confidence,
            "status_id": document.status_id,
            "status": document.status.name,
            "file_id": document.file_id,
            "page": document.page,
            "data": json.loads(document.data) if document.data else None,
            "link": document.link,
            "edited_link": document.edited_link,
            "created_at": document.created_at.isoformat(),
        }
