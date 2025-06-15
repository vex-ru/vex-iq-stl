import os
import pyvista as pv
from pathlib import Path

# Настройки рендеринга
MESH_COLOR = 'silver'
BACKGROUND_COLOR = 'white'
WINDOW_SIZE = [800, 600]
SCREENSHOT_SCALE = 2  # Масштаб изображения
CAMERA_POSITION = [(1.5, 1.5, 1.5), (0, 0, 0), (0, 0, 1)]  # Камера под 3D-углом

# Установка переменных окружения для off-screen рендеринга
os.environ['PYVISTA_OFF_SCREEN'] = 'true'
os.environ['PYVISTA_USE_PANEL'] = 'false'

# Директория с STL-файлами
ROOT_DIR = Path('.')
OUTPUT_SUFFIX = '_preview.png'

# Обход всех папок
for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.lower().endswith('.stl'):
            stl_path = Path(root) / file
            png_path = stl_path.with_name(f"{stl_path.stem}_preview.png")

            try:
                # Загрузка модели
                mesh = pv.read(str(stl_path))

                # Создание Plotter
                plotter = pv.Plotter(window_size=WINDOW_SIZE, off_screen=True)

                # Добавление модели с гладким шейдингом
                plotter.add_mesh(
                    mesh,
                    color=MESH_COLOR,
                    smooth_shading=True,
                    show_edges=False
                )

                # Настройка камеры
                plotter.camera_position = CAMERA_POSITION
                plotter.reset_camera()

                # Установка фона
                plotter.background_color = BACKGROUND_COLOR

                # Сохранение изображения
                plotter.screenshot(str(png_path), scale=SCREENSHOT_SCALE)
                plotter.close()

                print(f"✅ Сохранено: {png_path}")

            except Exception as e:
                print(f"❌ Ошибка: {stl_path} — {e}")