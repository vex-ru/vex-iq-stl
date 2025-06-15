import os

# Пути к основным папкам (относительно текущего скрипта)
categories = {
    'Крепежные элементы': 'Крепежные элементы',
    'Другие': 'Другие',
    'Электронные компоненты': 'Электронные компоненты',
    'Структурные элементы': 'Структурные элементы',
    'Элементы движения': 'Элементы движения'
}

# Начало HTML-документа
html = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Каталог деталей</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .category { margin-bottom: 30px; }
        .subcategory { margin-top: 20px; }
        .part-box {
            display: flex;
            align-items: center;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
            background: #f9f9f9;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .part-image {
            max-width: 350px;
            max-height: 350px;
            margin-right: 20px;
            object-fit: contain;
        }
        .part-info h3 { margin: 0; }
        .part-info p { color: #555; margin: 5px 0; }
        .part-links a { 
            display: inline-block; 
            margin-right: 10px; 
            text-decoration: none; 
            color: #0066cc;
            padding: 5px 10px;
            border-radius: 3px;
            background: #e8f4ff;
        }
        .part-links a:hover {
            background: #d0eaff;
        }
    </style>
</head>
<body>
    <h1>📦 Каталог деталей</h1>'''

# Обработка каждой категории
for category_name, folder in categories.items():
    if not os.path.exists(folder):
        continue
        
    html += f'<div class="category"><h2>📁 {category_name}</h2>'
    
    # Обход всех подкаталогов и файлов
    for root, dirs, files in os.walk(folder):
        # Группировка файлов по подкатегориям
        rel_path = os.path.relpath(root, folder)
        if rel_path == '.':
            subcategory = ''
        else:
            subcategory = rel_path.replace('\\', '/')

        # Группировка файлов
        step_files = {}
        stl_files = {}
        
        for f in files:
            if f.endswith('.STEP'):
                base = os.path.splitext(f)[0]
                step_files[base] = f
            elif f.endswith('.stl'):
                base = os.path.splitext(f)[0]
                stl_files[base] = f
        
        # Если есть детали в подкатегории, выводим заголовок
        if subcategory and any(base in stl_files for base in step_files):
            html += f'<div class="subcategory"><h3>🗂️ {subcategory}</h3>'

        # Поиск совпадающих пар
        for base in step_files:
            if base in stl_files:
                # Формирование относительных путей
                step_rel = os.path.join(os.path.relpath(root, '.'), step_files[base]).replace('\\', '/')
                stl_rel = os.path.join(os.path.relpath(root, '.'), stl_files[base]).replace('\\', '/')
                
                # Проверка наличия изображения
                image_rel = "https://via.placeholder.com/150" 
                for ext in [".png", ".jpg"]:
                    image_filename = f"{base}_preview{ext}"
                    image_path_local = os.path.join(root, image_filename)
                    if os.path.exists(image_path_local):
                        image_rel = os.path.join(os.path.relpath(root, '.'), image_filename).replace('\\', '/')
                        break
                
                # Блок детали
                html += f'''
<div class="part-box">
    <img class="part-image" src="{image_rel}" alt="Изображение детали {base}">
    <div class="part-info">
        <h3>🔧 {base}</h3>
        <p>Номер детали: {base}</p>
        <div class="part-links">
            <a href="{step_rel}" download>📥 Скачать STEP</a>
            <a href="{stl_rel}" download>📦 Скачать STL</a>
        </div>
    </div>
</div>'''

        # Закрытие подкатегории
        if subcategory and any(base in stl_files for base in step_files):
            html += '</div>'

    html += '</div> <!-- category -->'

# Конец HTML-документа
html += '''
</body>
</html>
'''

# Сохранение файла
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Сайт успешно сгенерирован в файле index.html")