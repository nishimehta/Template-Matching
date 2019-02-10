"""
Created on Mon Sep 17 19:22:42 2018

@author: nishimehta
#person 50291671
#ubit nishimeh
"""

# import the necessary packages
import numpy as np
import glob
import os
import cv2
#Path to the template
templatePath = 'template.jpeg'
#templatePath = 'task3_bonus/Bonus_1/t_1.jpg'
#templatePath = 'task3_bonus/Bonus_2/t_2.jpeg'
#templatePath = 'task3_bonus/Bonus_3/t_3.jpeg'
#path to the image folder
imageFolderPath = 'images'
#imageFolderPath = 'task3_bonus/Bonus_1'
#imageFolderPath = 'task3_bonus/Bonus_2'
#imageFolderPath = 'task3_bonus/Bonus_3'

def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
	# initialize the dimensions of the image to be resized and
	# grab the image size
	dim = None
	(h, w) = image.shape[:2]

	# if both the width and height are None, then return the
	# original image
	if width is None and height is None:
		return image

	# check to see if the width is None
	if width is None:
		# calculate the ratio of the height and construct the
		# dimensions
		r = height / float(h)
		dim = (int(w * r), height)

	# otherwise, the height is None
	else:
		# calculate the ratio of the width and construct the
		# dimensions
		r = width / float(w)
		dim = (width, int(h * r))

	# resize the image
	resized = cv2.resize(image, dim, interpolation = inter)

	# return the resized image
	return resized



#reading template image
template = cv2.imread(templatePath,0)

#applying laplacian transformation to the template
template = cv2.Laplacian(template,cv2.CV_64F)
template = np.float32(template)
#th and tw are the height and width of the template
(tH, tW) = template.shape[:2]
i=0
# loop over the images to find the template in
for imagePath in glob.glob(imageFolderPath + "/*.jpg"):
	i+=1
	#reads image
	image = cv2.imread(imagePath)
	
	#converts image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#applies gaussian blur with kernel size of 3 on the image
	blur = cv2.GaussianBlur(gray,(3,3),0)
	gray = cv2.Laplacian(blur,cv2.CV_64F)
	gray = np.float32(gray)
	found = None
	pos=0
	# loop over the scales of the image
	for scale in np.linspace(0.5, 2, 30):
		# resize the image according to the scale, and keep track
		# of the ratio of the resizing
		
		resized = resize(gray, width = int(gray.shape[1] * scale))
		r = gray.shape[1] / float(resized.shape[1])

		# if the resized image is smaller than the template, then break
		# from the loop
		if resized.shape[0] < tH or resized.shape[1] < tW:
			break

		# matching to find the template in the image
		#edged = cv2.Canny(resized, 50, 200)
		result = cv2.matchTemplate(resized, template, cv2.TM_CCOEFF)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

		# if we have found a new maximum correlation value, then update found
		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)
			(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
			(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
			
			

	# unpack the bookkeeping varaible and compute the (x, y) coordinates
	# of the bounding box based on the resized ratio
	if found is not None:#and pos>5:
		# draw a bounding box around the detected result and display the image
		(maxVal, maxLoc, r) = found
		if(maxVal>350000):
			print(imagePath,'maxval=',maxVal,'Cursor detected at location:',(int(maxLoc[0] * r), int(maxLoc[1] * r)))
			(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
			(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
			cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
		else:
			print(imagePath,'Cursor not detected')
	
	
	cv2.imshow(imagePath, image)
	cv2.waitKey(0)
	
	