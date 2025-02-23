import base64
from io import BytesIO
from PIL import Image
from sqladmin import ModelView
from starlette.requests import Request
from starlette.datastructures import UploadFile
from wtforms import FileField, MultipleFileField
from wtforms.validators import DataRequired
from .models import Projects
import json


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
            data["images"] = json.loads(processed_images)
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
                img_base64 = await self.resize_and_convert(image)
                processed_images.append(img_base64)

        return processed_images

    async def resize_and_convert(self, upload_file: UploadFile, fixed_width=200):
        image_bytes = await upload_file.read()
        image = Image.open(BytesIO(image_bytes))

        aspect_ratio = image.height / image.width
        new_height = int(fixed_width * aspect_ratio)
        resized_image = image.resize((fixed_width, new_height))

        buffered = BytesIO()
        resized_image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return f"data:image/png;base64,{img_base64}"
