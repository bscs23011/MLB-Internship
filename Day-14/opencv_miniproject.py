import cv2
import numpy as np
import os

# Build a menu driven Python application using OpenCV that allows a user to perform different operations on an image.
# The application should support:
# Load an image
# Convert to grayscale
# Resize image
# Rotate image
# Flip image
# Crop image
# Draw shapes
# Add custom text
# Save the processed image


    
while True:

    


    try: 
        num = int(input("Enter a number (1-7) to perform an operation or 0 to exit:\n1. Convert to grayscale\n2. Resize image\n3. Rotate image\n4. Flip image\n5. Crop image\n6. Draw shapes\n7. Add custom text\n8. Save the picture\n9. Load another image\n0. Exit\n"))

        if num < 0 or num > 9:
            raise ValueError("number between 0 and 9")
        
    except ValueError:
        print("Invalid input. Please enter a number between 0 and 9.")
        continue

    if num == 0:
        print("Exiting the application.")
        break

    if num == 1:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("Image converted to grayscale")
        cv2.imshow("Image Preview", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif num == 2:
        x = int(input("enter the x :"))
        y = int(input("enter the y :"))

        if x <= 0 or y <= 0:
            print("Width and height must be greater than 0.")
            continue
            
        image = cv2.resize(image, (x, y))
        print("Image resized")
        cv2.imshow("Image Preview", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif num == 3:
        try:
            rot = int(input("\n1: rotate 90, \n2: rotate 180, \n3: rotate 270\n"))
            if rot < 1 or rot > 3:
                raise ValueError("number between 1 and 3")
        except ValueError:
            print("invalid input")
            continue

        if rot == 1:
            image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif rot == 2:
            image = cv2.rotate(image, cv2.ROTATE_180)
        elif rot == 3:
            image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

        print("image rotated")
        cv2.imshow("Image Preview", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    elif num == 4:
        try:
            flip = int(input("\n1:flip horizontal, \n2: flip vertical\n"))
            if flip < 1 or flip > 2:
                raise ValueError("number between 1 and 2")
            
        except ValueError:
            print("invalid input")
            continue

        if flip == 1:
            image = cv2.flip(image, 1)
        elif flip == 2:
            image = cv2.flip(image, 0)
        else:
            print("Invalid choice. Please select 1 or 2.")

        print("image flipped")
        cv2.imshow("Image Preview", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif num == 5:
        height, width = image.shape[:2]
        print(f"Image dimensions: {width}x{height}")

        x1 = int(input("enter the x1 :"))
        y1 = int(input("enter the y1 :"))
        x2 = int(input("enter the x2 :"))
        y2 = int(input("enter the y2 :"))

        

        if 0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height:
            image = image[y1:y2, x1:x2]
            print("Image cropped")
        else:
            print("Invalid crop coordinates.")
            continue

        print("Image cropped")
        cv2.imshow("Image Preview", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif num == 6:
        try:
            shape = int(input("\n1: Draw rectangle\n2: Draw circle\n3: Draw line\n4: Draw polygon\n"))
            if shape < 1 or shape > 4:
                raise ValueError
        except ValueError:
            print("Invalid choice")
            continue

        if shape == 1:
            x1 = int(input("enter the x1 :"))
            y1 = int(input("enter the y1 :"))
            x2 = int(input("enter the x2 :"))
            y2 = int(input("enter the y2 :"))

            color = tuple(map(int, input("Enter color (B G R): ").split()))
            thickness = int(input("Enter thickness: "))
            cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
            print("Rectangle drawn")

        if shape == 2:
            x = int(input("enter the x :"))
            y = int(input("enter the y :"))

            radius = int(input("enter the radius :"))
            color = tuple(map(int, input("Enter color (B G R): ").split()))
            thickness = int(input("Enter thickness: "))
            cv2.circle(image, (x, y), radius, color, thickness)
            print("Circle drawn")

        if shape == 3:
            x1 = int(input("enter the x1 :"))
            y1 = int(input("enter the y1 :"))
            x2 = int(input("enter the x2 :"))
            y2 = int(input("enter the y2 :"))
            color = tuple(map(int, input("Enter color (B G R): ").split()))
            thickness = int(input("Enter thickness: "))
            cv2.line(image, (x1, y1), (x2, y2), color, thickness)
            print("Line drawn")
        
        if shape == 4:
            points = []
            n = int(input("Enter number of points for polygon: "))
            for i in range(n):
                x = int(input(f"Enter x coordinate of point {i+1}: "))
                y = int(input(f"Enter y coordinate of point {i+1}: "))
                points.append((x, y))
            points = np.array(points, np.int32)
            points = points.reshape((-1, 1, 2))
            color = tuple(map(int, input("Enter color (B G R): ").split()))
            thickness = int(input("Enter thickness: "))
            cv2.polylines(image, [points], isClosed=True, color=color, thickness=thickness)
            print("Polygon drawn")

        cv2.imshow("Image Preview", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif num == 7:
        text = input("Enter the text to add: ")
        x = int(input("Enter x coordinate: "))
        y = int(input("Enter y coordinate: "))
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = float(input("Enter font scale (e.g., 1.0): "))
        color = tuple(map(int, input("Enter color (B G R): ").split()))
        thickness = int(input("Enter thickness: "))
        cv2.putText(image, text, (x, y), font, font_scale, color, thickness)
        print("Text added")

        cv2.imshow("Image Preview", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif num == 8:
        image_name = input("enter the name of image: ")
        cv2.imwrite(f"output_miniproject/{image_name}.jpg", image)
        print(f"Image saved as output_miniproject/{image_name}.jpg")

    elif num == 9:

        try:
            image_num = input("Enter the image number (1-5): ")

            if not image_num.isdigit():
                raise ValueError

            image_num = int(image_num)

            if image_num < 1 or image_num > 5:
                raise ValueError

            imagename = f"{image_num}.jfif"
            image = cv2.imread("sample_pictures/" + imagename)

            if image is None:
                print("Image not found. Please choose another image.")
                continue

            print("Image loaded successfully.")

            cv2.imshow("Image Preview", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            

        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")






    



            