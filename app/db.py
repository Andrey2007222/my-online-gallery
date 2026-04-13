from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String

# Создаем подключение к базе данных
engine = create_engine(url='sqlite:///data.db', connect_args={"check_same_thread": False})

# Создаем фабрику сессий
SessionLocal = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

# Модель изображения (картины)
class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=True)
    artist = Column(String, index=True, nullable=False)
    year = Column(String, nullable=True)
    description = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)

# Получить изображение по имени файла
def get_image(filename: str):
    with SessionLocal() as new_session:
        query = select(Image).filter_by(filename=filename)
        result = new_session.execute(query)
        return result.scalar_one_or_none()

# Получить все изображения
def get_all_images():
    with SessionLocal() as new_session:
        query = select(Image)
        result = new_session.execute(query)
        return result.scalars().all()

# Получить изображения по художнику
def get_images_by_artist(artist: str):
    with SessionLocal() as new_session:
        query = select(Image).filter_by(artist=artist)
        result = new_session.execute(query)
        return result.scalars().all()

# Добавить новое изображение
def add_image(image_data: dict):
    with SessionLocal() as new_session:
        db_image = Image(**image_data)
        new_session.add(db_image)
        new_session.commit()
        new_session.refresh(db_image)
        return db_image

# Удалить изображение по ID
def delete_image(image_id: int):
    with SessionLocal() as new_session:
        query = delete(Image).where(Image.id == image_id)
        new_session.execute(query)
        new_session.commit()

# Удалить все изображения (очистить базу)
def delete_all_images():
    with SessionLocal() as new_session:
        new_session.query(Image).delete()
        new_session.commit()

# Получить изображение по ID
def get_image_by_id(image_id: int):
    with SessionLocal() as new_session:
        query = select(Image).filter_by(id=image_id)
        result = new_session.execute(query)
        return result.scalar_one_or_none()