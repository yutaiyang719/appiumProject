#!/usr/bin/python
#-*- coding:utf-8 -*-
from __future__ import division
from appium import webdriver
import unittest
import time
import os
import shutil
import matchpicture,getReport
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 配置当前要测试的客户端版本号
Ver='v1.4.00'
# 用例执行优先级默认 1	基础步骤，必定执行；2	尝试执行，跳过其他步骤；	3	建新号，才执行；4	测试功能细节，才执行；
PRIORITYSTAGE=2

#点击指定位置启动应用，全局配置，比如应用icon是最后一个则配置为-1，以此类推
appStartPos = -1
#点击appName 这里全局配置
appName = u'侠隐江湖'
# 截图保存位置
picfile = 'picfile\\'


#停顿时间
waittime=2

#录制时候手机的分辨率
standardX=1920
standardY=1080

#运行时候手机分辨率，这个也要手动配置的，到时候抽出文件来
runningX=1920
runningY=1080

#记录到日志文件
def clog(buf):
	ftimename = time.strftime('%Y-%m-%d %H')
	# 统计耗时并打印到log.txt
	fLog = open('log\\' + ftimename + '.log', 'a+')
	fLog.write(buf + '\n')
	print buf
	fLog.close()

#适配时候用的
def getXValue(xvalue):
	return int(ratioX*xvalue)

#适配时候用的
def getYValue(yvalue):
	return int(ratioY*yvalue)

#不是基于控件的输入都要这么做，别问我为什么
def getkeycode(keystring):
	if len(keystring) <= 1:
		driver.keyevent(int(keystring))
		return

	keycodedict={'0':7,'1':8,'2':9,'3':10,'4':11,'5':12,'6':13,'7':14,'8':15,'9':16,'a':29,'b':30,'c':31,'d':32,'e':33,'f':34,'g':35,'h':36,'i':37,'j':38,'k':39,'l':40,'m':41,'n':42,'o':43,'p':44,'q':45,'r':46,'s':47,'t':48,'u':49,'v':50,'w':51,'x':52,'y':53,'z':54}
	for i in keystring:
		driver.keyevent(keycodedict[i]) 

def getActionFileName(packagenameChannel):
	channelDict = {}
	channelDict['yh'] = '00'
	channelDict['tx'] = '02'
	return channelDict[packagenameChannel] + '_' +  packagenameChannel

def testresultdata(apkfilename, buf):
	resultFile=open(apkfilename+'/testresult.txt',"a+") 
	resultFile.write(buf + '\n')
	resultFile.close()

def clickScreen(x, y):
	driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(x), "y":getYValue(y)})#点击屏幕x,y坐标

def getChannelName(apkfilename):
	strTemp = apkfilename.split(Ver)[-1]
	packagenameChannel = strTemp.split('_')[1]
	return packagenameChannel

def isSkip(priority,num,remark):
	# 低于当前指定PRIORITYSTAGE的用例自动忽略执行
	if int(priority) > PRIORITYSTAGE:
		print 'The priority use cases skip execution：'+num+'	'+remark
		return 'skip'
	return 'success'


