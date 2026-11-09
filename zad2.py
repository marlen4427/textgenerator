import random
import re


def read_and_clean_text(filename):
    """Читает файл и оставляет только слова (убирает пунктуацию)."""
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
    # Оставляем только буквы (кириллица и латиница)
    words = re.findall(r'[А-Яа-яA-Za-z]+', text)
    return words


def build_chain(words, n=2):
    """Строит словарь цепочек Маркова для n слов."""
    chain = {}
    for i in range(len(words) - n + 1):
        # Ключ - это n-1 слов. Значение - список слов, которые идут после
        key = tuple(words[i:i + n - 1])
        value = words[i + n - 1]

        if key in chain:
            chain[key].append(value)
        else:
            chain[key] = [value]
    return chain


def generate_text(chain, length, n=2):
    """Генерирует текст заданной длины."""
    # Ищем ключи, которые начинаются с заглавной буквы
    valid_starts = [k for k in chain.keys() if k[0][0].isupper()]

    if not valid_starts:
        valid_starts = list(chain.keys())  # если заглавных нет, берем любые

    current_state = random.choice(valid_starts)
    result = list(current_state)

    for _ in range(length - n + 1):
        # Если такого ключа нет в словаре (тупик), прерываем генерацию
        if current_state not in chain:
            break

        next_word = random.choice(chain[current_state])
        result.append(next_word)

        # Сдвигаем окно (для n=2 берем последнее слово, для n=3 — последние два)
        current_state = tuple(result[-(n - 1):])

    return ' '.join(result)


if __name__ == '__main__':
    print("=== Генератор текста на цепях Маркова ===")

    # Запрашиваем данные у пользователя
    filename = input("Введите имя файла с текстом (например, text1.txt): ")

    # Обрабатываем возможные ошибки ввода для длины
    while True:
        try:
            length = int(input("Введите желаемую длину текста в словах (например, 50): "))
            break
        except ValueError:
            print("Ошибка: нужно ввести целое число. Попробуйте еще раз.")

    # Обрабатываем возможные ошибки ввода для размера цепочки
    while True:
        try:
            n = int(input("Введите размер цепочки (2 или 3): "))
            if n >= 2:
                break
            else:
                print("Цепочка должна состоять хотя бы из 2 слов. Попробуйте еще раз.")
        except ValueError:
            print("Ошибка: нужно ввести целое число. Попробуйте еще раз.")

    print("\nЧитаем файл и генерируем текст... Пожалуйста, подождите.\n")

    try:
        words = read_and_clean_text(filename)
        if not words:
            print("Ошибка: файл пуст или в нем не найдено слов.")
        else:
            chain = build_chain(words, n)
            generated = generate_text(chain, length, n)

            print(f"--- Сгенерированный текст (n={n}) ---\n")
            print(generated)
    except FileNotFoundError:
        print(f"\nОшибка: Файл '{filename}' не найден. Убедитесь, что он лежит в папке с программой.")