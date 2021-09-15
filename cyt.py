from multiprocessing import cpu_count
from imutils import paths
import numpy as np
import argparse
from module.analisis import areap_staining
from module.analisis import intensity_staining 
from module.analisis import integrated_staining 
import os
import pathlib
import sys
import multiprocessing 
from contextlib import contextmanager
from functools import partial
import shutil


if __name__ == "__main__":

	ap = argparse.ArgumentParser()
	
	ap.add_argument("-i", "--images", required=True, type=str,
		help="path to input directory of images")
	ap.add_argument ("-m", "--method", required=True, type = str,
		help = "method could be area, intensity or integrate")
	ap.add_argument("-b", "--background", required=False, action="store_true",
		help="if you write b, background will be substracted in intensity method")
	ap.add_argument("-t","--threshold", required=False, action="store_true",
		help="if you write t, Otsu threslholding will procces in intensity method") 
	ap.add_argument("-ihq","--imnunohystochemestry", required=False, action="store_true",
		help="if you write ihq, intensity methods will invert the mean gray value") 
	ap.add_argument ("-s", "--scale", required=False, type = float,
		help = "set a scale in pixels/unit")

	print ("organizing data")

	args = vars(ap.parse_args())
	allImagePaths = sorted(list(paths.list_images(args["images"])))
	NUM_IMAGES = len (allImagePaths)
	index = list(range (1,NUM_IMAGES+1))
	payloads = []

	for (i, imagePaths) in enumerate(allImagePaths):
		data = imagePaths
		payloads.append(data)

	print ("done")

	print ("checking temporal file")

	temporal = pathlib.Path("temporal")

	if temporal.exists():
		print("temporal exist")
		print ("removing temporal file")
		shutil.rmtree('temporal')
		os.mkdir ("temporal")
		print ("creating a new temporal file")
	else:
		print ("creating a temporal file") 
		os.mkdir ("temporal")

	print ("starting parallel processing")

	def pool1context(*args, **kwargs):
		pool1 = multiprocessing.Pool(*args, **kwargs)
		yield pool1
		pool1.terminate()

	bool1 = False
	bool2 = False
	back = args["background"] 
	ihq = args["imnunohystochemestry"]
	thr = args["threshold"]


	if "area" in args["method"] :
		with multiprocessing.Pool(processes=cpu_count()) as pool:
			results = pool.map(partial(areap_staining, back= back), payloads)

	elif "intensity" in args["method"] :
		with multiprocessing.Pool(processes=cpu_count()) as pool:
				results = pool.map(partial(intensity_staining, back= back, thr=thr, ihq =ihq), payloads)
		bool1 = True 
	elif "integrate" in args["method"] :
		with multiprocessing.Pool(processes=cpu_count()) as pool:
				results = pool.map(partial(integrated_staining, back= back,ihq =ihq, scale = scale), payloads) 
		bool2 = True

	
	print("removing temporal file")
	shutil.rmtree('temporal') 

	print("checking output file")

	outfile = pathlib.Path("output")

	if outfile.exists():
		print("output file exist")
	else:
		os.mkdir ("output")
		print ("creating an output file") 

	
	print ("naming the output")

	BACK = "wob"
	THR = "wot"
	IHQ = "ifb"

	

	if back == True:
		BACK = str ("back")

	if thr == True :
		THR = str("thr")

	if ihq == True:
		IHQ = str("ihq") 

	methodo = str(args["method"]) # 
	imageso = str(args["images"]) 
	out = "output/{0}-{1}-{2}-{3}-{4}resultado.csv" 
	outp = out.format(methodo, BACK,THR,IHQ,imageso) 
	#outp = str("output") + str ("/") +str(args["method"]) + "-"+ BACK + "-" + THR +"-"+ IHQ + "-"+ str(args["images"]) + str ("resultado.csv") 

	print ("done")

	print ("saving")

	scale = args["scale"] 
	sca = ","+ str (scale) # creating a string from the scale to add into result csv

	if bool2 == True:
		np.savetxt(outp,np.column_stack((index,allImagePaths,results)), delimiter=',',fmt='%s')
		with open(outp,'a') as f:
			f.write("index,ImagePaths,integrated_intensity,area_staining, percent_staining" + sca)
	elif bool1 == True:
		np.savetxt(outp,np.column_stack((index,allImagePaths,results)), delimiter=',',fmt='%s')
		with open(outp,'a') as f:
			f.write("index,ImagePaths,intensity_staining")
	else:
		np.savetxt(outp,np.column_stack((index,allImagePaths,results)), delimiter=',',fmt='%s')
		with open(outp,'a') as f:
			f.write("index,ImagePaths,area_percent")	