1. What is Transfer Learning?

Transfer Learning is a deep learning technique where a model that has already been trained on a large dataset is reused for a new but related task. 
Instead of training a model from scratchwe use the knowledge learned from the pre-trained model and add new layers for our specific classification problem.
For this project, MobileNetV2 was pre-trained on the ImageNet dataset, which contains over one million images across 1,000 classes.

2. Why did you choose MobileNetV2?

I chose MobileNetV2 because:
It is pre-trained on the ImageNet dataset.
It is lightweight and fast compared to larger models like VGG16 and ResNet50.
It requires fewer computational resources and memory.
It provides good accuracy while training quickly.
It is well-suited for deployment on mobile and edge devices.


3. What experiments did you perform to improve accuracy?


Used a pre-trained MobileNetV2 model instead of training from scratch.
Froze the base model to preserve the learned ImageNet features.
Added custom classification layers (GlobalAveragePooling2D, Dense(128), Softmax).
Used MobileNetV2's preprocess_input() function to normalize images correctly.
Split the dataset into training (80%) and validation (20%).
Ignored corrupted images in the Cats vs Dogs dataset to prevent training interruptions.
Trained the model using the Adam optimizer and Sparse Categorical Crossentropy loss.

4. Your final validation accuracy
Validation Accuracy: 0.984


5. Key challenges and lessons learned

Challenges:

The tensorflow_datasets Cats vs Dogs dataset produced archive errors.
Some images in the dataset were corrupted and caused training to stop.
I initially trained only the base model instead of connecting the custom classifier.
I accidentally batched the dataset twice, causing input shape errors.

Lessons Learned:

Transfer Learning greatly reduces training time and improves performance.
Pre-trained models can achieve high accuracy with only a few additional layers.
Proper image preprocessing is essential for good results.
Freezing the base model allows it to act as a feature extractor while only the new layers are trained.
Careful dataset preparation and debugging are important for successful deep learning projects.
