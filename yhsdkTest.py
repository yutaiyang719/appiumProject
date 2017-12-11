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

#点击指定位置启动应用，全局配置，比如应用icon是最后一个则配置为-1，以此类推
appStartPos = -1
#点击appName 这里全局配置
appName = u'侠隐江湖'

#停顿时间
waittime=2

#录制时候手机的分辨率
standardX=1920
standardY=1080

#运行时候手机分辨率，这个也要手动配置的，到时候抽出文件来
runningX=1920
runningY=1080


#适配时候用的
def getXValue(xvalue):
	return int(ratioX*xvalue)

#适配时候用的
def getYValue(yvalue):
	return int(ratioY*yvalue)

#不是基于控件的输入都要这么做，别问我为什么
def getkeycode(keystring):
	keycodedict={'0':7,'1':8,'2':9,'3':10,'4':11,'5':12,'6':13,'7':14,'8':15,'9':16,'a':29,'b':30,'c':31,'d':32,'e':33,'f':34,'g':35,'h':36,'i':37,'j':38,'k':39,'l':40,'m':41,'n':42,'o':43,'p':44,'q':45,'r':46,'s':47,'t':48,'u':49,'v':50,'w':51,'x':52,'y':53,'z':54}
	for i in keystring:
		driver.keyevent(keycodedict[i]) 

#把测试用例运行结果写入文件，包括测试用例编号，结果，用例描述
def writeTestResultText(testcasenum,result,mark):
	testresultdata.write(testcasenum+":"+result+";"+mark+"\n")


#点击账号注册按钮
def clickAccountRegister():
	driver.find_elements_by_class_name("android.widget.Button")[2].click()


def ErrorExit():
	testresultdata.close()
	driver.quit()
	os.system("adb uninstall "+packagename)
	sys.exit()

def ErrorHandler(isDirectlogin):
	print "error hanlder"
	os.system("adb shell am force-stop "+packagename)
	time.sleep(waittime*5)
	driver.find_elements_by_class_name("android.widget.TextView")[appStartPos].click()#点击appName 这里全局配置
	time.sleep(waittime*10)
	driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1119), "y":getYValue(709)})#补丁
	time.sleep(30)
	driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(959), "y":getYValue(888)})
	time.sleep(waittime*2)
	if isDirectlogin=='true':
		driver.find_elements_by_class_name("android.widget.Button")[0].click()
	else:
		textfields=driver.find_elements_by_class_name("android.widget.EditText")
		textfields[0].send_keys(username)
		textfields[1].send_keys(password)
		time.sleep(waittime*2)
		driver.find_elements_by_class_name("android.widget.Button")[0].click()
	time.sleep(waittime*5)
	driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(958), "y":getYValue(752)})#点击进入游戏
	time.sleep(waittime*5)
	driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1762), "y":getYValue(853)})#点击开始
	time.sleep(waittime*5)
	driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1637), "y":getYValue(150)})#点击关闭
	time.sleep(waittime)



class SDKAndroidInitialTest(unittest.TestCase):

	def setUp(self):
		print "SDK Initial Test"
		time.sleep(waittime)

	#点击返回，sdk消失
	def test_a1CickReturn(self):
		self.testcaseNum='1'
		driver.get_screenshot_as_file(picfilepath+self.testcaseNum+".png")
		driver.keyevent(4);
		if len(driver.find_elements_by_class_name("android.widget.EditText")) == 2:
			writeTestResultText(self.testcaseNum,'failed',u"检查初始化状态")
		else:
			writeTestResultText(self.testcaseNum,'success',u"检查初始化状态")
		self.assertNotEqual(2, len(driver.find_elements_by_class_name("android.widget.EditText")))
		
	#再点击界面sdk出现
	def test_a2CickReturn(self):
		self.testcaseNum='2'
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(634), "y":getYValue(631)})#随便点击下屏幕
		time.sleep(waittime)
		driver.get_screenshot_as_file(picfilepath+self.testcaseNum+".png")
		if len(driver.find_elements_by_class_name("android.widget.EditText")) == 2:
			writeTestResultText(self.testcaseNum,'success',u"点击返回，再点击屏幕")
		else:
			writeTestResultText(self.testcaseNum,'failed',u"点击返回，再点击屏幕")
			ErrorExit()
		self.assertEqual(2, len(driver.find_elements_by_class_name("android.widget.EditText")))


