import numpy as np
import cv2

class resample:

    def resize(self, image, fx = None, fy = None, interpolation = None):
        """calls the appropriate funciton to resample an image based on the interpolation method
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        interpolation: method used for interpolation ('either bilinear or nearest_neighbor)
        returns a resized image based on the interpolation method
        """

        if interpolation == 'bilinear':
            return self.bilinear_interpolation(image, fx, fy)

        elif interpolation == 'nearest_neighbor':
            return self.nearest_neighbor(image, fx, fy)

    def nearest_neighbor(self, image, fx, fy):
        """resizes an image using bilinear interpolation approximation for resampling
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        returns a resized image based on the nearest neighbor interpolation method
        """

        #Write your code for nearest neighbor interpolation here
        codes = list(map(int, [image.shape[0] * fy, image.shape[1] * fx, image.shape[2]]))
        newImg = np.empty(codes, np.uint8)

        # Get width and height ratio between old and new images
        originRow = image.shape[0]
        originCol = image.shape[1]
        newRow = newImg.shape[0]
        newCol = newImg.shape[1]

        rowScale = newRow / originRow
        colScale = newCol / originCol

        for col in range(newCol - 1):
            for row in range(newRow - 1):
                x = col / colScale
                y = row / rowScale
                x = round(x)
                y = round(y)
                newImg[row, col] = image[y, x]

        # Save image
        cv2.imwrite('pic\scaledImage_nearestNeighbor.png', newImg)
        return newImg


    #Calculate interpolation
    def calculate_interpolation(self, img, positionX, positionY):
        outImg = []

        # Get integer and fractional parts of numbers
        x = int(positionX)
        y = int(positionY)
        x_diff = positionX - x
        y_diff = positionY - y
        xPlus = min(x + 1, img.shape[1] - 1)
        yPlus = min(y + 1, img.shape[0] - 1)

        # Get pixels in four corners
        for channel in range(img.shape[2]):
            bottomLeft = img[y, x, channel]
            bottomRight = img[y, xPlus, channel]
            topLeft = img[yPlus, x, channel]
            topRight = img[yPlus, xPlus, channel]

            # Calculate interpolation
            bottom = x_diff * bottomRight + (1. - x_diff) * bottomLeft
            top = x_diff * topRight + (1. - x_diff) * topLeft
            pixel = y_diff * top + (1. - y_diff) * bottom

            outImg.append(int(pixel + 0.5))

        return outImg

    def bilinear_interpolation(self, image, fx, fy):
        """resizes an image using bilinear interpolation approximation for resampling
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        returns a resized image based on the bilinear interpolation method
        """

        # Write your code for bilinear interpolation here
        # Create scaled empty image
        codes = list(map(int, [image.shape[0] * fy, image.shape[1] * fx, image.shape[2]]))
        newImg = np.empty(codes, np.uint8)

        # Get width and height ratio between old and new images
        rowScale = float(image.shape[0]) / float(newImg.shape[0])
        colScale = float(image.shape[1]) / float(newImg.shape[1])

        for row in range(newImg.shape[0]):
            for col in range(newImg.shape[1]):
                originRow = row * rowScale  # Find position in original image
                originCol = col * colScale
                newImg[row, col] = self.calculate_interpolation(image, originCol, originRow)

        #Save new scaled image
        cv2.imwrite('output\scaled_image_bilinear.png', newImg)
        return newImg

