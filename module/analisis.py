import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import subprocess

def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    blurred = cv.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened

def areapercent (image):
    hist = np.histogram(image, bins=256, range=(0, 256)) [0]
    blur = cv.GaussianBlur(image,(5,5),0)
    ret,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU) 
    ret2= int(ret)
    histthresholed = hist[0:ret2-1]
    percent = (sum(histthresholed))*100/sum(hist)
    return percent

def area (image):
    hist = np.histogram(image, bins=256, range=(0, 256)) [0]
    blur = cv.GaussianBlur(image,(5,5),0)
    ret,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU) 
    ret2= int(ret)
    histthresholed = hist[0:ret2-1]
    areat = sum(histthresholed)   
    return areat 

def meanintensity (image,hist,thr,ihq) :
 
    if thr == True:
        blur = cv.GaussianBlur(image,(5,5),0)
        ret,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU) 
        ret2= int(ret)
        histthresholed = hist[0:ret2-1]
        bins = np.arange (0,ret2-1)
        av = histthresholed.dot(bins) 
        Imean = av/sum(histthresholed)
    else:
        bins = np.arange (0,256)
        av = hist.dot(bins) 
        Imean = av/sum(hist)
    if ihq == True:
       Imean = 255 - Imean  
    return Imean

def areap_staining(name,back):

	if back == True:  
		name2 = name.split ("/")
		name3 = name2[0].split("\\")
		name4 =  name3[0] + "/"+ name3[1]
		javacall = "java -jar ij.jar -batch background.ijm" + " " + name4
		javaoutput = "temporal/" + "out" + name3[1]
		javao = str (javaoutput)
		proc = subprocess.run (javacall)
		img2 = cv.imread(javao,0)
		areap = areapercent (img2)  

	else:
		img = cv.imread (name ,0) 
		areap = areapercent (img)
	return areap     

def intensity_staining(name,back,thr,ihq): 

	if back == True: 
		name2 = name.split ("/")
		name3 = name2[0].split("\\")
		name4 = name3[0] + "/"+ name3[1]
		javacall = "java -jar ij.jar -batch background.ijm" + " " + name4
		javaoutput = "temporal/" + "out" + name3[1]
		javao = str (javaoutput)
		proc = subprocess.run (javacall)
		img2 = cv.imread(javao,0) 
		hist = np.histogram(img2, bins=256, range=(0, 256)) [0]  
		intensidad = meanintensity(img2,hist,thr,ihq) 
	else:
		img = cv.imread (name ,0)
		hist = np.histogram(img, bins=256, range=(0, 256)) [0]  
		intensidad = meanintensity(img,hist,thr,ihq)
	return intensidad 

def integrated_staining(name,back,ihq,scale):

	if back == True: 
		name2 = name.split ("/")
		name3 = name2[0].split("\\")
		name4 = name3[0] + "/"+ name3[1]
		javacall = "java -jar ij.jar -batch background.ijm" + " " + name4
		javaoutput = "temporal/" + "out" + name3[1]
		javao = str (javaoutput)
		proc = subprocess.run (javacall)
		img2 = cv.imread(javao,0) 
		areat = area (img2)
		areats = areat/scale 
		hist = np.histogram(img2, bins=256, range=(0, 256)) [0] 
		percent = areat*100/sum(hist) 
		thr2 = True
		intensidad = meanintensity(img2,hist,thr2,ihq)
		integrated = intensidad * areats 
	else:
		img = cv.imread (name ,0)
		areat = area (img)
		areats = areat/scale 
		hist = np.histogram(img, bins=256, range=(0, 256)) [0] 
		percent = areat*100/sum(hist)
		thr2 = True
		intensidad = meanintensity(img,hist,thr2,ihq)
		integrated = intensidad * areats 
	return integrated,areats,percent 