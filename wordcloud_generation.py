#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 16:06:16 2019

@author: dominic
"""

import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import gensim, os

def iter_documents(top_directory):
    """This is a generator function: Iterate over all documents, yielding
    one tokenized document (=list of utf8 tokens) at a time. Each
    document corresponds to one file. The generator function finds all
    `.txt` files, no matter how deep under `top_directory`.

    """
    for root, dirs, files in os.walk(top_directory):
        for fname in filter(lambda fname: fname.endswith('.txt'), files):
            # Read each `.txt` document as one big string.
            document = open(os.path.join(root, fname)).read()
            # Break document into utf8 tokens.
            yield gensim.parsing.preprocessing.preprocess_string(document)

#setup stopwords for the wordcloud
stopwords = set(STOPWORDS)
stopwords.update(['hong', 'kong', 'said', 'govern'])

#wordcloud generation
wordcloud = WordCloud(stopwords = stopwords).generate(" ".join(word for lst in iter_documents('.') for word in lst))

#plotting the wordcloud
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()    