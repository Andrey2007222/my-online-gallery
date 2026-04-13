from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from contextlib import asynccontextmanager
from app.db import Base, Image, engine, SessionLocal, get_all_images, get_image, get_images_by_artist, add_image, delete_image
from app.utils import load_paintings_to_db
from app.models import ImageResponse
from typing import List
from pathlib import Path
from datetime import datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    print("✅ База данных создана")
    with SessionLocal() as session:
        count = session.query(Image).count()
        if count == 0:
            load_paintings_to_db()
            print(f"📚 Загружено {session.query(Image).count()} картин")
        else:
            print(f"📚 В базе уже есть {count} картин")
    yield

# СОЗДАЕМ ПРИЛОЖЕНИЕ - ЭТО ВАЖНО!
app = FastAPI(lifespan=lifespan, title="ArtSpace Галерея")

UPLOAD_DIR = Path("paintings")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    images = get_all_images()
    
    # Получаем уникальных художников
    artists = sorted(set(img.artist for img in images if img.artist))
    years = sorted(set(img.year for img in images if img.year), reverse=True)
    
    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ArtSpace | Современная галерея</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Montserrat', sans-serif;
                background: #0a0a0a;
                color: #fff;
                overflow-x: hidden;
            }}
            
            .background {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -2;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            }}
            
            .navbar {{
                position: fixed;
                top: 0;
                width: 100%;
                background: rgba(10, 10, 10, 0.95);
                backdrop-filter: blur(20px);
                z-index: 1000;
                padding: 1rem 2rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .nav-container {{
                max-width: 1400px;
                margin: 0 auto;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            .logo {{
                font-family: 'Playfair Display', serif;
                font-size: 1.8rem;
                font-weight: 700;
                background: linear-gradient(135deg, #fff 0%, #a8a8ff 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            
            .hero {{
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 0 2rem;
            }}
            
            .hero-title {{
                font-family: 'Playfair Display', serif;
                font-size: 5rem;
                font-weight: 800;
                margin-bottom: 1rem;
                background: linear-gradient(135deg, #fff 0%, #a8a8ff 50%, #ffa8a8 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            
            .hero-subtitle {{
                font-size: 1.2rem;
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 2rem;
            }}
            
            .main-content {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 6rem 2rem;
            }}
            
            .section-title {{
                font-family: 'Playfair Display', serif;
                font-size: 2.5rem;
                margin-bottom: 2rem;
                text-align: center;
            }}
            
            .filter-container {{
                display: flex;
                gap: 1rem;
                justify-content: center;
                flex-wrap: wrap;
                margin-bottom: 3rem;
            }}
            
            .filter-btn {{
                padding: 0.8rem 1.5rem;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 50px;
                color: #fff;
                cursor: pointer;
                transition: all 0.3s;
            }}
            
            .filter-btn:hover, .filter-btn.active {{
                background: linear-gradient(135deg, #a8a8ff, #ffa8a8);
            }}
            
            .gallery {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: 2rem;
            }}
            
            .art-card {{
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                overflow: hidden;
                transition: all 0.3s;
                cursor: pointer;
                position: relative;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .art-card:hover {{
                transform: translateY(-10px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            }}
            
            .art-image {{
                width: 100%;
                height: 350px;
                object-fit: cover;
            }}
            
            .art-info {{
                padding: 1.5rem;
            }}
            
            .art-title {{
                font-family: 'Playfair Display', serif;
                font-size: 1.3rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
            }}
            
            .art-artist {{
                color: #a8a8ff;
                font-size: 0.9rem;
                margin-bottom: 0.5rem;
            }}
            
            .delete-btn {{
                position: absolute;
                top: 1rem;
                right: 1rem;
                background: rgba(255, 59, 59, 0.9);
                color: white;
                border: none;
                border-radius: 50%;
                width: 35px;
                height: 35px;
                cursor: pointer;
                z-index: 10;
            }}
            
            .floating-btn {{
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, #a8a8ff, #ffa8a8);
                border: none;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(168, 168, 255, 0.3);
                z-index: 100;
            }}
            
            .modal {{
                display: none;
                position: fixed;
                z-index: 2000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.95);
            }}
            
            .modal-content {{
                margin: auto;
                display: block;
                max-width: 90%;
                max-height: 85%;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                border-radius: 20px;
            }}
            
            .close {{
                position: absolute;
                top: 20px;
                right: 35px;
                color: #fff;
                font-size: 40px;
                cursor: pointer;
            }}
            
            @media (max-width: 768px) {{
                .hero-title {{ font-size: 2.5rem; }}
                .gallery {{ grid-template-columns: 1fr; }}
            }}
        </style>
    </head>
    <body>
        <div class="background"></div>
        
        <nav class="navbar">
            <div class="nav-container">
                <div class="logo">ARTSPACE</div>
            </div>
        </nav>
        
        <section class="hero">
            <div>
                <h1 class="hero-title">Искусство <br>в каждой детали</h1>
                <p class="hero-subtitle">Исследуйте уникальную коллекцию шедевров мирового искусства</p>
            </div>
        </section>
        
        <section class="main-content">
            <h2 class="section-title">Коллекция</h2>
            <div class="filter-container" id="filterContainer">
                <button class="filter-btn active" data-filter="all">Все</button>
                {''.join(f'<button class="filter-btn" data-filter="{a}">{a}</button>' for a in artists[:10])}
            </div>
            
            <div class="gallery" id="gallery">
    """
    
    for img in images:
        html += f"""
                <div class="art-card" data-artist="{img.artist}">
                    <button class="delete-btn" onclick="deleteImage(event, {img.id})">🗑️</button>
                    <img class="art-image" src="/image/{img.filename}" alt="{img.title}" onclick="openModal('/image/{img.filename}', '{img.title}', '{img.artist}', '{img.year}')">
                    <div class="art-info">
                        <h3 class="art-title">{img.title}</h3>
                        <p class="art-artist">{img.artist}</p>
                        <p class="art-year">{img.year if img.year else 'Год неизвестен'}</p>
                    </div>
                </div>
        """
    
    html += """
            </div>
        </section>
        
        <button class="floating-btn" onclick="openAddModal()">
            <i class="fas fa-plus" style="font-size: 24px; color: white;"></i>
        </button>
        
        <div id="modal" class="modal" onclick="closeModalOnClick(event)">
            <span class="close" onclick="closeModal()">&times;</span>
            <img class="modal-content" id="modalImage">
            <div id="modalCaption" class="modal-caption"></div>
        </div>
        
        <div id="addModal" class="modal" style="display: none;" onclick="closeAddModalOnClick(event)">
            <div class="close" onclick="closeAddModal()">&times;</div>
            <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 20px; padding: 40px; max-width: 500px; margin: 100px auto;">
                <h2 style="margin-bottom: 20px;">Добавить шедевр</h2>
                <form id="addForm" enctype="multipart/form-data" onsubmit="submitImage(event)">
                    <div style="margin-bottom: 20px;">
                        <input type="file" name="file" accept=".jpg,.jpeg,.png" required style="width: 100%; padding: 10px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; color: white;">
                    </div>
                    <div style="margin-bottom: 20px;">
                        <input type="text" name="title" placeholder="Название" required style="width: 100%; padding: 10px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; color: white;">
                    </div>
                    <div style="margin-bottom: 20px;">
                        <input type="text" name="artist" placeholder="Художник" required style="width: 100%; padding: 10px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; color: white;">
                    </div>
                    <div style="margin-bottom: 20px;">
                        <input type="text" name="year" placeholder="Год" style="width: 100%; padding: 10px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; color: white;">
                    </div>
                    <div style="margin-bottom: 20px;">
                        <textarea name="description" placeholder="Описание" rows="3" style="width: 100%; padding: 10px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; color: white;"></textarea>
                    </div>
                    <button type="submit" style="width: 100%; padding: 12px; background: linear-gradient(135deg, #a8a8ff, #ffa8a8); border: none; border-radius: 10px; color: white; cursor: pointer;">Добавить</button>
                </form>
            </div>
        </div>
        
        <script>
            const filterButtons = document.querySelectorAll('.filter-btn');
            const artCards = document.querySelectorAll('.art-card');
            
            filterButtons.forEach(btn => {
                btn.addEventListener('click', () => {
                    filterButtons.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    const filter = btn.dataset.filter;
                    artCards.forEach(card => {
                        if (filter === 'all' || card.dataset.artist === filter) {
                            card.style.display = 'block';
                        } else {
                            card.style.display = 'none';
                        }
                    });
                });
            });
            
            function openModal(imageUrl, title, artist, year) {
                const modal = document.getElementById('modal');
                const modalImg = document.getElementById('modalImage');
                const caption = document.getElementById('modalCaption');
                modal.style.display = 'block';
                modalImg.src = imageUrl;
                caption.innerHTML = `<strong>${title}</strong><br>${artist}${year ? ' (' + year + ')' : ''}`;
            }
            
            function closeModal() {
                document.getElementById('modal').style.display = 'none';
            }
            
            function closeModalOnClick(event) {
                if (event.target === document.getElementById('modal')) {
                    closeModal();
                }
            }
            
            function openAddModal() {
                document.getElementById('addModal').style.display = 'block';
            }
            
            function closeAddModal() {
                document.getElementById('addModal').style.display = 'none';
            }
            
            function closeAddModalOnClick(event) {
                if (event.target === document.getElementById('addModal')) {
                    closeAddModal();
                }
            }
            
            async function submitImage(event) {
                event.preventDefault();
                const formData = new FormData(event.target);
                const response = await fetch('/add-image', {
                    method: 'POST',
                    body: formData
                });
                if (response.ok) {
                    alert('✅ Шедевр добавлен!');
                    location.reload();
                } else {
                    alert('❌ Ошибка');
                }
            }
            
            async function deleteImage(event, imageId) {
                event.stopPropagation();
                if (confirm('Удалить?')) {
                    const response = await fetch(`/delete-image/${imageId}`, {
                        method: 'DELETE'
                    });
                    if (response.ok) {
                        location.reload();
                    }
                }
            }
        </script>
    </body>
    </html>
    """
    
    return html

@app.post("/add-image")
async def add_image_endpoint(
    file: UploadFile = File(...),
    title: str = Form(...),
    artist: str = Form(...),
    year: str = Form(""),
    description: str = Form("")
):
    try:
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        file_path = UPLOAD_DIR / filename
        content = await file.read()
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        from PIL import Image as PILImage
        with PILImage.open(file_path) as img:
            width, height = img.size
        
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
        
        add_image(image_data)
        return {"message": "Картина успешно добавлена"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete-image/{image_id}")
async def delete_image_endpoint(image_id: int):
    with SessionLocal() as session:
        image = session.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(status_code=404, detail="Картина не найдена")
        
        file_path = Path(image.file_path)
        if file_path.exists():
            file_path.unlink()
        
        session.delete(image)
        session.commit()
        
        return {"message": "Картина удалена"}

@app.get("/image/{filename}")
async def get_image_file(filename: str):
    image = get_image(filename)
    if not image:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    
    file_path = Path(image.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Файл не найден на сервере")
    
    return FileResponse(file_path)