What is clustering?

Clustering is an unsupervised machine learning technique that groups similar data points into clusters based on their characteristics.

What is PCA?
Principal Component Analysis (PCA) is a dimensionality reduction technique that transforms a dataset with many features into a smaller set of principal components while preserving most of the important information (variance). 
In this project, PCA reduced the Iris dataset from 4 features to 2 principal components, making it easier to visualize the data on a 2D scatter plot.

How did you determine the best value of K?

The best value of K was determined using the Elbow Method.

K-Means was run for values of K = 1 to 10.
For each K, the inertia was calculated.
These inertia values were plotted against the number of clusters.
The optimal value of K was chosen at the "elbow" of the graph, where the decrease in inertia became much smaller.

What insights did you gain from the visualizations?
The original scatter plot showed the distribution of the flowers using two selected features (sepal length and sepal width),
but there was some overlap between species.
The K-Means visualization showed that the algorithm successfully grouped the flowers into three clusters, which closely matched the three Iris species.
there was slight overlap between the Versicolor and Virginica clusters because these species have similar measurements.
The PCA visualization reduced the dataset to two principal components while preserving most of the important information. 
This made the clusters much easier to observe and demonstrated that Setosa is clearly separated from the other two species,
while Versicolor and Virginica remain partially overlapping.
