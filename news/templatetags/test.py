# для теста на ValueError
import json

def censor(text: str) -> str:
    try:
        with open('json_mat.txt', 'r', encoding='utf8') as f:
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

print(censor(121))


