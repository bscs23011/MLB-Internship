import sklearn.datasets as datasets
import sklearn.cluster as cluster
import matplotlib.pyplot as plt

# Load the Iris dataset.
data = datasets.load_iris()

# Apply K-Means clustering.
cluster_model = cluster.KMeans(n_clusters=3, random_state=42)
cluster_model.fit(data.data)


# Use the Elbow Method to determine the optimal number of clusters.
optimal_clusters = []
for k in range(1, 11):
    kmeans = cluster.KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data.data)
    optimal_clusters.append(kmeans.inertia_)


print(optimal_clusters)

plt.plot(range(1, 11), optimal_clusters, marker='o')
plt.xlabel("Number of Clusters")
plt.ylabel("Inertia")
plt.title("Elbow Method")
plt.show()

# Visualize the clusters using a scatter plot.
plt.scatter(data.data[:, 0], data.data[:, 1], c=cluster_model.labels_)
plt.scatter(cluster_model.cluster_centers_[:, 0], cluster_model.cluster_centers_[:, 1], s=300, c='red', marker='X')  # Mark cluster centers
plt.title('K-Means Clustering of Iris Dataset')
plt.xlabel(data.feature_names[0])
plt.ylabel(data.feature_names[1])
plt.show()
