import random
import re
import argparse
import pytest
import os

def read_and_clean_text(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='cp1251') as file:
            text = file.read()
    words = re.findall(r'[А-Яа-яA-Za-z]+', text)
    return words

def build_chain(words, n=2):
    chain = {}
    for i in range(len(words) - n + 1):
        key = tuple(words[i:i+n-1])
        value = words[i+n-1]
        if key in chain:
            chain[key].append(value)
        else:
            chain[key] = [value]
    return chain

def generate_text(chain, length, n=2, seed=None):
    if seed is not None:
        random.seed(seed)
    valid_starts = [k for k in chain.keys() if k[0][0].isupper()]
    if not valid_starts:
        valid_starts = list(chain.keys())
    current_state = random.choice(valid_starts)
    result = list(current_state)
    for _ in range(length - n + 1):
        if current_state not in chain:
            break
        next_word = random.choice(chain[current_state])
        result.append(next_word)
        current_state = tuple(result[-(n-1):])
    return ' '.join(result)

def main():
    parser = argparse.ArgumentParser(description="Генератор текста на цепях Маркова")
    parser.add_argument("filename", help="Имя файла с исходным текстом")
    parser.add_argument("length", type=int, help="Длина текста")
    parser.add_argument("-n", "--size", type=int, default=2, help="Размер цепочки")
    args = parser.parse_args()
    try:
        words = read_and_clean_text(args.filename)
        if not words:
            print("Ошибка: файл пуст.")
            return
        chain = build_chain(words, args.size)
        generated = generate_text(chain, args.length, args.size)
        print(f"\n--- Сгенерированный текст (n={args.size}) ---\n")
        print(generated)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{args.filename}' не найден.")

@pytest.fixture
def temp_text_file(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Привет мир. Как дела? Привет мир!", encoding="utf-8")
    return str(file_path)

def test_read_and_clean_text(temp_text_file):
    words = read_and_clean_text(temp_text_file)
    assert words == ["Привет", "мир", "Как", "дела", "Привет", "мир"]

def test_build_chain():
    words = ["Привет", "мир", "Привет", "мир", "Как", "дела"]
    chain = build_chain(words, n=2)
    assert chain[("Привет",)] == ["мир", "мир"]
    assert chain[("мир",)] == ["Привет", "Как"]

def test_generate_text_length_and_start():
    words = ["Привет", "мир", "Привет", "мир", "Как", "дела", "Хорошо"]
    chain = build_chain(words, n=2)
    text = generate_text(chain, length=4, n=2, seed=42)
    assert len(text.split()) <= 4
    assert text[0].isupper()

def test_generate_text_dead_end():
    words = ["Начало", "истории", "тут", "конец"]
    chain = build_chain(words, n=2)
    text = generate_text(chain, length=10, n=2, seed=1)
    assert len(text.split()) < 10

if __name__ == '__main__':
    # Если запускаем файл напрямую без аргументов,
    # он может случайно запустить pytest, поэтому ловим ошибку
    import sys
    if "pytest" in sys.modules:
        pass
    else:
        main()