1. Why CNNs are Better than ANNs for Image Data

CNNs are designed specifically for image processing, while ANNs treat every pixel as an independent input by flattening the image into a 1D vector. 
This causes ANNs to lose spatial information and require a large number of parameters.
CNNs use convolutional layers to detect local features such as edges, textures, and shapes, and weight sharing to reduce the number of parameters. 
This makes CNNs more efficient, faster to train, and better at image classification.

2. Purpose of Convolution and Pooling Layers

Convolution Layer:
The convolution layer applies filters (kernels) to the input image to automatically extract important features like edges, textures, and patterns. 
In this project, a 3×3 kernel with 32 filters was used.
Pooling Layer:
The max pooling layer reduces the size of the feature maps by selecting the maximum value from each 2×2 region. 
This reduces computation, helps prevent overfitting, and preserves the most important features.

3. Model Architecture

The CNN model consists of the following layers:
Reshape (28×28×1): Adds a channel dimension for grayscale images.
Conv2D (32 filters, 3×3, ReLU): Extracts image features.
MaxPooling2D (2×2): Reduces feature map size.
Flatten: Converts 3D feature maps into a 1D vector.
Dense (128, ReLU): Learns high-level features.
Dense (10, Softmax): Predicts one of the 10 Fashion MNIST classes.

4. Final Training and Testing Accuracy with Graphs and Confusion Matrix

After training the model for 5 epochs it achieved good performance on both the training and test datasets.
final test accuracy: 0.9096999764442444
final training accuracy: 0.9405999779701233
Confusion Matrix:
 tf.Tensor(
[[818   1  14  34  10   1 114   1   7   0]
 [  0 981   1   9   5   0   3   0   1   0]
 [ 15   1 807   7 112   0  58   0   0   0]
 [  4   6  11 931  25   0  21   0   2   0]
 [  0   1  19  23 921   0  34   0   2   0]
 [  0   0   0   0   0 982   0  11   0   7]
 [ 69   0  41  29  89   0 760   0  12   0]
 [  0   0   0   0   0   5   0 984   1  10]
 [  4   0   2   3   1   1   4   1 984   0]
 [  1   0   0   0   0   8   0  62   0 929]]

5. Challenges Faced and How They Were Solved
Displaying images: Used Matplotlib's imshow() instead of print().
Confusion matrix error: Predicted labels for the entire test dataset instead of only the first five images, ensuring both arrays had the same size.
