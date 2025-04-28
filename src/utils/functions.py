import re
from fastapi import UploadFile
import os
import aiofiles
from uuid import uuid4


def format_local_number(raw_number: str) -> str:
    cleaned = re.sub(r'\D', '', raw_number)
    if len(cleaned) != 9:
        raise ValueError("Invalid phone number: must contain exactly 9 digits")
    return cleaned


async def save_file(file: UploadFile) -> str:
        try:
            if not file.content_type.startswith("image/"):
                raise ValueError("Only image files are allowed")
            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)
            filename = f"{uuid4()}_{file.filename}"
            file_path = os.path.join(upload_dir, filename)
            async with aiofiles.open(file_path, "wb") as buffer:
                content = await file.read()
                await buffer.write(content)
            return file_path
        except Exception as e:
            raise ValueError(f"Failed to save file: {str(e)}")
        finally:
            await file.close()