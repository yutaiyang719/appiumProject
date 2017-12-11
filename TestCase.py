#!/usr/bin/python
#-*- coding:utf-8 -*-
import os
import shutil
import xml.dom.minidom
import getReport
import sys,re
import time
import SDKTest
reload(sys)  
sys.setdefaultencoding('utf8') 

apkconfigdict={}#存放要跑的apk信息,包括文件路径和包名
accountconfigdict={}#存放账号信息

DEBUG=False	# 是否开启DEBUG模式

def logOut(buf):
	print buf

def cinstalllog(apkfullpath):
	finstalllog = open('log\\' + 'installlog.log','a+')
	finstalllog.write(apkfullpath + '|' + 'installSuccess' + '\n')
	finstalllog.close()

def isInstall(apkfullpath):
	finstalllog = open('log\\' + 'installlog.log','r+')
	for line in finstalllog:
		if line == (apkfullpath + '|' + 'installSuccess' + '\n'):
			finstalllog.close()
			return True
	finstalllog.close()
	return False

def getaccountinfo():
	accountconfig=open('accountconfig.txt')
	userandpwd = {}
	for accountline in accountconfig:
		if not accountline.strip() == '':
			userandpwd[0] = accountline.split('	')[1]
			userandpwd[1] = accountline.split('	')[2]
			accountconfigdict[accountline.split('	')[0]]=userandpwd
	accountconfig.close()

def getUserAndPwd(userandpwd):
	return userandpwd.split(';')[0],userandpwd.split(';')[1]
 

#解析apk，得到包名
def getpackagename(apkpath):
	os.system("java -jar apktool_2.0.2.jar d "+apkpath)
	dom = xml.dom.minidom.parse(shotname+'/AndroidManifest.xml')
	root = dom.documentElement
	return root.getAttribute("package")

# 返回要测试的apk路径+apk名，appPackage，appActivity
def getapkconfig():
	# fapkconfig = open('tools//apkconfig.txt', 'w')
	logOut(u'准备读取apkconfig信息')
	fapkconfig = open('apkconfig.txt', 'r+')
	apkconfigdict = {}
	for line in fapkconfig:
		# print line
		apkconfigdict[line.split(':')[0]]=line.split(':')[1]
	# 关闭apkconfig文件
	fapkconfig.close()
	return apkconfigdict

if __name__=='__main__': 
	androidapkpath=u'apk\\'#安卓包路径，这里要改的！之后把要改的都弄到一个文件里，到时候再说
	getaccountinfo()#获得账号信息
	logOut(u'已经getaccountinfo')
	#运行顺序是根据apkcofnig文件里面的顺序跑的，开始跑所有要跑的包
	apkconfigdict={}
	apkconfigdict = getapkconfig()
	logOut(u'已经getapkconfig')
	# print apkconfigdict

	#获得文件路径，文件名，包名。同时创建跟文件名相同的文件夹，用于之后存放相应的截图，结果，报告
	for key,value in apkconfigdict.items():
		startTime = time.time()
		apkfullpath=key
		print apkfullpath
		apkfilename = apkfullpath.split('\\')[-1]
		if os.path.exists(apkfilename):
			shutil.rmtree(apkfilename)
		os.mkdir(apkfilename)
		packagename=value.split('-')[0]
		appActivity=value.split('-')[1]


		#安装这个apk到手机
		logOut(u'准备安装'+ apkfullpath + u'开始')
		if not isInstall(apkfullpath):
			os.system("adb install "+apkfullpath)
			logOut(u'安装'+ apkfullpath + u'完成')
			cinstalllog(apkfullpath)
		else:
			logOut(u'跳过安装'+ apkfullpath)

		# print accountconfigdict
		username,password=accountconfigdict[packagename][0], accountconfigdict[packagename][1]

		logOut(apkfullpath + u'测试用例开始执行')
		#运行相应的测试用例
		Test = SDKTest.SDKTest(apkfilename,packagename,appActivity,username,password,DEBUG)
		Test.MainTestYHSDK()

		logOut(apkfullpath + u'测试用例执行完毕')	

		# 卸载这个安装包
		if DEBUG == False:
			os.system("adb uninstall "+packagename)
			logOut(u'卸载'+apkfullpath+u'完成')
		
		endTime = time.time()
		ftimename = time.strftime('%Y-%m-%d %H')
		# 统计耗时并打印到log.txt
		SDKTest.clog(u'testApkTime' + '|' + apkfilename + '|'+str(int(endTime-startTime)))
