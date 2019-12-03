# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 00:16:12 2019

@author: Dominic Yuen
"""

import gensim

#c is stream of document vectors

id2word = \
    gensim.corpora.Dictionary.load_from_text(
        'data-wiki-en/wiki_en_wordids.txt.bz2')

lsi = \
    gensim.models.lsimodel.LsiModel(
        corpus=c,
        id2word=id2word,
        num_topics=400)
    
# Print the words that contribute most (both positively and
# negatively) for each of the first ten topics.
lsi.print_topics(10)    