#!/usr/bin/python
#-*- coding:utf-8 -*-
import os
import shutil
import xml.dom.minidom
import sys,re
import string
import time
reload(sys)  
sys.setdefaultencoding('utf8') 


#解析apk，得到 appPackage, appActivity
def getAppPackage(apkpath):
	print u'开始反编译：' + apkpath
	os.system("java -jar apktool_2.0.2.jar d "+apkpath)
	print u'反编译完成：' + apkpath
	dom = xml.dom.minidom.parse(shotname+'/AndroidManifest.xml')
	root = dom.documentElement
	appPackage = root.getAttribute("package")

	my_file=open(shotname+'/AndroidManifest.xml','r')
	while 1:
		line = my_file.readline()
		if not line:
			break
		pass
		if not line.find('activity') == -1:
			a = line.find('android:name="')+len('android:name="')
			b = line.find('"',a,-1)
			print line
			print a, b

			appActivity = line[a:b]
			print appActivity
			break
		pass

	return appPackage, appActivity


#返回现在要测试的apk信息，同时删掉在apkconfig文件中信息
def deleteconfigfirstline():
	configfile=open('apkconfig.txt')
	configfristline=configfile.readlines()
	if len(configfristline) == 0 or configfristline[0].strip() == '':
		print u'没有文件了'
		configfile.close()
		sys.exit(0)
	configfristline[0]=re.sub('\n','',configfristline[0])
	apkconfigdict[configfristline[0].split(':')[0]]=configfristline[0].split(':')[1] 
	configlastfile=open('apkconfignew.txt','w')
	configlaststring=''.join(configfristline[1:])
	configlastfile.write(configlaststring)
	configfile.close()
	configlastfile.close()
	os.remove('apkconfig.txt')
	shutil.move('apkconfignew.txt','apkconfig.txt')






if __name__=='__main__':

	androidapkpath=u'apk'#安卓包路径，这里要改的！之后把要改的都弄到一个文件里，到时候再说

	isparsepackage = 'yes'

	appPackage=''
	appActivity=''
	totalapkfile=0
	#要不要解析apk包，有一种情况：如果apkconfig文件里面没有你要跑的包了，你就要解析，如果有，你可以不解析了
	if isparsepackage == 'yes':
		# 为了解决中文问题，改文件名
		# for root,dirs,files in os.walk(androidapkpath):
		# 	for filename in files:
		# 		if filename.endswith('.apk'):
		# 			srcfullpath=os.path.join(root, filename)
		# 			dstfullpath=os.path.join(root,filename.split("_")[-1])
		# 			shutil.move(srcfullpath,dstfullpath)
				
		# 为了解决中文问题，替换文件名中的中文字符
		# for root,dirs,files in os.walk(androidapkpath):
		# 	for filename in files:
		# 		if filename.endswith('.apk'):
		# 			srcfullpath=os.path.join(root, filename)
		# 			dstfullpath=os.path.join(root,filename.replace(u'侠隐江湖','xyjh'))
		# 			dstfullpath=os.path.join(root,filename.replace(u'银汉','yh'))
		# 			dstfullpath=os.path.join(root,filename.replace(u'腾讯','tx'))
		# 			shutil.move(srcfullpath,dstfullpath)
		# 			print filename

		#获取各个apk的文件名和包名写入apkconfig文件中
		for root,dirs,files in os.walk(androidapkpath): 
			for filename in files:
				if filename.endswith('.apk'):
					startTime = time.time()
					configfile=file('apkconfig.txt',"a+")

					totalapkfile=totalapkfile+1
					(shotname,extension) = os.path.splitext(filename)
					if os.path.exists(shotname):
						pass
						shutil.rmtree(shotname)
					print root
					filefullpath=os.path.join(root, filename)
					print filefullpath
					filefullpath = filefullpath.decode('utf-8').encode('gb2312') 
					print filefullpath
					# filefullpath = unicode(filefullpath).encode('utf-8') 
					appPackage,appActivity = getAppPackage(filefullpath)
					configfile.write(filefullpath":"+appPackage+"-"+appActivity+"\n")
					shutil.rmtree(shotname)
					configfile.close()

					endTime = time.time()

					ftimename = time.strftime('%Y-%m-%d %H')
					# 统计耗时并打印到log.txt
					fLog = open('log\\' + ftimename + '.log', 'a+')
					fLog.write('反编译apk耗时' + '|' + filename + '|' + str(int(endTime-startTime))+'|'+appPackage+'|'+appActivity+'\n')
					fLog.close()
	else:
		configfile=open('apkconfig.txt')
		for configline in configfile:
			if not configline.strip() == '':
				totalapkfile=totalapkfile+1 
		configfile.close()