class SDKAndroidAccountRegisterTest(unittest.TestCase):

	def setUp(self):
		print "SDKAndroidAccountRegisterTest"
		time.sleep(waittime)

	#账号注册成功
	def test_a1RegisterSuccess(self):
		self.testcaseNum='3'
		self.textfields=driver.find_elements_by_class_name("android.widget.EditText")
		self.textfields[1].send_keys("123456")
		driver.find_elements_by_class_name("android.widget.Button")[2].click()
		time.sleep(waittime/2)
		driver.get_screenshot_as_file(picfilepath+self.testcaseNum+".png")
		self.titletext=driver.find_element_by_class_name("android.widget.TextView")
		if self.titletext.text == u'账号注册':
			writeTestResultText(self.testcaseNum,'failed',u"账号注册")
			ErrorExit()
		else:
			writeTestResultText(self.testcaseNum,'success',u"账号注册")
		self.assertNotEqual(u'账号注册', self.titletext.text)

	# 登陆成功
	def test_a2Mobileloginsuccess(self):
		self.testcaseNum='4'
		time.sleep(waittime)
		driver.find_elements_by_class_name("android.widget.Button")[0].click()
		time.sleep(waittime*5)
		driver.get_screenshot_as_file(picfilepath+self.testcaseNum+".png")
		time.sleep(waittime*2)
		if len(driver.find_elements_by_class_name("android.widget.EditText")) == 0:
			writeTestResultText(self.testcaseNum,'success',u"账号登录")
		else:
			writeTestResultText(self.testcaseNum,'failed',u"账号登录")
			ErrorExit()
		self.assertEqual(0, len(driver.find_elements_by_class_name("android.widget.EditText")))

	#新建角色
	def test_a3CreatRole(self):
		self.testcaseNum='5'
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1115), "y":getYValue(620)})#点击选择服务
		time.sleep(waittime)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(380), "y":getYValue(381)})#点击1-10服
		time.sleep(waittime)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(813), "y":getYValue(522)})#点击1服
		time.sleep(waittime)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(958), "y":getYValue(752)})#点击进入游戏
		time.sleep(waittime*5)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1762), "y":getYValue(853)})#点击开始
		time.sleep(waittime*5)
		driver.get_screenshot_as_file(picfilepath+self.testcaseNum+".png")

		getReport.loadImageData(picfilepath+self.testcaseNum+".png")
		if matchpicture.catchpicture(self.testcaseNum,picfilepath+self.testcaseNum+".png")=="match":
			writeTestResultText(self.testcaseNum,'success',u"新建角色")
		else:
			ErrorHandler('true')
			driver.get_screenshot_as_file(picfilepath+self.testcaseNum+".png")
			getReport.loadImageData(picfilepath+self.testcaseNum+".png")
			if matchpicture.catchpicture(self.testcaseNum,picfilepath+self.testcaseNum+".png")=="match":
				writeTestResultText(self.testcaseNum,'success',u"新建角色")
			else:
				writeTestResultText(self.testcaseNum,'failed',u"新建角色")
				ErrorExit()

		


	#新手指引
	def test_a4newguideSuccess(self):
		self.testcaseNum='6'
		time.sleep(waittime*3)
		for i in range(8):
			driver.swipe(getXValue(288), getYValue(754), getXValue(374), getYValue(624), 1000)
			time.sleep(waittime/2)
		time.sleep(waittime*3)
		for i in range(10):
			driver.swipe(getXValue(288), getYValue(754), getXValue(324), getYValue(624), 1000)
			time.sleep(waittime/2)

		time.sleep(waittime*5)
		for i in range(30):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1762), "y":getYValue(894)})#点击放招
			time.sleep(waittime/2)
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1536), "y":getYValue(952)})#点击放招
			time.sleep(waittime/2)
		time.sleep(waittime*10)
		for i in range(15):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(220), "y":getYValue(460)})#点击主线
			time.sleep(waittime/2)
		for i in range(2):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1487), "y":getYValue(657)})#点击领奖 
			time.sleep(waittime)
		for i in range(2):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(220), "y":getYValue(460)})#点击主线
			time.sleep(waittime)
		for i in range(2):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1228), "y":getYValue(830)})#点击战斗
			time.sleep(waittime)
		time.sleep(waittime*5)
		for i in range(5):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1228), "y":getYValue(830)})#随便点击
			time.sleep(waittime/2)

		for i in range(10):
			driver.swipe(getXValue(283), getYValue(696), getXValue(260), getYValue(631), 1000)
			time.sleep(waittime/2)

		for i in range(10):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1532), "y":getYValue(786)})#点击放招
			time.sleep(waittime/2)
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1762), "y":getYValue(894)})#点击放招
			time.sleep(waittime/2)
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1536), "y":getYValue(952)})#点击放招
			time.sleep(waittime/2)


		for i in range(10):
			driver.swipe(getXValue(283), getYValue(696), getXValue(260), getYValue(631), 1000)
			time.sleep(waittime/2)

		for i in range(30):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1532), "y":getYValue(786)})#点击放招
			time.sleep(waittime/2)
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1762), "y":getYValue(894)})#点击放招
			time.sleep(waittime/2)
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1536), "y":getYValue(952)})#点击放招
			time.sleep(waittime/2)


		time.sleep(waittime*5)
		for i in range(2):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1838), "y":getYValue(418)})#点击背包
			time.sleep(waittime)
		for i in range(2):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1333), "y":getYValue(289)})#点击装备
			time.sleep(waittime)
		for i in range(2):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1276), "y":getYValue(930)})#点击装备
			time.sleep(waittime)
		for i in range(2):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1858), "y":getYValue(54)})#点击关闭
			time.sleep(waittime)
		for i in range(2):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(220), "y":getYValue(460)})#点击主线
			time.sleep(waittime)
		for i in range(2):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1487), "y":getYValue(657)})#点击领奖 
			time.sleep(waittime)
		for i in range(2):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1697), "y":getYValue(72)})#点击领奖 
			time.sleep(waittime)
		for i in range(2):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(656), "y":getYValue(308)})#点击签到
			time.sleep(waittime)
		for i in range(2):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(985), "y":getYValue(700)})#点击签到
			time.sleep(waittime)
		for i in range(2):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1683), "y":getYValue(133)})#点击签到
			time.sleep(waittime)
		for i in range(10):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(220), "y":getYValue(460)})#点击主线
			time.sleep(waittime)
		for i in range(1):
			driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1487), "y":getYValue(657)})#点击领奖 
			time.sleep(waittime)
	
		driver.get_screenshot_as_file(picfilepath+self.testcaseNum+".png")
		getReport.loadImageData(picfilepath+self.testcaseNum+".png")
		if matchpicture.catchpicture(self.testcaseNum,picfilepath+self.testcaseNum+".png")=="match":
			writeTestResultText(self.testcaseNum,'success',u"新手引导")
		else:
			writeTestResultText(self.testcaseNum,'failed',u"新手引导")
			ErrorHandler('false')




