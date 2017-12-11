#!/usr/bin/python
#-*- coding:utf-8 -*-
from PIL import ImageGrab,Image,ImageDraw,ImageFont
import os
import re
import math
import operator
import SDKTest

screenshotPath = ".\\rightpicture\\"
SUFFIX = ".png"

def pil_image_similarity(filepath1, filepath2):
	image1 = Image.open(filepath1)
	image2 = Image.open(filepath2)

	h1 = image1.histogram()
	h2 = image2.histogram()
	rms = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
	return rms

def transposePicture(filename):
	im = Image.open(filename)
	im = im.transpose(Image.ROTATE_90)
	im.save(filename)

def screenshot(source, dest, x1,y1,x2,y2):
	im = Image.open(source+SUFFIX)
	box=(x1,y1,x2,y2)
	region=im.crop(box)
	region.save(dest+SUFFIX)

def screenshotBoxCP(source, dest, x1,y1,x2,y2):
	imSource= Image.open(source+SUFFIX)
	imDest = Image.open(dest+SUFFIX)
	box=(x1,y1,x2,y2)
	regionSource=imSource.crop(box)
	regionDest=imDest.crop(box)
	# print '准备保存regionSource截图'
	regionSource.save(screenshotPath+'source'+SUFFIX)
	# print '准备保存regionDest截图'
	regionDest.save(screenshotPath+'dest'+SUFFIX)

	if pil_image_similarity(screenshotPath+'source'+SUFFIX,screenshotPath+'dest'+SUFFIX)<100:
		return "match"
	else:
		return "nomatch"

def comparedPicture(a,b):
	a = a + SUFFIX
	b = b + SUFFIX
	print u'正在对比图片结果：'
	if pil_image_similarity(a,b)<100:
		return "match"
	else:
		return "nomatch"