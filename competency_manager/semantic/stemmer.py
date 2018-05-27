from typing import List, Dict, Optional, Union
from pymystem3 import Mystem

stemmer = Mystem()


def _convert_word(word: Dict) -> Optional[str]:
    analysis = word.get('analysis')
    if analysis:
        analysis = analysis[0]
        assert len(analysis) == 2 or len(analysis) == 3 and 'qual' in analysis, word
        lex = analysis['lex']
        gr = analysis['gr']
        gr = gr.split('=')
        assert len(gr) == 2, word
        gr = gr[0].split(',')[0]
        if gr in 'ASV':
            return lex + {'A': '_ADJ', 'S': '_NOUN', 'V': '_VERB'}[gr]
    return None


def stem_text(text: Union[str, List[str]]) -> str:
    if type(text) is list:
        text = '. '.join(text)
    text = text.replace('\r', ' ').replace('\n', ' ')
    analyzed_words = stemmer.analyze(text)
    stemmed_words = []
    for analyzed_word in analyzed_words:
        stemmed_word = _convert_word(analyzed_word)
        if stemmed_word:
            stemmed_words.append(stemmed_word)
    return ' '.join(stemmed_words)
