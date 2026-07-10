import sklearn.datasets as datasets
import sklearn.decomposition as decomposition
import matplotlib.pyplot as plt
import sklearn.cluster as cluster


data = datasets.load_iris()

# Apply PCA to reduce the dataset to 2 principal components.
pca = decomposition.PCA(n_components=2)
transformed_data = pca.fit_transform(data.data)

# Visualize the transformed data.
plt.scatter(transformed_data[:, 0], transformed_data[:, 1], c=data.target)
plt.title('PCA of Iris Dataset')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()

# Compare the PCA visualization with the clustering results.
cluster_model = cluster.KMeans(n_clusters=3, random_state=42)
cluster_model.fit(data.data)


optimal_clusters = []
for k in range(1, 11):
    kmeans = cluster.KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data.data)
    optimal_clusters.append(kmeans.inertia_)

plt.scatter(transformed_data[:, 0], transformed_data[:, 1], c=cluster_model.labels_)
plt.title('PCA of Iris Dataset with Clustering Results')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()