class SDKAndroidLoginSuccessTest(unittest.TestCase):
	def setUp(self):
		print "Login success test"
		time.sleep(waittime)

	# 支付宝界面拉取成功
	def test_a1ZFBsuccess(self):
		self.testcaseNum='7'
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(119), "y":getYValue(274)})#点击优惠
		time.sleep(waittime*3)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1522), "y":getYValue(244)})#点击前往充值
		time.sleep(waittime*3)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(623), "y":getYValue(366)})#点击30块月卡
		time.sleep(waittime*3)

		for i in range(len(driver.find_elements_by_class_name("android.widget.TextView"))):
			if driver.find_elements_by_class_name("android.widget.TextView")[i].text == u'支付宝':
				driver.find_elements_by_class_name("android.widget.TextView")[i].click()#点击支付宝
				time.sleep(waittime*8)
				driver.get_screenshot_as_file(picfilepath+self.testcaseNum+".png")
				self.titletext=driver.find_elements_by_class_name("android.widget.TextView")[1]
				if self.titletext.text == u'登录支付宝':
					writeTestResultText(self.testcaseNum,'success',u"支付宝界面拉取")
				else:
					writeTestResultText(self.testcaseNum,'failed',u"支付宝界面拉取")
					rerunning='true'
				break
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(121), "y":getYValue(146)})#点击返回
		time.sleep(waittime)
		driver.find_elements_by_class_name("android.widget.Button")[1].click()#点击是 
		time.sleep(waittime)


	# 微信界面拉取成功
	def test_a2WXsuccess(self):
		self.testcaseNum='8'
		for i in range(len(driver.find_elements_by_class_name("android.widget.TextView"))):
			if driver.find_elements_by_class_name("android.widget.TextView")[i].text == u'微信支付':
				driver.find_elements_by_class_name("android.widget.TextView")[i].click()#点击微信支付
				time.sleep(waittime*5)
				driver.get_screenshot_as_file(picfilepath+self.testcaseNum+".png")
				self.titletext=driver.find_elements_by_class_name("android.widget.TextView")[0]
				if self.titletext.text == u'登录微信':
					writeTestResultText(self.testcaseNum,'success',u"微信界面拉取")
				else:
					writeTestResultText(self.testcaseNum,'failed',u"微信界面拉取")
					rerunning='true'
				break
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(73), "y":getYValue(142)})#点击返回
		time.sleep(waittime*2)
		driver.find_elements_by_class_name("android.widget.Button")[0].click()#这里不会是每台机器都不一样吧。。。。
		time.sleep(waittime*2)
		driver.find_elements_by_class_name("android.widget.Button")[0].click()
		time.sleep(waittime*2)



	# 银联界面拉取成功
	def test_a3YLsuccess(self):
		self.testcaseNum='9'
		for i in range(len(driver.find_elements_by_class_name("android.widget.TextView"))):
			if driver.find_elements_by_class_name("android.widget.TextView")[i].text == u'银联':
				driver.find_elements_by_class_name("android.widget.TextView")[i].click()#点击银联
				time.sleep(waittime*5)
				driver.get_screenshot_as_file(picfilepath+self.testcaseNum+".png")
				self.titletext=driver.find_elements_by_class_name("android.widget.TextView")[0]
				if self.titletext.text == u'订单支付':
					writeTestResultText(self.testcaseNum,'success',u"银联界面拉取")
				else:
					writeTestResultText(self.testcaseNum,'failed',u"银联界面拉取")
					rerunning='true'
				break
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(73), "y":getYValue(142)})#点击返回
		time.sleep(waittime)
		driver.find_elements_by_class_name("android.widget.TextView")[2].click()



	# 充值卡界面拉取成功
	def test_a4CZKsuccess(self):
		self.testcaseNum='10'
		for i in range(len(driver.find_elements_by_class_name("android.widget.TextView"))):
			if driver.find_elements_by_class_name("android.widget.TextView")[i].text == u'充值卡':
				driver.find_elements_by_class_name("android.widget.TextView")[i].click()#点击充值卡
				time.sleep(waittime*5)
				driver.get_screenshot_as_file(picfilepath+self.testcaseNum+".png")
				self.titletext=driver.find_elements_by_class_name("android.widget.TextView")[0]
				if self.titletext.text == u' 充值卡':
					writeTestResultText(self.testcaseNum,'success',u"充值卡界面拉取")
				else:
					writeTestResultText(self.testcaseNum,'failed',u"充值卡界面拉取")
					rerunning='true'
				break
		driver.find_elements_by_class_name("android.widget.TextView")[1].click()
		time.sleep(waittime)
		driver.find_elements_by_class_name("android.widget.Button")[0].click()
		time.sleep(waittime)