def runAction(apkfilename,packagename,num,channel,method,element,event,value,rectCoordinate,waittime=2,priority=1,remark=''):
	print 'runAction：	' + num + '	' + remark
	print 'apkfilename == ' + apkfilename
	packagenameChannel = getChannelName(apkfilename)
	parameter = {}

	if channel == '0' or packagenameChannel == channel:
		if len(value) != 0:
			parameter = value.split('*')
		if method == 'execute_script':
			if element == 'mobile: tap':
				if event == 'longClick':
					startTime = time.time()
					endTime = startTime
					while (endTime-startTime) < int(parameter[2]):
						driver.execute_script(element, {"touchCount":'1', "x":getXValue(int(parameter[0])), "y":getYValue(int(parameter[1]))})
						endTime = time.time()
				if event == 'nClick':
					for i in range(int(parameter[2])):
						driver.execute_script(element, {"touchCount":'1', "x":getXValue(int(parameter[0])), "y":getYValue(int(parameter[1]))})
						time.sleep(int(1))
				else:
					driver.execute_script(element, {"touchCount":'1', "x":getXValue(int(parameter[0])), "y":getYValue(int(parameter[1]))})
			
			else:# 后面补充
				pass
		elif method == 'find_elements_by_class_name':
			if element == 'android.widget.Button':
				if event == 'click':
					driver.find_elements_by_class_name("android.widget.Button")[int(parameter[0])].click()
				else:# 后面补充
					pass
			elif element == 'android.widget.TextView':
				if event == 'click':
					driver.find_elements_by_class_name("android.widget.TextView")[int(parameter[0])].click()
				elif event == 'text':
					for i in range(len(driver.find_elements_by_class_name("android.widget.TextView"))):
						if driver.find_elements_by_class_name("android.widget.TextView")[i].text == parameter[0]:
							driver.find_elements_by_class_name("android.widget.TextView")[i].click()
				else:# 后面补充
					pass
			elif element == 'android.widget.EditText':
				if event == '':
					# if len(driver.find_elements_by_class_name("android.widget.EditText")) == int(parameter[0]):
					# 	writeTestResultText(num,'failed',parameter[1])
					# else:
					# 	writeTestResultText(num,'success',parameter[1])
					pass
				elif event == 'send_keys':
					driver.find_elements_by_class_name("android.widget.EditText")[int(parameter[0])].send_keys(parameter[1])
				else:# 后面补充
					pass
			else:# 后面补充
				pass
		elif method == 'find_element_by_class_name':
			titletext=driver.find_element_by_class_name("android.widget.TextView")
			# if titletext.text == value:
			# 	writeTestResultText(num,'failed',value)
			# else:
			# 	writeTestResultText(num,'success',value)
		elif method == 'keyevent':
			if event == 'button':
				getkeycode(value) 
			elif event == 'send_keys':
				getkeycode(value)
			else:# 后面补充
				pass 
		elif method == 'get_screenshot_as_file':
			driver.get_screenshot_as_file(picfilepath+num)

		elif method == 'matchpicture':
			# getReport.loadImageData(picfilepath+num)
			# if matchpicture.catchpicture(num,picfilepath+num)=="match":
			# 	writeTestResultText(num,'success',u"新建角色")
			# else:
			# 	driver.get_screenshot_as_file(picfilepath+num)
			# 	getReport.loadImageData(picfilepath+num)
			# 	if matchpicture.catchpicture(num,picfilepath+num)=="match":
			# 		writeTestResultText(num,'success',u"新建角色")
			# 	else:
			# 		writeTestResultText(num,'failed',u"新建角色")
			pass
		elif method == 'swipe':
			startX = int(parameter[0])
			startY = int(parameter[1])
			endX = int(parameter[2])
			endY = int(parameter[3])
			during = int(parameter[4])
			n = int(parameter[5])
			for i in range(n):
				driver.swipe(getXValue(startX), getYValue(startY), getXValue(endX), getYValue(endY), during)
		else:# 后面补充
			pass

	else:
		# 跳过该渠道测试用例
		print 'The priority use cases skip execution：'+num+'	'+remark
	time.sleep(int(waittime))

# 截取图片
def screenshotSave(apkfilename,num,channel,remark,DEBUG,screenshotPath):
	fname = remark
	# 满足测试用例的优先级条件截取当前手机图片 一份临时图片，一份备案存档
	driver.get_screenshot_as_file(screenshotPath+"temp.png")
	# print u'保存temp图片成功'
	matchpicture.transposePicture(screenshotPath+"temp.png")
	# print u'旋转图片并保存成功'

	# 如果是DEBUG模式，则预截取正常情况的图片进行备份
	if DEBUG == True:
		# print u'预截取正常情况的图片进行备份'
		matchpicture.screenshot(screenshotPath+"temp", screenshotPath+fname, 0,0,runningX,runningY)
		# print u'预截取正常情况的图片备份完成'

	# 保存测试过程截图记录
	picturePathName = apkfilename+'\\'+picfile+fname
	# print u'测试过程截图进行备份'
	matchpicture.screenshot(screenshotPath+"temp", picturePathName, 0,0,runningX,runningY)
	# print u'测试过程截图进行备份完成'

# 对比图片
def screenshotCP(apkfilename,num,channel,remark,x1,y1,x2,y2,priority,picturePathName,screenshotPath):
	# 截图并对比截图结果
	print picturePathName +'	CP	'+screenshotPath,'	rect:',x1,y1,x2,y2
	if matchpicture.screenshotBoxCP(picturePathName,screenshotPath,x1,y1,x2,y2) == 'match':
		isResult = 'success'
	else:
		isResult = 'failed'
	print 'screenshotCP:'+isResult
	return isResult

# 打印结果
def outResult(apkfilename,num,channel,remark,isResult,testresultdataID):
	remark 
	testresultdata(apkfilename, str(testresultdataID)+'	'+ num+'	'+isResult+'	'+remark)
	print u'该条用例执行完成，打印到日志'
	clog('runActionResult' + '|' + apkfilename + '|' + num + '|'+ channel+ '|' + isResult + '|'  + remark)
	pass

