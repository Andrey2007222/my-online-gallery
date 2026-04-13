import uvicorn
import sys
from pathlib import Path

# Добавляем текущую директорию в путь
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    print("=" * 60)
    print("🎨 ARTSPACE ГАЛЕРЕЯ")
    print("=" * 60)
    print("🌐 Сайт запускается...")
    print("📱 Откройте в браузере: http://localhost:8000")
    print("📚 API документация: http://localhost:8000/docs")
    print("=" * 60)
    print("⚠️  Для остановки нажмите Ctrl+C")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True 
    )