class SDKAndroidLogout(unittest.TestCase):
	def setUp(self):
		print "logout success test"
		time.sleep(waittime)

	#注销
	def test_a1ReturnKey(self):
		self.testcaseNum='11'
		driver.keyevent(4)
		time.sleep(waittime)
		driver.get_screenshot_as_file(picfilepath+self.testcaseNum+"_1.png")
		driver.find_elements_by_class_name("android.widget.Button")[1].click()#点击退出游戏
		time.sleep(waittime*5)
		driver.get_screenshot_as_file(picfilepath+self.testcaseNum+"_2.png")
		self.titletext=driver.find_elements_by_class_name("android.widget.TextView")
		#这里到时候要配置
		if self.titletext[appStartPos].text == appName:
			writeTestResultText(self.testcaseNum,'success',u"退出游戏")
		else:
			writeTestResultText(self.testcaseNum,'failed',u"退出游戏")
			ErrorExit() 
		self.assertEqual(appName, self.titletext[appStartPos].text)#点击appName 这里到全局配置

		driver.find_elements_by_class_name("android.widget.TextView")[appStartPos].click()#点击appName 这里全局配置
		time.sleep(waittime*10)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1119), "y":getYValue(709)})#补丁
		time.sleep(30)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(959), "y":getYValue(888)})
		time.sleep(waittime*2)
		self.textfields=driver.find_elements_by_class_name("android.widget.EditText")
		self.textfields[0].send_keys(username)
		self.textfields[1].send_keys(password)
		driver.find_elements_by_class_name("android.widget.Button")[0].click()
		time.sleep(waittime*5)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(958), "y":getYValue(752)})#点击进入游戏
		time.sleep(waittime*5)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1762), "y":getYValue(853)})#点击开始
		time.sleep(waittime*5)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1637), "y":getYValue(150)})#点击关闭
		time.sleep(waittime)
		


