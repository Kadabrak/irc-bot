from translate import Translator

def translate_sentence(lang_income,lang_out,sentence):
    sentence = ' '.join(sentence)
    translator = Translator(from_lang=lang_income,to_lang=lang_out)
    translation = translator.translate(sentence)
    return translation


