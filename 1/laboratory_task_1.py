import argparse
import re

def count_characters(text):
    return len(text)

def count_words(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def count_sentences(text):
    pattern = r'[^.!?]*(?:\.{3}|[.!?])(?![.!?])'
    sentences = re.findall(pattern, text)
    return len(sentences)

def count_numbers(text):
    numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
    return len(numbers)

def main():
    parser = argparse.ArgumentParser(description='Анализ текстового файла')
    parser.add_argument('filepath', type=str, help='Путь к файлу для анализа')
    args = parser.parse_args()

    with open(args.filepath, 'r', encoding='utf-8') as file:
        text = file.read()

    print(f"Символов: {count_characters(text)}")
    print(f"Слов: {count_words(text)}")
    print(f"Предложений: {count_sentences(text)}")
    print(f"Чисел: {count_numbers(text)}")

if __name__ == '__main__':
    main()