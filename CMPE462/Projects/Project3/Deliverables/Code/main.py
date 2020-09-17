import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sp
import numpy.linalg as linalg

import plot_utils
import k_means_util
import pca_utils

#
# TASK 1: K-MEANS CLUSTERING
#

N = [1,2,3,4,5,6,7,8,9]

kmeans_data = np.load("data.npy")
kmeans_labels = np.load("label.npy")

# 1.1
fig = plt.figure()
ax = fig.add_subplot(111)
plot_utils.scatter_plot_util(kmeans_data,kmeans_labels,ax)
ax.set_title("Scatter Plot: Clusters (Ground Truth)")
ax.legend(loc='lower left')
plt.show()

# 1.2
# RUN K-MEANS FOR N=12
_,cluster_labels = k_means_util.k_means(kmeans_data,k=3,N=12)
# PLOT
fig = plt.figure()
ax = fig.add_subplot(111)
plot_utils.scatter_plot_util(kmeans_data,cluster_labels,ax)
ax.set_title("Scatter Plot: Clusters (Max. Iteration = 12)")
ax.legend(loc='lower left')
plt.show()


# 1.3
fig = plt.figure()
plt.suptitle("Scatter Plot: Clusters vs Max. Iterations")
for i,max_iter in enumerate(N):
    ax = fig.add_subplot(3,3,i+1)
    _,cluster_labels = k_means_util.k_means(kmeans_data,k=3,N=max_iter)
    plot_utils.scatter_plot_util(kmeans_data,cluster_labels,ax)
    ax.set_title("N = " + str(max_iter))
    if i==len(N)-1:
        handles, legend_labels = ax.get_legend_handles_labels()
        fig.legend(handles, legend_labels, loc='lower left')
plt.show()

#
# TASK 2: PCA
#
pca_data = sp.loadmat("USPS.mat")
pca_data_x = pca_data['A']
pca_data_y = pca_data['L']

#
# TASK 2.1
#
d = [50, 100, 200]
transformation_matrices = pca_utils.pca(pca_data_x, d)

#
# TASK 2.2
#
reconstructed_matrices = pca_utils.transform_data(pca_data_x, transformation_matrices)

#
# TASK 2.3
#
image_indices = [0, 500, 1000, 2000]

fig = plt.figure()
plt.suptitle("Reconstructed Images")
for i,image_index in enumerate(image_indices):
    for j,reconstructed_matrix in enumerate(reconstructed_matrices):
        ax = fig.add_subplot(4,4,i*4+j+1)
        ax.imshow(reconstructed_matrix[image_index].reshape(16,16))
        ax.set_title('d = ' + str(d[j]))
        ax.set_ylabel('i = ' + str(image_index))
        ax.set_yticklabels([])
        ax.set_xticklabels([])
    ax = fig.add_subplot(4,4,4*(i+1))
    ax.imshow(pca_data_x[image_index].reshape(16,16))
    ax.set_title('Raw Image')
    ax.set_ylabel('i = ' + str(image_index))
    ax.set_yticklabels([])
    ax.set_xticklabels([])
plt.show()

#
# APPENDIX
#
#
# A.1: ANALYSIS of INFORMATION LOSS
#
information_loss = list()
for current_d,reconstructed_matrix in zip(d,reconstructed_matrices):
    information_loss.append(linalg.norm(pca_data_x - reconstructed_matrix,ord='fro')**2)
plot_utils.information_loss_plot(information_loss,d)