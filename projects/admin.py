import base64
from io import BytesIO
from PIL import Image
from sqladmin import ModelView
from starlette.requests import Request
from starlette.datastructures import UploadFile
from wtforms import FileField, MultipleFileField
from wtforms.validators import DataRequired
from .models import Projects


class ProjectAdmin(ModelView, model=Projects):
    name = "Project"
    name_plural = "Projects"
    edit_template = "custom_edit.html"
    create_template = "custom_create.html"

    column_list = [
        Projects.id,
        Projects.title,
        Projects.technologies,
        Projects.description,
        Projects.images,
    ]

    column_searchable_list = [Projects.title]
    column_sortable_list = [Projects.id]

    form_columns = ["title", "technologies", "description", "images"]
    form_overrides = {"images": MultipleFileField}
    form_args = {
        "images": {
            "label": "Upload de Imagens",
            "validators": [DataRequired()],
        }
    }

    async def insert_model(self, request: Request, data: dict):
        if "images" in request.form:
            uploaded_files = await request.form.getlist("images")
            data["images"] = await self.process_images(uploaded_files)
        return await super().insert_model(request, data)

    async def update_model(self, request: Request, pk: int, data: dict):
        if "images" in request.form:
            uploaded_files = await request.form.getlist("images")
            data["images"] = await self.process_images(uploaded_files)
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

        # Mantém a proporção
        aspect_ratio = image.height / image.width
        new_height = int(fixed_width * aspect_ratio)
        resized_image = image.resize((fixed_width, new_height))

        buffered = BytesIO()
        resized_image.save(buffered, format="PNG")
        img_base64 = base64

        return f"data:image/png;base64,{img_base64}"
