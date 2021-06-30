from modules.FreeTranslator import FreeTranslator
from settings import *

contents = open(FILENAME, 'r', encoding='utf-8').read().splitlines()
contents = [f[:5000] for f in contents if f]

Translator = FreeTranslator('https://translate.google.com/?hl=pt&sl=pt&tl=en&op=translate')
Translator.open()
Translator.getTextArea()

translated = []
def save_translated_at(FILENAME, translated):
    FILENAME = FILENAME[:-4] + '_translated.txt'
    with open(FILENAME, 'w') as file:
        [file.write(t+'\n') for t in translated]


qt = len(contents)
errors = 0
for i, content in enumerate(contents):
    print(f'{i+1} de {qt}')
    try:
        Translator.sendText(content)
        response = Translator.getResponse()
        if response:
            response = response.replace('\n', '')
            translated.append(response)
        else:
            print(f'cannot to translate "{content}"')
            errors += 1
        Translator.cleanTextArea()
    except Exception as e:
        print('error!:',str(e))
        errors += 1
        save_translated_at(translated)


save_translated_at(FILENAME, translated)
Translator.close()

print(f'Translated {len(translated)}/{qt} inputs, with {errors} errors. I would really like to you give me some feedback! Contact me! 😊')