#coding=utf-8
"""数据预处理"""
from gensim import corpora, models


def preprocessing(documents):
    """数据预处理的方法"""
    # 分离标点的token化
    from nltk.tokenize import word_tokenize
    texts_tokenized = [[word.lower() for word in word_tokenize(document.decode('utf-8'))] for document in documents]
    # print texts_tokenized[0]
    # 删除停用词
    from nltk.corpus import stopwords
    english_stopwords = stopwords.words('english')
    texts_filtered_stopwords = [[word for word in document if not word in english_stopwords] for document in texts_tokenized]
    # print texts_filtered_stopwords[0]
    # 删除英文标点
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    texts_filtered = [[word for word in document if not word in english_punctuations] for document in texts_filtered_stopwords]
    # 词干化
    # from nltk.stem.lancaster import LancasterStemmer
    # st = LancasterStemmer()
    # texts_stemmed = [[st.stem(word) for word in document] for document in texts_filtered]
    # print texts_stemmed[:10]
    # 删除低频次，频率=1
    # all_stems = sum(texts_filtered, [])
    # stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
    # texts = [[stem for stem in text if stem not in stems_once] for text in texts_filtered]
    # print texts[0]
    return texts_filtered


def calc_tfidf(texts, dictionary):
    corpus = [dictionary.doc2bow(text) for text in texts]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    return corpus_tfidf


def get_dict(texts):
    return corpora.Dictionary(texts)

if __name__ == '__main__':
    preprocessing()