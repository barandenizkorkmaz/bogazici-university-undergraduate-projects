import numpy as np
import numpy.linalg as linalg

def k_means(data,k,N):
    np.random.seed(1)
    x_min, x_max, y_min, y_max = get_range(data)
    centroids = get_initial_centroids(k,x_min,x_max,y_min,y_max)
    labels = list()
    for i in range(N):
        labels = get_clusters(data,centroids)
        centroids = get_centroids(k,data,labels)
    return centroids, labels

def get_range(data):
    data_t = np.transpose(data)
    x_min, x_max = min(data_t[0]),max(data_t[0])
    y_min, y_max = min(data_t[1]),max(data_t[1])
    return x_min, x_max, y_min, y_max

def get_initial_centroids(k,x_min,x_max,y_min,y_max):
    centroids = []
    for i in range(k):
        x = np.random.uniform(x_min, x_max)
        y = np.random.uniform(y_min, y_max)
        centroids.append((x,y))
    return centroids

def get_clusters(data,centroids):
    labels = list()
    for point in data:
        distance = list()
        for centroid in centroids:
            distance.append(linalg.norm(np.array(point)-np.array(centroid)))
        class_number = distance.index(min(distance))
        labels.append(class_number)
    return labels

def get_centroids(k,data,labels):
    centroids = list()
    counts = np.zeros(k)
    for i in range(k):
        centroids.append((0.0,0.0))
    for point, y in zip(data, labels):
        tmp = list(centroids[y])
        tmp[0] += point[0]
        tmp[1] += point[1]
        centroids[y] = (tmp[0],tmp[1])
        counts[y] += 1
    for i in range(len(centroids)):
        tmp = list(centroids[i])
        tmp[0] = tmp[0] /counts[i]
        tmp[1] = tmp[1] / counts[i]
        centroids[i] = (tmp[0],tmp[1])
    return centroids