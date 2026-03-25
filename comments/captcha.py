import base64
import random
import string
from io import BytesIO

from captcha.image import ImageCaptcha


def generate_captcha():
    text = "".join(random.choices(string.ascii_letters + string.digits, k=5))

    image = ImageCaptcha()
    data = image.generate(text)

    buffer = BytesIO()
    buffer.write(data.read())
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    return text, image_base64
