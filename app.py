from flask import Flask
app = Flask(__name__)

import numpy as np, json
from sklearn.preprocessing import normalize
from flask import render_template
import requests


class WikiEmbedding:
    def __init__(self, fname):

        self.w2idx = {}
        self.idx2w = []

        with open(fname, 'rb') as f:
            try:
                m, n = next(f).decode('utf8').strip().split(' ')
                self.E = np.zeros((int(m), int(n)))

                for i, l in enumerate(f):
                    l = l.decode('utf8').strip().split(' ')
                    w = l[0]
                    self.E[i] = np.array(l[1:])
                    self.w2idx[w] = i
                    self.idx2w.append(w)
            except:
                pass

        self.E = normalize(self.E)
        self.idx2w = np.array(self.idx2w)

    def most_similar(self, w, n=10, min_similarity=0.5):
        """
        Find the top-N most similar words to w, based on cosine similarity.
        As a speed optimization, only consider neighbors with a similarity
        above min_similarity
        """

        if type(w) is str:
            w = self.E[self.w2idx[w]]

        scores = self.E.dot(w)
        # only consider neighbors above threshold
        min_idxs = np.where(scores > min_similarity)
        ranking = np.argsort(-scores[min_idxs])[1:(n + 1)]
        nn_ws = self.idx2w[min_idxs][ranking]
        nn_scores = scores[min_idxs][ranking]
        return list(zip(list(nn_ws), list(nn_scores)))

def hello():
    en_embedding = WikiEmbedding('2017-01-01_2017-01-30_en_100')
    return json.dumps(en_embedding.most_similar('Word2vec', n=10))


@app.route("/")
def index():
    """ Request ..."""
    return render_template("index.html", data=hello())

if __name__ == "__main__":
    app.run(port=5050)
