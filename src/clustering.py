import numpy as np
import copy

import warnings
warnings.filterwarnings('ignore')

# distance functions
def cosine_dist(x, y):
    return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))
def euc_dist(x,y):
    return np.sqrt(np.sum((x - y) ** 2))
def manhattan_distance(a,b):
    return np.sum(np.abs(np.subtract(a,b)))

class kmeans(object):

    def __init__(self,k=2, measure='euc', maxIters=100, random_seed=101):
        self.setDistanceMeasure(measure)
        self.centroid_count = k
        self.maxIters = maxIters
        self.seed=101

    def fit(self, X, labels=None, tol=1e-3):
        ''' clusters X data '''
        np.random.seed(self.seed)

        # copy and normalize data
        X = np.array(copy.deepcopy(X))
        X = np.subtract(X,np.min(X, axis=0, keepdims=True))
        X = np.divide(X, np.subtract(np.max(X, axis=0, keepdims=True),np.min(X, axis=0, keepdims=True)))

        # init centriod positions to random instance
        centroids = X[np.random.choice(len(X), self.centroid_count, replace=False)]

        iter_count = 0
        prev_centroids = centroids + 1
        while (np.abs(prev_centroids - centroids) > tol).any():
            
            # reset clusters
            clusters = [[] for _ in centroids]
        
            # find best cluster for each data point
            self.train_labels = []
            for x in X:
                distances = [self.distFunc(x,c) for c in centroids]
                closest_cluster = np.argmin(distances)
                self.train_labels.append(closest_cluster)
                clusters[closest_cluster].append(x)

            # get new center points
            new_centers = []    
            for clust in clusters:
                new_centers.append(np.array(np.average(clust, axis=0)))
            
            # save old centers for comparison
            # ensure new centers are valid
            prev_centroids = copy.deepcopy(centroids)
            for k in range(self.centroid_count):
                if not (np.isnan(new_centers[k])).any():
                    centroids[k] = new_centers[k] 

            # stop if max iters
            if iter_count>=self.maxIters: break
            iter_count+=1

        self.centroids = centroids

    def predict(self):
        ''' TBD '''
        pass

    def setDistanceMeasure(self, measure):
        '''
            Set the distance function to be used

            params:
                measure (str):
                    Defines the type of distance measure to be used
                    MUST be:
                        'euc' --> euclidian distance
                        'cosine' --> cosine distance
                        'manhat' --> manhattan distance
        '''
        if measure == 'euc':
            self.distFunc = euc_dist
        elif measure == 'cosine':
            self.distFunc = cosine_dist
        elif measure == 'manhat':
            self.distFunc = manhattan_distance
        else:
            raise ValueError(f"Invalid distance measure selected {measure}\n \
                            MUST be one of \'euc\', \'cosine\' or \'manhat\'")

