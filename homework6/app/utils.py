import base64
import logging
from io import BytesIO
from typing import Optional

from PIL import Image as PILImage
from pydantic import BaseModel, validator

from config import cfg

from .redis_cfg import redis_conn
from .size import Size

logger = logging.getLogger(__name__)


class ImageSchema(BaseModel):
    data: str

    @validator('data')
    def data_must_be_square(cls, v: str) -> str:
        image = ImageEncoder.decode(v)
        if image.width != image.height:
            raise ValueError('Image must be square')
        return v

    @validator('data')
    def data_must_encode_decode(cls, v: str) -> str:
        try:
            image = ImageEncoder.decode(v)
            v_new = ImageEncoder.encode(image)
            assert v == v_new
        except Exception as exc:
            logger.exception('decode/encode error')
            raise ValueError('Invalid image data') from exc
        return v


class ImageEncoder:
    @staticmethod
    def decode(image_data: str) -> PILImage:
        try:
            return PILImage.open(BytesIO(base64.b64decode(image_data)))
        except Exception as exc:
            logger.exception('Failed to decode image')
            raise ValueError('Invalid image data') from exc

    @staticmethod
    def encode(image: PILImage) -> str:
        try:
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
        except Exception as exc:
            logger.exception('Failed to encode image')
            raise ValueError('Failed to encode image') from exc


class ImageProcessor:
    @classmethod
    def process(
        cls, task_id: int, image_data: str, return_data: bool = False
    ) -> Optional[dict[str, str]]:
        result = {size: '' for size in cfg.allowed_sizes}
        result['original'] = image_data
        try:
            image = ImageEncoder.decode(result['original'])
        except ValueError:
            logger.exception('Failed to decode image')
            raise

        for size in result:
            if size == 'original':
                continue
            try:
                image_copy = image.copy()
                image_copy.thumbnail((int(size), int(size)))
                result[Size(size)] = ImageEncoder.encode(image_copy)
            except Exception:
                logger.exception('Failed to resize image')
                raise

        if return_data:
            return result
        redis_conn.hset(task_id, mapping=result)  # type: ignore
        return None


def generate_task_id() -> str:
    return str(redis_conn.incr('task_id'))
