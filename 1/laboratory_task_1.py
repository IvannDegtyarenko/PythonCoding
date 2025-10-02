import argparse
import re
from collections import defaultdict, Counter

# Количество сиволов 
def count_characters(text):
    return len(text)

# Количество слов
def count_words(text):
    words = re.findall(r'\b\w+\b', text)
    return len(words)

# Количество предложений
def count_sentences(text):
    pattern = r'[^.!?]*(?:\.{3}|[.!?])(?![.!?])'
    sentences = re.findall(pattern, text)
    return len(sentences)

# Количество чисел
def count_numbers(text):
    numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
    return len(numbers)

# Распределение слов по их длине.
def word_length_distribution(text):
    words = re.findall(r'\b\w+\b', text) 
    length_dist = defaultdict(int)   

    for word in words:
        length = len(word)
        length_dist[length] += 1
    
    sorted_dist = dict(sorted(length_dist.items()))
    return sorted_dist

# Средняя и максимальная длина слова
def word_length_stats(text):
    words = re.findall(r'\b\w+\b', text)
    if not words:
        return 0, 0
    
    lengths = [len(word) for word in words]
    avg_length = sum(lengths) / len(lengths)
    max_length = max(lengths)
    
    return avg_length, max_length

# Распределение частот букв в тексте
def letter_frequency_distribution(text):
    letters = re.findall(r'[a-zA-Zа-яА-ЯёЁ]', text.lower())
    frequency_dist = Counter(letters)
    
    sorted_dist = dict(frequency_dist.most_common())
    return sorted_dist

# Топ-N самых частых слов, исключая стоп-слова
def top_frequent_words(text, exclude_words=None, top_n=10):
   
    if exclude_words is None:
        exclude_words = {
            'и', 'или', 'то', 'это', 'в', 'на', 'с', 'по', 'за', 'под', 'над', 
            'от', 'до', 'из', 'у', 'о', 'об', 'но', 'а', 'же', 'ли', 'бы', 'б', 
            'как', 'что', 'чтобы', 'когда', 'где', 'куда', 'откуда', 'почему', 
            'зачем', 'какой', 'который', 'чей', 'сколько', 'не', 'ни', 'да', 'нет',
            'он', 'она', 'оно', 'они', 'я', 'ты', 'вы', 'мы', 'себя', 'мой', 'твой',
            'его', 'её', 'их', 'наш', 'ваш', 'свой', 'кто'
        }
    words = re.findall(r'\b[а-яёa-z]+\b', text.lower())
    
    filtered_words = [
        word for word in words 
        if word not in exclude_words and len(word) > 1
    ]
    
    word_freq = Counter(filtered_words)
    return word_freq.most_common(top_n)

# Генерирует n-граммы из списка слов
def generate_ngrams(words, n):

    if len(words) < n:
        return []  
    total_ngrams = len(words) - n + 1
    ngrams_result = []
    
    for start_index in range(total_ngrams):
        word_group = words[start_index:start_index + n]
        
        ngram_text = ' '.join(word_group)
        
        ngrams_result.append(ngram_text)
    
    return ngrams_result

# Tоп-N самых частых n-грамм в тексте.
def top_ngrams(text, n=2, top_n=10):

    words = re.findall(r'\b[а-яёa-z]+\b', text.lower()) 
    ngrams_list = generate_ngrams(words, n) 
    ngram_freq = Counter(ngrams_list)
    
    return ngram_freq.most_common(top_n)

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
    
    length_dist = word_length_distribution(text)
    print("\nРаспределение длин слов:")
    for length, count in length_dist.items():
        print(f"  Длина {length}: {count} слов")

    avg_len, max_len = word_length_stats(text)
    print(f"\nСредняя длина слова: {avg_len:.2f}")
    print(f"Максимальная длина слова: {max_len}")

    print("\nРаспределение частот букв (отсортировано по убыванию частоты):")
    freq_dist = letter_frequency_distribution(text)
    
    total_letters = sum(freq_dist.values())
    print(f"Всего букв в тексте: {total_letters}")
    print("Частоты букв:")
        
    for i, (letter, count) in enumerate(freq_dist.items(), 1):
        percentage = (count / total_letters) * 100
        print(f"  {i:2d}. Буква '{letter}': {count:4d} раз ({percentage:5.2f}%)")

    print("\n")
    print("Топ-10 самых частых слов (без стоп-слов):")
    top_words = top_frequent_words(text, top_n=10)
    
    for i, (word, count) in enumerate(top_words, 1):
        print(f"  {i:2d}. Слово '{word}': {count:2d} раз")
    
    print("\n")
    print("Топ-10 биграмм (пар соседних слов):")
    bigrams = top_ngrams(text, n=2, top_n=10)
    
    for i, (bigram, count) in enumerate(bigrams, 1):
        print(f"  {i:2d}. Биграмма '{bigram}': {count:1d} раз")
    
    print("\n")
    print("Топ-10 триграмм (троек соседних слов):")
    trigrams = top_ngrams(text, n=3, top_n=10)
    
    for i, (trigram, count) in enumerate(trigrams, 1):
            print(f"  {i:2d}. Триграмма '{trigram}': {count:1d} раз")
    
if __name__ == '__main__':
    main()
