import numpy as np
import scipy.linalg as la

def standardize(data):
    data_t = np.transpose(data)
    for i,row in enumerate(data_t):
        mean = np.mean(row)
        stdev = np.std(row)
        for j,elem in enumerate(row):
            new_elem = (elem-mean)/stdev
            data[j][i] = new_elem
    return data

def get_eigen_vectors(data):
    standardized_pca_data_x = standardize(data)
    covariance_matrix = np.transpose(standardized_pca_data_x).dot(np.array(standardized_pca_data_x))*(1.0/len(standardized_pca_data_x))

    results = la.eig(covariance_matrix)

    eigen_values = results[0]
    eigen_vectors = results[1]

    eigen_dict = {k: v for v, k in enumerate(eigen_values)}
    sorted_eigen_values = sorted(eigen_values,reverse=True)

    pc_matrix = []

    for eigen_value in sorted_eigen_values:
        eigen_index = eigen_dict[eigen_value]
        pc_matrix.append(eigen_vectors[:,eigen_index])

    return np.transpose(pc_matrix)

def get_transformation_matrices(eigen_vectors, d):
    transformation_matrices = []
    for current_d in d:
        transformation_matrices.append(eigen_vectors[:,0:current_d])
    return transformation_matrices

def pca(data, d):
    eigen_vectors = get_eigen_vectors(data)
    return get_transformation_matrices(eigen_vectors, d)

def transform_data(data, transformation_matrices):
    reconstructed_matrices = []
    for G in transformation_matrices:
        reconstructed_matrices.append(np.transpose(G.dot(np.transpose(G).dot(np.transpose(data)))))
    return reconstructed_matrices