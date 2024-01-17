
# Лицензия: MIT License
# Автор: Ваше Имя
# Описание: Программа для сравнения и сохранения похожих лиц на изображениях.

# Импорт необходимых библиотек

import os
import json
import face_recognition
from PIL import Image, ImageDraw
import numpy as np
from shutil import copyfile
import shutil

# Функция для сравнения лиц
def compare_faces(known_face_encoding, face_encoding_to_check, tolerance=0.55):
    """
    Сравнивает два лицевых кодирования, чтобы определить, насколько они похожи.
    :param known_face_encoding: Известное лицевое кодирование
    :param face_encoding_to_check: Кодирование лица для проверки
    :param tolerance: Допустимая погрешность при сравнении
    :return: True, если лица похожи, иначе False
    """
    # Вычисление расстояния между лицевыми кодированиями
    face_distance = face_recognition.face_distance([known_face_encoding], face_encoding_to_check)
    return face_distance[0] <= tolerance
    
# Функция для сохранения похожих лиц
def save_similar_faces(known_faces, output_folder, recognized_faces):
    """
    Сравнивает лицевые кодирования и сохраняет похожие лица в отдельную папку.
    :param known_faces: Список известных лицевых параметров
    :param output_folder: Папка для сохранения похожих лиц
    :param recognized_faces: Список распознанных лиц
    """
    # Создание папки для похожих лиц, если её нет
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Перебор всех известных лиц
    for i, known_face in enumerate(known_faces):
        # Создание папки для текущего известного лица, если её нет
        known_face_folder = os.path.join(output_folder, f"known_face_{i}")
        if not os.path.exists(known_face_folder):
            os.makedirs(known_face_folder)

        # Перебор всех распознанных лиц для сравнения
        for j, recognized_face in enumerate(recognized_faces):
            # Сравнение лиц
            if compare_faces(known_face["encoding"], np.array(recognized_face["encoding"])):
                # Сохранение похожего лица в папку
                image_path = recognized_face["name"]  # Путь к изображению с распознанным лицом
                _, image_filename = os.path.split(image_path)
                save_image_path = os.path.join(known_face_folder, f"similar_{image_filename}")
                copyfile(image_path, save_image_path)

def recognize_faces_in_folder(folder_path, output_folder, known_faces):
    # Получение списка файлов в папке
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Перебор всех файлов
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)

        # Загрузка изображения с лицами
        image = face_recognition.load_image_file(image_path)

        # Нахождение всех лиц на изображении
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        # Определение имен и сохранение параметров по распознанным лицам
        recognized_faces = []
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            face_data = {
                "name": os.path.abspath(image_path),  # Используйте абсолютный путь
                "encoding": face_encoding.tolist(),
            }
            recognized_faces.append(face_data)

        # Отрисовка прямоугольников вокруг лиц
        pil_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_image)

        for (top, right, bottom, left), face_data in zip(face_locations, recognized_faces):
            draw.rectangle([left, top, right, bottom], outline="red", width=5)
            draw.text((left, top - 10), face_data["name"], fill="red")

        # Сохранение параметров каждого распознанного лица в JSON
        save_path = os.path.join(output_folder, f"recognized_faces_{image_file.replace('.', '_')}.json")
        with open(save_path, 'w') as json_file:
            json_file.write(json.dumps(recognized_faces, indent=2))

        # Сохранение результата изображения с выделенными лицами
        pil_image.save(os.path.join(output_folder, f"recognized_faces_{image_file}"))

        # Вызов функции для сравнения и сохранения похожих лиц
        save_similar_faces(known_faces, output_folder, recognized_faces)

# Пример использования
# Путь к папке с известными лицами
known_faces_folder = "known_faces"

# Путь к папке с изображениями
folder_path = "faces"

# Путь к папке с результатом
output_folder = "recognized"



# Отчистка папки с резултьтатами
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)

# Создание пустой папки recognized
    os.makedirs(output_folder)
    
# Загрузка известных лиц и их кодирований
known_faces = []
known_face_files = [f for f in os.listdir(known_faces_folder) if f.lower().endswith('.json')]
for known_face_file in known_face_files:
    known_face_path = os.path.join(known_faces_folder, known_face_file)
    with open(known_face_path, 'r') as json_file:
        known_face_data = json.load(json_file)

        # Обработка каждого лица в файле
        for face in known_face_data:
            if "encoding" in face:
                known_faces.append({"encoding": np.array(face["encoding"]), "name": face["name"]})
            else:
                print(f"Invalid format in {known_face_file}. Skipping...")

# Путь к папке с изображениями
folder_path = "faces"
output_folder = "recognized"

# Распознавание лиц во всех фотографиях из папки
recognize_faces_in_folder(folder_path, output_folder, known_faces)
