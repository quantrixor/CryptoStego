from crypto_stego_utils import generate_key, encrypt_message, decrypt_message, embed_message_in_image, \
    extract_message_from_image
import base64

def encrypt_and_embed():
    input_image_path = input("Введите путь к оригинальному изображению: ")
    output_image_path = input("Введите путь для сохранения модифицированного изображения: ")
    message = input("Введите сообщение для шифрования и встраивания в изображение: ")

    encryption_key = generate_key()

    encrypted_message = encrypt_message(message, encryption_key)
    print(f"Зашифрованное сообщение: {encrypted_message}")

    message_base64 = base64.urlsafe_b64encode(encrypted_message).decode('utf-8')

    embed_message_in_image(input_image_path, message_base64.encode(), output_image_path)
    print(f"Сообщение было встроено в изображение: {output_image_path}")

    # Сохраняем ключ шифрования в файл, чтобы его можно было использовать для дешифрования
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(encryption_key)

def extract_and_decrypt():
    encrypted_image_path = input("Введите путь к изображению с зашифрованным сообщением: ")

    # Загрузка ключа шифрования из файла
    try:
        with open("encryption_key.key", "rb") as key_file:
            encryption_key = key_file.read()
    except FileNotFoundError:
        print("Файл ключа не найден. Убедитесь, что ключ находится в той же директории, что и программа.")
        return

    extracted_encrypted_message_base64 = extract_message_from_image(encrypted_image_path)
    extracted_encrypted_message_bytes = base64.urlsafe_b64decode(extracted_encrypted_message_base64.encode('utf-8'))

    decrypted_message = decrypt_message(extracted_encrypted_message_bytes, encryption_key)
    print(f"Дешифрованное сообщение: {decrypted_message}")


def main():
    choice = input(
        "Введите '1' для шифрования и встраивания сообщения в изображение или '2' для извлечения и дешифрования сообщения из изображения: ")
    if choice == '1':
        encrypt_and_embed()
    elif choice == '2':
        extract_and_decrypt()
    else:
        print("Неверный ввод. Пожалуйста, введите '1' или '2'.")


if __name__ == "__main__":
    main()
