#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,xlsxwriter,re
from PIL import Image
import sys 


allRootPath=os.getcwd()
SHEET_NAME='result'


DEFAULT_CELL_SIZE=260
DEFAULT_IMAGE_CELL_SIZE=0.3
DEFAULT_IMAGE_HEIGHT_SIZE=0.3


def loadImageData(theImagePath):
	imageObject = Image.open(theImagePath)
	if imageObject.size[0]<imageObject.size[1]:
		imageObject=imageObject.transpose(Image.ROTATE_90)   
		imageObject.save(theImagePath) 

def exportReport(apkfilename):
	allRootPath = apkfilename
	reportfile=allRootPath+"/report.xlsx"
	picfilepath=allRootPath+'/picfile/'
	testresulttxt=allRootPath+'/testresult.txt'

	reload(sys)
	sys.setdefaultencoding('utf-8')

	#写入excel
	workbook=xlsxwriter.Workbook(reportfile)
	worksheet=workbook.add_worksheet(SHEET_NAME)
	rowNum = 1
	for parent,dirnames,filenames in os.walk(picfilepath):
		for filename in filenames:
			if filename.endswith('.png') or filename.endswith('.jpg'):
				picturefullpath=os.path.join(parent,filename)
				loadImageData(picturefullpath)
				worksheet.set_row(rowNum,DEFAULT_CELL_SIZE)
				worksheet.insert_image(rowNum,1,picturefullpath,{'positioning':2,'x_scale':DEFAULT_IMAGE_CELL_SIZE,'y_scale':DEFAULT_IMAGE_HEIGHT_SIZE})
				rowNum += 2
				# worksheet.set_row(int(filename.split(".")[0].split("_")[0]),DEFAULT_CELL_SIZE)
				# worksheet.insert_image(int(filename.split(".")[0].split("_")[0]),1,picturefullpath,{'positioning':2,'x_scale':DEFAULT_IMAGE_CELL_SIZE,'y_scale':DEFAULT_IMAGE_HEIGHT_SIZE})

	green = workbook.add_format({'bg_color':'green'})
	red = workbook.add_format({'bg_color':'red'})
	yellow = workbook.add_format({'bg_color':'yellow'})
	formatColor = green
	picdata = open(testresulttxt, 'r+')
	rowNum = 0
	for each_line in picdata:
		each_line=each_line.strip('\n')
		each_lineList = each_line.split('	')
		# print each_line
		rowResult=each_lineList[2]
		if rowResult == 'success':
			formatColor = green
		elif rowResult == 'failed':
			formatColor = red
		else:
			formatColor = yellow

		worksheet.write(rowNum,0,each_lineList[0],formatColor)
		worksheet.write(rowNum,1,each_lineList[1],formatColor)
		worksheet.write(rowNum,2,each_lineList[2],formatColor)
		# worksheet.write(rowNum,3,u'中文字符无法输出到excel，操作详情请看testresult.txt',formatColor)
		rowNum += 2
		# print rowNum

	picdata.close()
	workbook.close()

# if __name__ == "__main__":
# 	exportReport()
# 	exportReport('00_xyjh_v1.3.80_yh_v2.1.0_2.apk')
