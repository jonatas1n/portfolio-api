from sqladmin import ModelView
from starlette.requests import Request
from .models import Projects
import shutil
import os

UPLOAD_FOLDER = "uploads"  # Pasta onde as imagens serão armazenadas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Criar a pasta se não existir


class ProjectAdmin(ModelView, model=Projects):
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

    async def on_model_change(self, form, model, is_created, request: Request):
        form_data = await request.form()
        file = form_data.get("images")

        if file and hasattr(file, "filename"):
            file_path = f"{UPLOAD_FOLDER}/{file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            model.images = file_path

    async def on_model_delete(self, model):
        if model.images and os.path.exists(model.images):
            os.remove(model.images)

    def _format_image(self, model):
        print(model)
        return "Sem imagem"
        if model.images:
            return f'<img src="/{model.images}" width="100"/>'
        return "Sem imagem"

    column_formatters = {"images": _format_image}
