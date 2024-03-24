import base64
from cryptography.fernet import Fernet
from PIL import Image
import numpy as np

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()

def embed_message_in_image(image_path, message, output_path):
    img = Image.open(image_path)
    img_array = np.array(img)

    # Гарантируем, что сообщение влезет в изображение
    assert img_array.size // 3 >= len(message), "Message too long for this image."

    # Конвертируем сообщение в бинарный формат
    # Так как message уже является байтовой строкой (bytes), преобразование в 'utf-8' не требуется
    binary_message = ''.join(format(byte, '08b') for byte in message)  # Исправлено здесь
    binary_message += '1111111111111110'  # Добавляем стоп-сигнал в конец сообщения
    message_index = 0

    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            pixel = img_array[i, j]
            for k in range(3):  # Проходим по каждому каналу пикселя
                if message_index < len(binary_message):
                    # Заменяем наименее значимый бит на бит сообщения
                    img_array[i, j, k] = int(format(pixel[k], '08b')[:-1] + binary_message[message_index], 2)
                    message_index += 1

    Image.fromarray(img_array).save(output_path)

def extract_message_from_image(image_path):
    img = Image.open(image_path)
    img_array = np.array(img)

    binary_message = ''
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            pixel = img_array[i, j]
            for k in range(3):  # Проходим по каждому каналу пикселя
                binary_message += format(pixel[k], '08b')[-1]

    # Ищем стоп-сигнал в бинарном сообщении
    stop_index = binary_message.find('1111111111111110')
    if stop_index != -1:
        binary_message = binary_message[:stop_index]

    message_bytes = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]
    message = ''.join([chr(int(byte, 2)) for byte in message_bytes])

    return message
