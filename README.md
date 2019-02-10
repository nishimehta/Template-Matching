# Template-Matching
On a set of images, we detect the cursor object using a template image of cursor. We resize the image on different scales and try matching it with the template. However resizing may add false details so we first use a gaussian blur and then resize it. We use a 3x3 kernel to blur the image. Then, we apply the Laplacian transformation and then use CV2’s template matching.

References: Multi-scale Template Matching using Python and OpenCV 
https://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using- python-opencv/
