# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 00:22:23 2019

@author: Dominic Yuen
"""

import gensim

# c is a stream of document vectors

id2word = \
    gensim.corpora.Dictionary.load_from_text(
        'data-wiki-en/wiki_en_wordids.txt.bz2')

lda = \
    gensim.models.ldamodel.LdaModel(
        corpus=c,
        id2word=id2word,
        num_topics=100,
        update_every=0,
        passes=20)
    
# Print the most contributing words for 10 randomly selected topics.
lda.print_topics(10)

# A trained model can used be to transform new, unseen documents
# (plain bag-of-words or tf-idf count vectors) into LDA topic
# distributions.
doc_lda = lda[doc_bow]