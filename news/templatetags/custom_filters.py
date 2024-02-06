import json
from django import template

register = template.Library()

@register.filter()
def censor(text: str) -> str:
    """Функция цензуры. Загружает готовый json с сортированным словарем нецензурных слов,
    в котором ключ является первой буквой. Функция в первом цикле создает словарь из слов,
    пробелов и знаков препинания. Второй цикл сверяет слова и заменяет все буквы кроме первой '*'.
    Затем объединяет элементы исправленного словаря в текст"""
    #todo Попробую приметь в функции регулярные выражения как разберусь.
    #todo Переместить данную функцию в models.py. Пусть цензурит лишь раз при сохранение текста в бд.
    # лишний код лишня работа процессора. Если весь текст на страницах будет только из бд.
    try:
        with open('news/templatetags/json_mat.txt', 'r', encoding='utf8') as f:
            json_in = json.loads(f.read())
            edited = []
            word = ''
            for letter in text:
                if letter.isalpha():
                    word += letter
                else:
                    if word:
                        edited.append(word)
                    word = ''
                    edited.append(letter)
            for i, w in enumerate(edited):
                if w[0].isalpha():
                    if w[0] in json_in:
                        if w.lower() in json_in[w[0].lower()]:
                            edited[i] = w[0] + '*' * (len(w) - 1)
            text = "".join(edited)
            return text
    except Exception as e:
        print('Terminal message:\n'
              'From censor news.templatetags.custom_filters\n'
              'Error == ', e)
    finally:
        return text



def new_censor(new_censors: list[str]) -> None:
    """Для добавления новых цензурных слов в файл json_mat.txt"""
    with open('json_mat.txt', 'r', encoding='utf8') as f:
        f = f.read()
        json_in = json.loads(f)
        for w in new_censors:
            if w not in json_in[w[0].lower()]:
                json_in[w[0].lower()].append(w.lower())
        json_out = json.dumps(json_in)

    with open('json_mat.txt', 'w', encoding='utf8') as f:
        f.write(json_out)