class SDKTest:
	#初始化这个类的时候要传递apk文件名和包名进来
	def __init__(self,apkfilename,packagename,appActivity,username,password,DEBUG):
		self.apkfilename=apkfilename
		self.packagename=packagename
		self.username=username
		self.password=password
		self.appActivity=appActivity
		self.DEBUG = DEBUG

	def MainTestYHSDK(self):
		#建立好存放结果的文件夹和文件
		global picfilepath,testresultdata,username,password,packagename,rerunning,testresultdataID,screenshotPath
		rerunning='false'
		picfilepath=self.apkfilename+'/picfile/'
		beginScreenshotPath = "rightpicture\\"

		testresultdataID = 1

		username=self.username
		password=self.password
		packagename=self.packagename
		appActivity=self.appActivity

		if not os.path.exists(picfilepath): 
			os.mkdir(picfilepath)

		#计算好适配的比率
		global ratioX,ratioY
		ratioX=runningX/standardX
		ratioY=runningY/standardY

		#默认执行所有动作的结果为成功
		global RESULT
		RESULT='success'

		print " begin run appium"

		#不用多说，开始跑了
		desired_caps = {}
		desired_caps['platformName'] = 'Android'
		desired_caps['platformVersion'] = '5.0.2'
		desired_caps['deviceName'] = 'Redmi Note 2'
		desired_caps['appPackage'] = packagename
		desired_caps['appActivity'] = appActivity
		desired_caps['unicodeKeyboard'] = True 
		desired_caps['resetKeyboard'] = True
		global driver
		driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

		print 'link appium success'

		time.sleep(20)

		# 解析数据配置的动作并执行
		strTemp = self.apkfilename.split(Ver)[-1]
		packagenameChannel = strTemp.split('_')[1]
		if packagenameChannel == 'TENCENT':
			packagenameChannel = 'tx'

		fAction = open('action\\' + getActionFileName(packagenameChannel)+'_'+'Action.txt', 'r')

		skipList = {}
		skipList[0] = 'Click Close to recharge interface'
		skipList[1] = 'Click Skip sign'
		skipList[2] = 'Click to skip ads on her face'
		skipList[3] = 'Download the patch'
		skipList[4] = 'Skip Announcement'

		for line in fAction:
			line=line.strip('\n')
			lineList = line.split('	')
			num = lineList[0]
			channel = lineList[1]
			method = lineList[2]
			element = lineList[3]
			event = lineList[4]
			value = lineList[5]
			rectCoordinate = lineList[6]
			waittime = lineList[7]
			priority = lineList[8]
			remark = lineList[9]
			isResult = 'success'
			

			screenshotPath = beginScreenshotPath+getActionFileName(packagenameChannel)+'\\'
			fname = remark
			CPscreenshotPath = beginScreenshotPath+getActionFileName(packagenameChannel)+'\\'+fname
			picturePathName = self.apkfilename+'\\'+picfile+fname

			# print 'beginscreenshotPath:',screenshotPath

			# 执行动作
			isResult = isSkip(priority,num,remark)
			if int(priority) == 2:
				flag = False
				for i in skipList:
					if skipList[i] == remark:
						flag = True
				if flag:
					CPscreenshotPath = beginScreenshotPath+remark
			# print 'flagscreenshotPath:',CPscreenshotPath

			if isResult != 'skip':
				# 尝试执行，跳过其他步骤
				if int(priority)!=2:
					runAction(self.apkfilename,packagename,num,channel,method,element,event,value,rectCoordinate,waittime,priority,remark)

				# 截取图片
				screenshotSave(self.apkfilename,num,channel,remark,self.DEBUG,screenshotPath)

				# 对比图片
				x1,y1,x2,y2 = 0,0,runningX,runningY
				if rectCoordinate=='':
					x1,y1,x2,y2 = runningX-int(runningX/3), runningY-int(runningY/3), runningX, runningY
				else:
					rectCoordinateDict = rectCoordinate.split('*')
					# print rectCoordinateDict
					x1 = int(rectCoordinateDict[0])
					y1 = int(rectCoordinateDict[1])
					x2 = int(rectCoordinateDict[2])
					y2 = int(rectCoordinateDict[3])
				# print x1,y1,x2,y2
				isResult = screenshotCP(self.apkfilename,num,channel,remark,x1,y1,x2,y2,priority,picturePathName,CPscreenshotPath)
				if isResult == 'failed':
					if int(priority)!=2:
						RESULT = 'failed'

				# 如果是跳过类型的action，且匹配成功，则执行该步骤，不记录打印结果操作
				if int(priority)==2 :
					if isResult == 'success':
						runAction(self.apkfilename,packagename,num,channel,method,element,event,value,rectCoordinate,waittime,priority,remark)
					print num + '	execution：'+isResult+'	:'+remark
					continue
				else:
					outResult(self.apkfilename,num,channel,remark,isResult,testresultdataID)
					testresultdataID = 1 + testresultdataID

				# if isResult=='failed':
				# 	print u'录制测试过程出问题了，暂停100秒先，查看信息'
				# 	time.sleep(100)
				# 	pass

		fAction.close()

		# 打印执行结果保存到文件
		fresult = open('result\\result.txt', 'a+')
		fresult.write(time.strftime('%Y-%m-%d %H:%M:%S') +'|' +self.apkfilename + '|' + packagename + '|' + RESULT+'\n')
		fresult.close()
		RESULT='success'

		#导出报告
		getReport.exportReport(self.apkfilename)
		print u'测试报告导出完成'

		driver.quit()
