import cv2
import numpy as np

image = cv2.imread("sample_images/scan_000.png")
cv2.imshow("Original Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Translate an image horizontally and vertically.
horizontal_shift = int(input("Enter horizontal shift (positive for right, negative for left): "))
h_image = np.float32([[1, 0, horizontal_shift], [0, 1, 0]])


cv2.imshow("Horizontally Shifted Image", cv2.warpAffine(image, h_image, (image.shape[1], image.shape[0])))
cv2.waitKey(0)
cv2.destroyAllWindows()


vertical_shift = int(input("Enter vertical shift (positive for down, negative for up): "))
v_image = np.float32([[1, 0, 0], [0, 1, vertical_shift]])
cv2.imshow("Vertically Shifted Image", cv2.warpAffine(image, v_image, (image.shape[1], image.shape[0])))
cv2.waitKey(0)
cv2.destroyAllWindows()

# Rotate an image by different angles.
rotate_angle = int(input("Enter rotation angle (in degrees): "))
(h, w) = image.shape[:2]
rotation_matrix = cv2.getRotationMatrix2D((w / 2, h / 2), rotate_angle, 1)
rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))
cv2.imshow("Rotated Image", rotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Scale an image up and down.
print("scale up: \n")
fx = float(input("fx: "))
fy = float(input("fy: "))

scaled_up_image = cv2.resize(image, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)
cv2.imshow("Scaled Up Image", scaled_up_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("scale down: ")
x = float(input("fx: "))
y = float(input("fy: "))
scaled_down = cv2.resize(image, None, fx=x, fy=y, interpolation=cv2.INTER_AREA)
cv2.imshow("Scaled Down Image", scaled_down)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Apply an affine transformation.
pts1 = np.float32([[50,50],[200,50],[50,200]])
pts2 = np.float32([[10,100],[200,50],[100,250]])
matrix = cv2.getAffineTransform(pts1, pts2)
affine = cv2.warpAffine(image, matrix, (image.shape[1], image.shape[0]))
cv2.imshow("Affine Transformed Image", affine)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Apply a perspective transformation to straighten a tilted document.
prespective_matrix = np.float32([[0.2, 0.1, 0], [0.1, 0.2, 0], [0.001, 0.001, 1]])
prespective_transformed_image = cv2.warpPerspective(image, prespective_matrix, (image.shape[1], image.shape[0]))
cv2.imshow("Perspective Transformed Image", prespective_transformed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Increase and decrease image brightness.
brightness_increase = 50
brightened_image = cv2.convertScaleAbs(image, alpha=1, beta=brightness_increase)
cv2.imshow("Brightened Image", brightened_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

brightness_decrease = -50
darkened_image = cv2.convertScaleAbs(image, alpha=1, beta=brightness_decrease)
cv2.imshow("Darkened Image", darkened_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Adjust image contrast.
contrast_increase = 1.5
contrasted_image = cv2.convertScaleAbs(image, alpha=contrast_increase, beta=0)
cv2.imshow("Contrasted Image", contrasted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Apply Gaussian Blur, Median Blur, and Bilateral Filter.
gaussian_blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
cv2.imshow("Gaussian Blurred Image", gaussian_blurred_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

median_blurred_image = cv2.medianBlur(image, 5)
cv2.imshow("Median Blurred Image", median_blurred_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

bilateral_filtered_image = cv2.bilateralFilter(image, 9, 75, 75)
cv2.imshow("Bilateral Filtered Image", bilateral_filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Sharpen the image using an image sharpening filter.
sharpening_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
sharpened_image = cv2.filter2D(image, -1, sharpening_kernel)
cv2.imshow("Sharpened Image", sharpened_image)
cv2.waitKey(0)
cv2.destroyAllWindows()