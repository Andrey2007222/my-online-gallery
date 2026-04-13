from pydantic import BaseModel
from typing import Optional

class ImageResponse(BaseModel):
    """Модель для ответа API с информацией о картине"""
    id: int
    filename: str
    title: Optional[str] = None
    artist: str
    year: Optional[str] = None
    description: Optional[str] = None
    file_path: str
    file_size: int
    width: Optional[int] = None
    height: Optional[int] = None

    class Config:
        from_attributes = True

class ImageCreate(BaseModel):
    """Модель для создания новой картины"""
    filename: str
    title: Optional[str] = None
    artist: str
    year: Optional[str] = None
    description: Optional[str] = None
    file_path: str
    file_size: int
    width: Optional[int] = None
    height: Optional[int] = None

class ImageUpdate(BaseModel):
    """Модель для обновления информации о картине"""
    title: Optional[str] = None
    artist: Optional[str] = None
    year: Optional[str] = None
    description: Optional[str] = None