from deep_translator import GoogleTranslator

translated = GoogleTranslator(source='auto', target='en').translate('привет ')
print(translated)