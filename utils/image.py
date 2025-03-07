import base64
from io import BytesIO
from PIL import Image
from starlette.datastructures import UploadFile

FIXED_WIDTH = 920

async def resize_and_convert(upload_file: UploadFile, fixed_width=FIXED_WIDTH):
    image_bytes = await upload_file.read()
    image = Image.open(BytesIO(image_bytes))

    aspect_ratio = image.height / image.width
    new_height = int(fixed_width * aspect_ratio)
    resized_image = image.resize((fixed_width, new_height))

    buffered = BytesIO()
    resized_image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return f"data:image/png;base64,{img_base64}"
