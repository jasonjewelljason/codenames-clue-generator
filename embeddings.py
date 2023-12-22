# Taken from my a5.

import math
import numpy as np
from tqdm import tqdm

class Embeddings:

    def __init__(self, glove_file = 'glove.42B.300d.filtered.txt'):
        
        self.embeddings = {}
        for line in tqdm(open(glove_file), total=108947, desc='Loading GloVe vectors'):
            row = line.split()
            word = row[0]
            vals = np.array([float(x) for x in row[1:]])
            self.embeddings[word] = vals
        
    def __getitem__(self, word):
        return self.embeddings[word]

    def __contains__(self, word):
        return word in self.embeddings

    def vector_norm(self, vec):
        """
        Calculate the vector norm (aka length) of a vector.

        Parameters
        ----------
        vec : np.array
            An embedding vector.

        Returns
        -------
        float
            The length (L2 norm, Euclidean norm) of the input vector.
        """
        return math.sqrt(np.sum(vec**2))

    def cosine_similarity(self, v1, v2):
        """
        Calculate cosine similarity between v1 and v2; these could be
        either words or numpy vectors.

        If either or both are words (e.g., type(v#) == str), replace them 
        with their corresponding numpy vectors before calculating similarity.

        Parameters
        ----------
        v1, v2 : str or np.array
            The words or vectors for which to calculate similarity.

        Returns
        -------
        float
            The cosine similarity between v1 and v2.
        """
        if type(v1) == str:
            vec1 = self.__getitem__(v1)
        else:
            vec1 = v1
        if type(v2) == str:
            vec2 = self.__getitem__(v2)
        else:
            vec2 = v2
        
        return (vec1 @ vec2) / (self.vector_norm(vec1) * self.vector_norm(vec2))

    def most_similar(self, vec, n = 5, exclude = []):
        """
        Return the most similar words to `vec` and their similarities. 
        As in the cosine similarity function, allow words or embeddings as input.


        Parameters
        ----------
        vec : str or np.array
            Input to calculate similarity against.

        n : int
            Number of results to return. Defaults to 5.

        exclude : list of str
            Do not include any words in this list in what you return.

        Returns
        -------
        list of ('word', similarity_score) tuples
            The top n results.        
        """
        if type(vec) == str:
            vec = self.__getitem__(vec)

        similarity_list = []
        for word in self.embeddings:
            if word not in exclude:
                similarity_list.append((word, self.cosine_similarity(self.embeddings[word], vec)))
        similarity_list.sort(key=lambda a: a[1], reverse=True)
        return similarity_list[:n]

if __name__ == '__main__':
    
    embeddings = Embeddings()
    # word = 'mercury'
    # print(f'Most similar to {word}:')
    # for item in embeddings.most_similar(word, exclude=[word], n=20):
    #     print('\t',item[0], '\t', item[1])

    # print(len(embeddings.embeddings))


