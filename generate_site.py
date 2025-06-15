import os

# Пути к основным папкам
categories = {
    'Крепежные элементы': 'Крепежные элементы',
    'Другие': 'Другие',
    'Электронные компоненты': 'Электронные компоненты',
    'Структурные элементы': 'Структурные элементы',
    'Элементы движения': 'Элементы движения'
}

# Сбор категорий и подкатегорий
category_data = []

for category_name, folder in categories.items():
    if not os.path.exists(folder):
        continue

    subcategories = set()

    for root, dirs, files in os.walk(folder):
        rel_path = os.path.relpath(root, folder)
        if rel_path == '.':
            continue

        step_files = {}
        stl_files = {}

        for f in files:
            if f.endswith('.STEP'):
                base = os.path.splitext(f)[0]
                step_files[base] = f
            elif f.endswith('.stl'):
                base = os.path.splitext(f)[0]
                stl_files[base] = f

        common_bases = set(step_files.keys()) & set(stl_files.keys())
        if common_bases:
            subcategories.add(rel_path.replace('\\', '/'))

    category_data.append({
        'name': category_name,
        'folder': folder,
        'subcategories': sorted(subcategories)
    })

# Начало HTML-документа
html = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Бесплатные STL и STEP файлы для VEX IQ роботов. Качественные 3D модели для образовательной робототехники. Скачайте готовые детали для сборки и проектов прямо сейчас!">
    <meta name="keywords" content="VEX IQ, STL файлы, 3D модели, образовательная робототехника, STEP файлы, детали для роботов, STEM-образование, скачивание STL, VEX IQ библиотека">
    <title>VEX IQ STL файлы | Бесплатные 3D модели для робототехники</title>
    <!-- Bootstrap CSS -->
    <link href="cssjs/bootstrap.min.css"  rel="stylesheet">
    <style>
        body {
            scroll-behavior: smooth;
            padding-top: 100px; /* Отступ под fixed navbar */
        }
        .navbar {
            background-color: #1e3a8a;
        }
        .navbar a {
            color: white !important;
        }
        .dropdown-menu {
            background-color: #1e3a8a !important;
        }
        .dropdown-item {
            color: white !important;
        }
        .part-image {
            max-width: 250px;
            max-height: 250px;
            object-fit: contain;
            border: 1px solid #ddd;
            padding: 5px;
            background: #fafafa;
        }
        .category, .subcategory {
            scroll-margin-top: 70px;
        }
        /* Стили для полноэкранного изображения */
        .fullscreen-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 9999;
            transition: opacity 0.3s ease;
        }
        .fullscreen-image {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            max-width: 90%;
            max-height: 90%;
            cursor: zoom-out;
        }

        
    </style>
    <!-- Yandex.Metrika counter -->
    <script type="text/javascript" >
    (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
    m[i].l=1*new Date();
    for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
    k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
    (window, document, "script", "https://mc.yandex.ru/metrika/tag.js",    "ym");

    ym(102655870, "init", {
            clickmap:true,
            trackLinks:true,
            accurateTrackBounce:true,
            webvisor:true
    });
    </script>
    <noscript><div><img src="https://mc.yandex.ru/watch/102655870"    style="position:absolute; left:-9999px;" alt="" /></div></noscript>
    <!-- /Yandex.Metrika counter -->
</head>
<body>

    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg fixed-top">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">🧠 VEX IQ STL</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">'''

# Генерация меню с выпадающими подкатегориями
for cat in category_data:
    category_name = cat['name']
    folder = cat['folder']
    subcategories = cat['subcategories']
    anchor = category_name.replace(' ', '_')

    if subcategories:
        html += f'''
        <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                {category_name}
            </a>
            <ul class="dropdown-menu">'''

        for sub in subcategories:
            sub_anchor = f"{anchor}_{sub.replace('/', '_')}"
            html += f'                <li><a class="dropdown-item" href="#{sub_anchor}">{sub}</a></li>\n'

        html += '            </ul>\n        </li>'
    else:
        html += f'        <li class="nav-item"><a class="nav-link" href="#{anchor}">{category_name}</a></li>\n'

html += '''            </ul>
        </div>
    </div>
</nav>

<!-- Main Content -->
<div class="container mt-5">
    <h1 class="mb-4">📚 Библиотека 3D моделей для VEX IQ</h1>
    <p class="lead">Бесплатные STL и STEP файлы для робототехнических проектов, образовательных сборок и STEM-программ.</p>'''

# Генерация контента
for cat in category_data:
    category_name = cat['name']
    folder = cat['folder']
    subcategories = cat['subcategories']
    anchor = category_name.replace(' ', '_')

    html += f'<div id="{anchor}" class="category mb-5"><h2 class="mb-4">📁 {category_name}</h2>'

    subcat_data = {}

    for root, dirs, files in os.walk(folder):
        rel_path = os.path.relpath(root, folder)
        if rel_path == '.':
            rel_path = ''
        else:
            if rel_path not in subcategories:
                continue

        step_files = {}
        stl_files = {}

        for f in files:
            if f.endswith('.STEP'):
                base = os.path.splitext(f)[0]
                step_files[base] = f
            elif f.endswith('.stl'):
                base = os.path.splitext(f)[0]
                stl_files[base] = f

        common_bases = set(step_files.keys()) & set(stl_files.keys())

        if common_bases:
            if rel_path not in subcat_data:
                subcat_data[rel_path] = []
            for base in common_bases:
                step_rel = os.path.join(os.path.relpath(root, '.'), step_files[base]).replace('\\', '/')
                stl_rel = os.path.join(os.path.relpath(root, '.'), stl_files[base]).replace('\\', '/')
                image_rel = "https://via.placeholder.com/250x250?text=Preview"
                for ext in [".png", ".jpg"]:
                    image_filename = f"{base}_preview{ext}"
                    image_path_local = os.path.join(root, image_filename)
                    if os.path.exists(image_path_local):
                        image_rel = os.path.join(os.path.relpath(root, '.'), image_filename).replace('\\', '/')
                        break

                subcat_data[rel_path].append({
                    'name': base,
                    'step': step_rel,
                    'stl': stl_rel,
                    'image': image_rel
                })

    for sub, parts in subcat_data.items():
        sub_anchor = f"{anchor}_{sub.replace('/', '_')}"
        if sub:
            html += f'<div id="{sub_anchor}" class="subcategory mb-4"><h4 class="mb-3">🗂️ {sub}</h4>'
        else:
            html += f'<div id="{anchor}" class="subcategory mb-4">'

        for part in parts:
            html += f'''
<div class="card mb-3">
    <div class="row g-0">
        <div class="col-md-3 d-flex align-items-center justify-content-center">
            <img src="{part["image"]}" class="part-image img-fluid" alt="Изображение детали {part["name"]}" onclick="showFullscreen(\'{part["image"]}\')">
        </div>
        <div class="col-md-9">
            <div class="card-body">
                <h5 class="card-title">🔧 {part["name"]}</h5>
                <p class="card-text">Номер детали: {part["name"]}</p>
                <div>
                    <a href="{part["step"]}" class="btn btn-primary me-2" download>📥 STEP</a>
                    <a href="{part["stl"]}" class="btn btn-outline-primary" download>📦 STL</a>
                </div>
            </div>
        </div>
    </div>
</div>'''

        html += '</div> <!-- subcategory -->'

    html += '</div> <!-- category -->\n'

# Конец HTML-документа    
html += '''
    </div>

    <!-- Полноэкранный слой -->
    <div class="fullscreen-overlay" onclick="hideFullscreen()">
        <img class="fullscreen-image" src="" alt="Полноэкранный просмотр">
    </div>

    <!-- Bootstrap JS -->
    <script src="cssjs/bootstrap.bundle.min.js"></script>
    <script>
        let fullscreenImage = document.querySelector('.fullscreen-image');
        let overlay = document.querySelector('.fullscreen-overlay');

        function showFullscreen(src) {
            fullscreenImage.src = src;
            overlay.style.display = 'block';
        }

        function hideFullscreen() {
            overlay.style.display = 'none';
        }
    </script>
</body>
</html>
'''

# Сохранение файла
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Сайт успешно сгенерирован в файле index.html")