class SDKAndroidChangeAccountTest(unittest.TestCase):
	def setUp(self):
		print "Change account test"
		time.sleep(waittime)

	# 切换账号
	def test_a1ChangeAccountSuccess(self):
		self.testcaseNum='12'
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1833), "y":getYValue(63)})#点击更多
		time.sleep(waittime)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1444), "y":getYValue(70)})#点击设置
		time.sleep(waittime)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1294), "y":getYValue(679)})#点击切换账号
		time.sleep(waittime)
		if not len(driver.find_elements_by_class_name("android.widget.EditText")) == 2:
			writeTestResultText(self.testcaseNum,'failed',u"切换账号")
			ErrorExit()

		driver.find_elements_by_class_name("android.widget.ImageView")[0].click()
		time.sleep(waittime)
		driver.find_elements_by_class_name("android.widget.TextView")[1].click()
		time.sleep(waittime)
		driver.find_elements_by_class_name("android.widget.Button")[0].click()
		time.sleep(waittime*5)
		driver.get_screenshot_as_file(picfilepath+self.testcaseNum+".png")
		writeTestResultText(self.testcaseNum,'None',u"切换账号")
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(142), "y":getYValue(1015)})#点击返回
		time.sleep(waittime)


	# 切换账号
	def test_a2ChangeAccountSuccess(self):
		self.testcaseNum='13'
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1701), "y":getYValue(1024)})#点击切换账号
		time.sleep(waittime)
		if not len(driver.find_elements_by_class_name("android.widget.EditText")) == 2:
			writeTestResultText(self.testcaseNum,'failed',u"切换账号")
			ErrorExit()
		driver.find_elements_by_class_name("android.widget.ImageView")[0].click()
		time.sleep(waittime)
		driver.find_elements_by_class_name("android.widget.TextView")[1].click()
		time.sleep(waittime)
		driver.find_elements_by_class_name("android.widget.Button")[0].click()
		time.sleep(waittime*5)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(958), "y":getYValue(752)})#点击进入游戏
		time.sleep(waittime*5)
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1762), "y":getYValue(853)})#点击开始
		time.sleep(waittime*5)
		driver.get_screenshot_as_file(picfilepath+self.testcaseNum+".png")
		writeTestResultText(self.testcaseNum,'None',u"切换账号")


class YHSDKTest:
	#初始化这个类的时候要传递apk文件名和包名进来
	def __init__(self,apkfilename,packagename,appActivity,username,password):
		self.apkfilename=apkfilename
		self.packagename=packagename
		self.username=username
		self.password=password
		self.appActivity=appActivity


	def MainTestYHSDK(self):
		#建立好存放结果的文件夹和文件
		global picfilepath,testresultdata,username,password,packagename,rerunning
		rerunning='false'
		picfilepath=self.apkfilename+'/picfile/'
		testresultdata=file(self.apkfilename+'/testresult.txt',"w") 
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

		print " begin run appium"

		
		#不用多说，开始跑了
		desired_caps = {}
		desired_caps['platformName'] = 'Android'
		desired_caps['platformVersion'] = '5.0'
		desired_caps['deviceName'] = 'SM-N9009'
		desired_caps['appPackage'] = packagename
		desired_caps['appActivity'] = appActivity
		desired_caps['unicodeKeyboard'] = True 
		desired_caps['resetKeyboard'] = True
		global driver
		driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

		time.sleep(waittime*10)
		#下载补丁
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(1119), "y":getYValue(709)})
		time.sleep(30)

		#跳过公告
		driver.execute_script("mobile: tap", {"touchCount":"1", "x":getXValue(959), "y":getYValue(888)})

		#初始化测试
		suiteInital = unittest.TestLoader().loadTestsFromTestCase(SDKAndroidInitialTest)
		unittest.TextTestRunner(verbosity=2).run(suiteInital)

		#账号注册
		clickAccountRegister()
		suiteRegisterAccount = unittest.TestLoader().loadTestsFromTestCase(SDKAndroidAccountRegisterTest)
		unittest.TextTestRunner(verbosity=2).run(suiteRegisterAccount)


		#账号登陆成功
		suitLoginSuccess = unittest.TestLoader().loadTestsFromTestCase(SDKAndroidLoginSuccessTest)
		unittest.TextTestRunner(verbosity=2).run(suitLoginSuccess)
		if rerunning == 'true':
			ErrorHandler('true')
			rerunning='false'
			suitLoginSuccess = unittest.TestLoader().loadTestsFromTestCase(SDKAndroidLoginSuccessTest)
			unittest.TextTestRunner(verbosity=2).run(suitLoginSuccess)

		if rerunning == 'true':
			ErrorExit()
 
		#注销
		suitLogout = unittest.TestLoader().loadTestsFromTestCase(SDKAndroidLogout)
		unittest.TextTestRunner(verbosity=2).run(suitLogout)

		
		#切换账号
		suitChangeAccount = unittest.TestLoader().loadTestsFromTestCase(SDKAndroidChangeAccountTest)
		unittest.TextTestRunner(verbosity=2).run(suitChangeAccount)

		testresultdata.close()

		driver.quit()
