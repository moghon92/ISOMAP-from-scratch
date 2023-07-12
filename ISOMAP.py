import os
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from scipy.sparse.csgraph import shortest_path
import seaborn as sns
import scipy.sparse.linalg as ll
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

####################### Q3a ###############################
## read the imags
file_path = os.getcwd() + '\\data\\isomap.mat'
matFile = sio.loadmat(file_path)
data = matFile['images'].T

m = data.shape[0]

# pick ebsilon
ebs = 12

#calc eucludian distances
distmat = pairwise_distances(data)
#calc adjacency matrix
A = distmat * (distmat <= ebs).astype(int)
# shortest path matrix
D = shortest_path(A, directed=False)
plt.figure(0)
plt.spy(A)
plt.title('Adjacency Matrix')
plt.savefig('ISOMAP_q3a_adjacency.png')

plt.figure(1)
mask_ut = np.triu(np.ones(D.shape)).astype(bool)
sns.heatmap(D, mask=mask_ut)
plt.title('Shortest Distance plot')
plt.savefig('ISOMAP_q3a_distance.png')

####################### Q3b ###############################
# centring matrix and C
ones = np.dot(np.ones(m).reshape(m,1), np.ones(m).reshape(1,m))
H = np.identity(m) - ((1/m)*ones)
C=(-1/2)*(H@(D*D)@H)

# calc top 2 eigenvals and vecs
K=2
S, W = ll.eigs(C, k=K)
S = S.real
W = W.real

#calc projctions
Z = W@np.diag(np.sqrt(S))

def getImage(index):
    return OffsetImage((data[index].reshape(64,64)), zoom=.3, alpha = 1)
#plot
fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
ax.scatter(Z[:, 0], Z[:, 1])
for index in  np.random.randint(0, m, 40):
    ab = AnnotationBbox(getImage(index), (Z[index,0], Z[index,1]), frameon=False)
    ax.add_artist(ab)

plt.title('ISOMAP')
plt.savefig('ISOMAP_q3b_faces.png')

####################### Q3c ###############################

import PCA
PC1, PC2 = PCA.performPCA(data, normalize=False, use_SVD=False)

# plot
fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
ax.scatter(PC1, PC2)
for index in np.random.randint(0, m, 40):
    ab = AnnotationBbox(getImage(index), (PC1[index], PC2[index]), frameon=False)
    ax.add_artist(ab)


plt.title('PCA')
plt.savefig('ISOMAP_q3c_PCA.png')
# plt.show()