import sklearn.datasets as datasets
import sklearn.decomposition as decomposition
import matplotlib.pyplot as plt
import sklearn.cluster as cluster
import pandas as pd


# Load the Iris dataset.
data = datasets.load_iris()

# Convert it into a Pandas DataFrame.
df = pd.DataFrame(data.data, columns=data.feature_names)

# Explore the dataset.
print(df.describe())
print(df.head())
print(df.info())
# Apply K-Means clustering.

cluster_model = cluster.KMeans(n_clusters=3, random_state=42)
cluster_model.fit(data.data)

# Use the Elbow Method to select the optimal number of clusters.
optimal_clusters = []
for k in range(1, 11):
    kmeans = cluster.KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data.data)
    optimal_clusters.append(kmeans.inertia_)

# Reduce the dataset to 2 dimensions using PCA.
pca = decomposition.PCA(n_components=2)
transformed_data = pca.fit_transform(data.data)

# Visualize:
  
# Original data (using selected features)
plt.scatter(data.data[:, 0], data.data[:, 1], c=data.target)
plt.title('Original Data (using selected features)')
plt.xlabel(data.feature_names[0])
plt.ylabel(data.feature_names[1])
plt.savefig('original_data.png') 
plt.show()


# K-Means clusters
plt.scatter(data.data[:, 0], data.data[:, 1], c=cluster_model.labels_)
plt.scatter(cluster_model.cluster_centers_[:, 0], cluster_model.cluster_centers_[:, 1], s=300, c='red', marker='X')
plt.title('K-Means Clustering of Iris Dataset')
plt.xlabel(data.feature_names[0])
plt.ylabel(data.feature_names[1])
plt.savefig('kmeans_clusters.png')
plt.show()


# PCA-transformed data
plt.scatter(transformed_data[:, 0], transformed_data[:, 1], c=data.target)
plt.title('PCA of Iris Dataset')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.savefig('pca_transformed_data.png')
plt.show()

# Briefly explain your observations:

# How many clusters were formed?
print(f"Number of clusters formed: {cluster_model.n_clusters}")

# Did the clusters represent the flower species well?
# The clusters formed by K-Means clustering represents  the actual species of the Iris dataset well.
# The scatter plot of the K-Means clusters shows that the data points are grouped into three distinct clusters
# They align with the three species of Iris (Setosa, Versicolor, and Virginica). 
# there may be some overlap between the clusters 
# indicating that K-Means may not perfectly separate these two species.

# How did PCA help in visualization?
# PCA helped in reducing the dimensionality of the dataset from 4 features to 2 principal components,
# making it easier to visualize the data in a 2D scatter plot.