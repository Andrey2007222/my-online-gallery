from fastapi import HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from app.db import Image, get_image, get_all_images, get_images_by_artist, SessionLocal, add_image

PAINTINGS_DIR = Path('paintings')

def get_paintings_info():
    """Информация о картинах для автозаполнения базы данных"""
    return {
        "Звездная ночь": {
            "artist": "Винсент Ван Гог",
            "year": "1889",
            "description": "Одна из самых известных картин Ван Гога, изображающая вид из окна психиатрической лечебницы. Небо наполнено вихревыми облаками и яркими звездами."
        },
        "Постоянство памяти": {
            "artist": "Сальвадор Дали",
            "year": "1931",
            "description": "Сюрреалистическая картина с мягкими тающими часами, символ текучести времени и относительности пространства."
        },
        "Крик": {
            "artist": "Эдвард Мунк",
            "year": "1893",
            "description": "Экспрессионистский шедевр, передающий чувство тревоги и отчаяния. Одна из самых узнаваемых картин в мире."
        },
        "Герника": {
            "artist": "Пабло Пикассо",
            "year": "1937",
            "description": "Монументальная картина о ужасах войны, написанная после бомбардировки испанского города Герника."
        },
        "Девушка с жемчужной сережкой": {
            "artist": "Ян Вермеер",
            "year": "1665",
            "description": "Знаменитый портрет, называемый 'Северной Моной Лизой'. Загадочный взгляд девушки приковывает внимание зрителей."
        },
        "Ночная терраса кафе": {
            "artist": "Винсент Ван Гог",
            "year": "1888",
            "description": "Яркая картина с звездным небом и освещенной террасой кафе в Арле. Передает атмосферу южной ночи."
        },
        "Поцелуй": {
            "artist": "Густав Климт",
            "year": "1908",
            "description": "Символ золотого периода Климта, изображающий влюбленную пару в объятиях. Украшена сусальным золотом."
        },
        "Водяные лилии": {
            "artist": "Клод Моне",
            "year": "1919",
            "description": "Серия импрессионистских картин с видом на пруд с кувшинками в саду Моне в Живерни."
        },
        "Три возраста женщины": {
            "artist": "Густав Климт",
            "year": "1905",
            "description": "Аллегорическая картина о жизненном цикле женщины: детство, материнство и старость."
        },
        "Автопортрет с перерезанным ухом": {
            "artist": "Винсент Ван Гог",
            "year": "1889",
            "description": "Один из самых известных автопортретов Ван Гога, созданный после инцидента с отрезанием уха."
        },
        "Сон": {
            "artist": "Пабло Пикассо",
            "year": "1932",
            "description": "Портрет возлюбленной Пикассо, Марии-Терезы Вальтер. Одна из самых дорогих картин в мире."
        },
        "Восход солнца": {
            "artist": "Клод Моне",
            "year": "1872",
            "description": "Картина, давшая название импрессионизму. Изображает порт Гавр на рассвете."
        },
        "Тайная вечеря": {
            "artist": "Леонардо да Винчи",
            "year": "1498",
            "description": "Фреска, изображающая последний ужин Иисуса с апостолами. Шедевр эпохи Возрождения."
        },
        "Рождение Венеры": {
            "artist": "Сандро Боттичелли",
            "year": "1485",
            "description": "Шедевр эпохи Возрождения, изображающий богиню любви Венеру, выходящую из морской пены."
        },
        "Черный квадрат": {
            "artist": "Казимир Малевич",
            "year": "1915",
            "description": "Икона супрематизма, символ нового искусства. Картина, изменившая представление о живописи."
        },
        "Мона Лиза": {
            "artist": "Леонардо да Винчи",
            "year": "1503",
            "description": "Самая известная картина в мире, известная своей загадочной улыбкой. Хранится в Лувре."
        },
        "Сотворение Адама": {
            "artist": "Микеланджело",
            "year": "1512",
            "description": "Фреска на потолке Сикстинской капеллы, изображающая момент создания Адама Богом."
        },
        "Ночной дозор": {
            "artist": "Рембрандт",
            "year": "1642",
            "description": "Групповой портрет амстердамских стрелков, известный игрой света и тени."
        },
        "Подсолнухи": {
            "artist": "Винсент Ван Гог",
            "year": "1888",
            "description": "Серия натюрмортов с подсолнухами, символизирующая благодарность и дружбу."
        },
        "Американская готика": {
            "artist": "Грант Вуд",
            "year": "1930",
            "description": "Икона американского искусства, изображающая фермера с дочерью на фоне готического дома."
        }
    }

