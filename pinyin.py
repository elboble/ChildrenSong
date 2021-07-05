from pypinyin import lazy_pinyin,TONE2,TONE
import jieba
# import gensim
import os

# res = lazy_pinyin("单田芳",style=TONE)

# res = list(jieba.cut_for_search("先帝创业未半而中道崩殂"))

# print(res)

# print(os.path.abspath('./'))

#
# import jieba
# from gensim import corpora
# from gensim import models
# from gensim import similarities
#
# l1 = ["你的名字是什么", "你今年几岁了", "你有多高你胸多大", "你胸多大"]
# a = "你今年多大了"
#
# all_doc_list = []
# for doc in l1:
#     doc_list = [word for word in jieba.cut_for_search(doc)]
#     all_doc_list.append(doc_list)
# doc_test_list = [word for word in jieba.cut_for_search(a)]
#
#
# dictionary = corpora.Dictionary(all_doc_list)  # 制作词袋
# corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
# doc_test_vec = dictionary.doc2bow(doc_test_list)

# lsi = models.LsiModel(corpus)
# index = similarities.SparseMatrixSimilarity(lsi[corpus], num_features=len(dictionary.keys()))
# sim = index[lsi[doc_test_vec]]
# cc = sorted(enumerate(sim), key=lambda item: -item[1])
# text = l1[cc[0][0]]
# print(a,text)

# from ai.my_simnet import my_simnet
#
# print(my_simnet('幸福的家'))