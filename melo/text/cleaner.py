from . import chinese, english, chinese_mix, korean, french, spanish
from . import cleaned_text_to_sequence
import copy

def load_japanese():
  from . import japanese
  return japanese

def get_module_from_language(language):
  if language == "JP":
    return load_japanese()
  else:
    language_module_map = {
          "ZH": chinese, 
          "EN": english, 
          'ZH_MIX_EN': chinese_mix, 
          'KR': korean, 
          'FR': french, 
          'SP': spanish, 
          'ES': spanish
      }
    return language_module_map[language]


def clean_text(text, language):
    language_module = get_module_from_language(language)
    norm_text = language_module.text_normalize(text)
    phones, tones, word2ph = language_module.g2p(norm_text)
    return norm_text, phones, tones, word2ph


def clean_text_bert(text, language, device=None):
    language_module = get_module_from_language(language)
    norm_text = language_module.text_normalize(text)
    phones, tones, word2ph = language_module.g2p(norm_text)
    
    word2ph_bak = copy.deepcopy(word2ph)
    for i in range(len(word2ph)):
        word2ph[i] = word2ph[i] * 2
    word2ph[0] += 1
    bert = language_module.get_bert_feature(norm_text, word2ph, device=device)
    
    return norm_text, phones, tones, word2ph_bak, bert


def text_to_sequence(text, language):
    norm_text, phones, tones, word2ph = clean_text(text, language)
    return cleaned_text_to_sequence(phones, tones, language)


if __name__ == "__main__":
    pass
