import tensorflow as tf
from tensorflow import keras


print("Using relu:")
# One Input Layer
input_layer = keras.layers.Input(shape=(784,), name='input_layer')

# One Hidden Layer
hidden_layer = keras.layers.Dense(128, activation='relu', name='hidden_layer')(input_layer)

# One Output Layer
output_layer = keras.layers.Dense(10, activation='softmax', name='output_layer')(hidden_layer)

model = keras.Model(inputs=input_layer, outputs=output_layer)
model.summary()

print("Using sigmoid:")
# One Input Layer
input_layer2 = keras.layers.Input(shape=(784,), name='input_layer')

# One Hidden Layer
hidden_layer2 = keras.layers.Dense(128, activation='sigmoid', name='hidden_layer')(input_layer2)

# One Output Layer
output_layer2 = keras.layers.Dense(10, activation='softmax', name='output_layer')(hidden_layer2)

model = keras.Model(inputs=input_layer2, outputs=output_layer2)
model.summary()

print("Using tanh:")
# One Input Layer
input_layer3 = keras.layers.Input(shape=(784,), name='input_layer')

# One Hidden Layer
hidden_layer3 = keras.layers.Dense(128, activation='tanh', name='hidden_layer')(input_layer3)

# One Output Layer
output_layer3 = keras.layers.Dense(10, activation='softmax', name='output_layer')(hidden_layer3)

model = keras.Model(inputs=input_layer3, outputs=output_layer3)
model.summary()


#input layer takes input of shape 784, which is the flattened version of a 28x28 image. 
# The hidden layer has 128 neurons  
# The output layer has 10 neurons and uses the softmax activation function to produce 
# probabilities for each class.

#Activation funnctions:
# ReLU: It is the most commonly used activation function in deep learning. Gives output between 0 and infinity
#Sigmoid: It is used in the output layer for binary classification problems. output is between 0 and 1.
# Tanh: It is used in the hidden layers of deep neural networks. output is between -1 and 1.

#activation functions only modify how neurons transform their outputs so the model structure remained the same 
#the summary for each model is identical.