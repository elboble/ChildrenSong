import jieba
from gensim import corpora
from gensim import models
from gensim import similarities
from setting import MONGO_DB


# print("init gensim")
all_doc_list = []
gensim_l1 = [item.get('title') for item in MONGO_DB.erge.find({})]
for doc in gensim_l1:
    doc_list = [word for word in jieba.cut_for_search(doc)]
    all_doc_list.append(doc_list)

gensim_dictionary = corpora.Dictionary(all_doc_list)  # 制作词袋
corpus = [gensim_dictionary.doc2bow(doc) for doc in all_doc_list]
gensim_lsi = models.LsiModel(corpus)

gensim_index = similarities.SparseMatrixSimilarity(gensim_lsi[corpus], num_features=len(gensim_dictionary.keys()))
# print(gensim_dictionary,gensim_index,gensim_lsi)


def do_simnet(a):

    doc_test_list = [word for word in jieba.cut_for_search(a)]
    # global gensim_dictionary
    doc_test_vec = gensim_dictionary.doc2bow(doc_test_list)
    # global gensim_index
    sim = gensim_index[gensim_lsi[doc_test_vec]]

    cc = sorted(enumerate(sim), key=lambda item: -item[1])
    print(cc)
    if cc[0][1] == 0:
        return None
    text = gensim_l1[cc[0][0]]
    return text

# init_gensim()
# print(my_simnet("我要听祝你新年快乐"))