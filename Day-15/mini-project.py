import cv2
import numpy as np

# Document Image Enhancement Tool

# Build a Python application that improves the quality of document images.

# Your application should:

# Load a document image.
# Correct its perspective if the document is tilted.
# Convert it to grayscale.
# Reduce image noise.
# Enhance brightness and contrast.
# Sharpen the image.
# Save the enhanced image.


image = None 

while True:

    

    try: 
        num = int(input("Enter a number (1-7) to perform an operation or 0 to exit:\n1. Load a document image.\n2. Correct its perspective if the document is tilted.\n3.  Convert it to grayscale.\n4. Reduce image noise.\n5. Enhance brightness and contrast.\n6.Sharpen the image.\n7. Save the picture\n0. Exit\n"))

        if num < 0 or num > 9:
            raise ValueError("number between 0 and 7")
        
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 7.")
        continue 
    
    if num == 1:

        try:
            image_num = input("Enter the image number (1-10): ")

            if not image_num.isdigit():
                raise ValueError
            image_num = int(image_num)
            if image_num < 1 or image_num > 10:
                raise ValueError

            imagename = f"{image_num}.png"
            image = cv2.imread("sample_images/" + imagename)

            if image is None:
                print("Image not found. Please choose another image.")
                continue

            print("Image loaded successfully.")

            cv2.imshow("Image Preview", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        except ValueError:
            print("Invalid input. Please enter a number between 1 and 10.")


    if num == 2:
        if image is None:
            print("there is no image")
            continue

        height,width = image.shape[:2]

        src = np.float32([
        [35, 18],    
        [365, 18],   
        [28, 545],   
        [372, 545]   
        ])

        dst = np.float32([
        [0, 0],
        [width - 1, 0],
        [0, height - 1],
        [width - 1, height - 1] ])

        matrix = cv2.getPerspectiveTransform(src, dst)
        image = cv2.warpPerspective(image, matrix, (width, height))
        cv2.imshow("Perspective Transformed Image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.imwrite(f"output_miniproject/perspective_image{image_num}.jpg", image)


    
    if num == 3:
        if image is None:
            print("there is no image")
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("Image converted to grayscale")
        cv2.imshow("Image Preview", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if num == 4:
        if image is None:
            print("there is no image")
            continue
        # image = cv2.medianBlur(image, 3)
        image = cv2.bilateralFilter(image, 9, 75, 75)

        cv2.imshow("reduced image noise", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if num == 5:
        if image is None:
            print("there is no image")
            continue
        image = cv2.convertScaleAbs(image, alpha=1.2, beta=15)
        cv2.imshow("contrast+brightness", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if num == 6:
        if image is None:
            print("there is no image")
            continue
        kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
        image = cv2.filter2D(image, -1, kernel)
        cv2.imshow("sharpened image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if num == 7:
        if image is None:
            print("there is no image")
            continue
        cv2.imwrite(f"output_miniproject/{image_num}.jpg", image)
        print(f"Image saved as output_miniproject/{image_num}.jpg")

    if num == 0:
        print("Program ended")
        break
