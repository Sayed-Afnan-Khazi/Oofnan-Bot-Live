import cv2

def detectFaces(imagePath,cascPath= "haarcascade_frontalface_default.xml"):

    # Reading the image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detecting faces in the image
    faceCascade = cv2.CascadeClassifier(cascPath)
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Drawing a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Saving the new image with the rectangles on faces
    new_image_path = "detected-"+imagePath
    cv2.imwrite(new_image_path, image)

    # Returning the new image path
    return new_image_path, len(faces)