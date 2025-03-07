from sqladmin import ModelView
from starlette.requests import Request
from starlette.datastructures import UploadFile
from wtforms import MultipleFileField
from .models import Projects
import json
from utils.image import resize_and_convert


class ProjectAdmin(ModelView, model=Projects):
    name = "Project"
    name_plural = "Projects"
    edit_template = "custom_edit.html"
    create_template = "custom_create.html"

    column_list = [
        Projects.id,
        Projects.title,
        Projects.technologies,
        Projects.images,
    ]

    column_searchable_list = [Projects.title]
    column_sortable_list = [Projects.id]

    form_columns = ["title", "technologies", "description", "images", "link"]
    form_overrides = {"images": MultipleFileField}
    form_args = {
        "images": {
            "label": "Upload de Imagens",
            "validators": [],
        }
    }

    async def on_model_get(self, model):
        if isinstance(model.images, str):
            try:
                model.images = json.loads(model.images)
            except json.JSONDecodeError:
                model.images = []

    async def insert_model(self, request: Request, data: dict):
        images = data.pop("images", None)
        if len(images) > 0 and images[0].size > 0:
            processed_images = await self.process_images(images)
            data["images"] = json.dumps(processed_images)
        return await super().insert_model(request, data)

    async def update_model(self, request: Request, pk: int, data: dict):
        images = data.pop("images", None)
        if len(images) > 0 and images[0].size > 0:
            processed_images = await self.process_images(images)
            data["images"] = json.dumps(processed_images)
        return await super().update_model(request, pk, data)

    async def process_images(self, images):
        processed_images = []
        for image in images:
            if isinstance(image, UploadFile):
                img_base64 = await resize_and_convert(image)
                processed_images.append(img_base64)

        return processed_images
