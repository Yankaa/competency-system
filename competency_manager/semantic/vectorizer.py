from numpy import array, ndarray
import gensim
from typing import List
from gensim.models.word2vec import Word2VecKeyedVectors as Model


def get_model() -> Model:
    file_name = 'ruscorpora_upos_skipgram_300_5_2018.vec.gz'
    model: Model = gensim.models.KeyedVectors.load_word2vec_format(file_name)
    model.init_sims(replace=True)
    return model


def mean(arr: List[ndarray]) -> ndarray:
    return gensim.matutils.unitvec(array(arr).mean(axis=0))


model = get_model()


def vectorize_string(stemmed_string: str) -> ndarray:
    word_vectors = []
    for word in stemmed_string.split():
        try:
            word_vectors.append(model.word_vec(word))
        except KeyError:
            pass
    return mean(word_vectors)
