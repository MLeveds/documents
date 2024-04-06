from src.api.transformers.base_transformer import BaseTransformer


class DocumentTransformer(BaseTransformer):
    def __init__(self):
        super().__init__()
        self.available_includes = []
        self.default_includes = []

    def transform(self, document):
        return {
            "id": document.id,
            "type_id": document.type_id,
            "type": document.type.name,
            "file_id": document.file_id,
            "page": document.page,
            "data": document.data,
            "link": document.link,
            "edited_link": document.edited_link,
            "created_at": document.created_at.isoformat(),
        }
