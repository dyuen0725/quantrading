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
            
for doc_tokens in iter_documents('.'):
    print('\nNext document:\n')
    for token in doc_tokens:
        print(token)
        
class TxtSubdirsCorpus(object):
    """This class instantiates an iterable: On each iteration, return
    bag-of-words vectors, one vector for each document. Process one
    document at a time using generators, never load the entire corpus
    into RAM.

    """
    def __init__(self, top_dir): # Constructor method.
        self.top_dir = top_dir
        # Create a dictionary, which is a mapping for documents to
        # sparse vectors.
        self.dictionary = gensim.corpora.Dictionary(iter_documents(top_dir))
        once_ids = [tokenid for tokenid, docfreq in self.dictionary.dfs.items() if docfreq == 1]
        self.dictionary.filter_tokens(once_ids)
        self.dictionary.compactify()
 
    def __iter__(self):         # Define a generator function.
        for doc_tokens in iter_documents(self.top_dir):
            # Transform tokens (strings) into a sparse bag-of-words
            # vector, one document at a time.
            yield self.dictionary.doc2bow(doc_tokens)
            
corpus = TxtSubdirsCorpus('.')

for vector in corpus:
    print(vector)
    
from gensim.models.lsimodel import stochastic_svd as svd
u, s = \
    svd(
        corpus,
        rank = 5,
        num_terms = len(corpus.dictionary),
        chunksize = 5000)
    
model = gensim.models.lsimodel.LsiModel(corpus = corpus, id2word = corpus.dictionary)    
print(model.show_topics())
print(model.projection.u)
print(model.projection.s)