def load_paintings_to_db():
    """Загрузка информации о картинах в базу данных"""
    if not PAINTINGS_DIR.exists():
        PAINTINGS_DIR.mkdir(exist_ok=True)
        print(f"📁 Создана папка {PAINTINGS_DIR}")
        return
    
    paintings_info = get_paintings_info()
    # Ищем изображения в папке paintings
    image_files = list(PAINTINGS_DIR.glob("*.jpg")) + \
                  list(PAINTINGS_DIR.glob("*.jpeg")) + \
                  list(PAINTINGS_DIR.glob("*.png")) + \
                  list(PAINTINGS_DIR.glob("*.gif"))
    
    if not image_files:
        print("⚠️ В папке paintings нет изображений")
        print("📝 Пожалуйста, добавьте изображения картин в папку paintings")
        print("📝 Имена файлов должны соответствовать названиям картин (например: 'Звездная ночь.jpg')")
        return
    
    loaded_count = 0
    skipped_count = 0
    
    for file_path in image_files:
        filename = file_path.name
        
        # Проверяем, есть ли уже такая картина в базе
        existing = get_image(filename)
        if existing:
            skipped_count += 1
            continue
        
        # Получаем название из имени файла (без расширения)
        name_without_ext = filename.rsplit('.', 1)[0]
        title = name_without_ext
        
        # Ищем информацию о картине
        info = paintings_info.get(title, {})
        artist = info.get("artist", "Неизвестный художник")
        year = info.get("year", "")
        description = info.get("description", f"Шедевр '{title}'")
        
        # Получаем размеры изображения
        width = None
        height = None
        try:
            from PIL import Image as PILImage
            with PILImage.open(file_path) as img:
                width, height = img.size
        except Exception as e:
            print(f"⚠️ Не удалось получить размеры для {filename}: {e}")
        
        # Создаем запись в базе данных
        image_data = {
            "filename": filename,
            "title": title,
            "artist": artist,
            "year": year,
            "description": description,
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size,
            "width": width,
            "height": height,
        }
        
        try:
            add_image(image_data)
            loaded_count += 1
            print(f"🖼️ Загружена картина: '{title}' - {artist}")
        except Exception as e:
            print(f"❌ Ошибка при загрузке {filename}: {e}")
    
    # Выводим итоговую статистику
    print("=" * 50)
    print(f"✅ Загружено новых картин: {loaded_count}")
    if skipped_count > 0:
        print(f"⏭️ Пропущено (уже есть в базе): {skipped_count}")
    if not image_files:
        print("💡 Подсказка: Добавьте изображения в папку 'paintings' и перезапустите сервер")
    print("=" * 50)

async def get_image_by_id(image_id: int):
    """Получить изображение по ID"""
    with SessionLocal() as session:
        image = session.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Картина не найдена")
        return image

async def get_image_file(filename: str):
    """Получить файл изображения"""
    image = get_image(filename)
    if not image:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    
    file_path = Path(image.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Файл не найден на сервере")
    
    return FileResponse(file_path)

async def get_images_by_artist_endpoint(artist_name: str):
    """Получить все картины художника"""
    images = get_images_by_artist(artist_name)
    if not images:
        raise HTTPException(status_code=404, detail=f"Картины художника '{artist_name}' не найдены")
    return images

async def get_all_artists():
    """Получить список всех художников с их картинами"""
    images = get_all_images()
    artists_dict = {}
    
    for image in images:
        if image.artist not in artists_dict:
            artists_dict[image.artist] = []
        artists_dict[image.artist].append({
            "id": image.id,
            "title": image.title,
            "filename": image.filename,
            "year": image.year,
            "description": image.description
        })
    
    return {"artists": artists_dict, "total_artists": len(artists_dict), "total_paintings": len(images)}

def search_images(query: str):
    """Поиск картин по названию или художнику"""
    images = get_all_images()
    query_lower = query.lower()
    
    results = []
    for image in images:
        if (query_lower in image.title.lower() or 
            query_lower in image.artist.lower() or
            (image.description and query_lower in image.description.lower())):
            results.append(image)
    
    return results

def get_paintings_by_year(year: str):
    """Получить картины по году создания"""
    images = get_all_images()
    return [img for img in images if img.year == year]

def get_statistics():
    """Получить статистику галереи"""
    images = get_all_images()
    artists = set()
    years = set()
    
    for img in images:
        artists.add(img.artist)
        if img.year:
            years.add(img.year)
    
    return {
        "total_paintings": len(images),
        "total_artists": len(artists),
        "total_years": len(years),
        "artists_list": sorted(list(artists)),
        "years_list": sorted(list(years), reverse=True)
    }