import pickle, cutie, random, re

"""
скомпилировать в exe
добавить комменты в код
раскидать код по блокам

Логика работы:
1) oldsAreHere - ищем старую ДБ
не нашли
1.1) initFile - получаем список героев
1.2) initFileKeywords - получаем список кейвордов
1.3) initDict - инцилизируем вручную словарь с параметрами героев
нашли
1.a) pickleLoad - загружаем ДБ с диска
2.0) workRoll для выбора старых настроек или сбора новых
2) initRoll - выбираем параметры для ролла
3) prepareDataAndRoll - происходит ролл, пишется герой
доп возможности
-printHeroDict - вывести словарь
-произвести initDict заново с предварительной проверкой в initDBOverwriteCheck

{Axe:	{Lol:3
		Kek:1
		Cheurek:2}
		}
"""

class WorkingPicker():

	'''
	Инцилизация
	'''
	def __init__(self):
		self.heroList=[]#список героев по умолчанию импортирующийся из листХиро.ткст
		self.keywordList=[]#список кейвордов по умолчанию импортирующийся из листКейвордс.ткст
		self.heroDict={}#словарь связок герой-его параметры формирующийся вручную и записывающийся в ДБ методом пикл
		self.searchingFor={}#словарь кейвордов с установленной оценкой для поиска по героям
		self.heroToRandom=[]#список героев подходящих под критерий
		self.deafaultDB="pckDB.dat"#стандартное название ДБ
		self.funcList=["Roll",""]#список функциий для вывода в кьюти
		self.gradeList=['1','2','3']#возможные оценки
		self.lastRollParam={}
	'''
	Загрузка/выгрузка данных из внешних файлов
	'''
	#Загрузка списока героев
	def initFile(self):	
		textfile=open("data/listHero.txt","r")
		for k in textfile:
			self.heroList.append(k.rstrip())
	#Загрузка списка свойств
	def initFileKeywords(self):	
		textfile=open("data/listKeywords.txt","r")
		for k in textfile:
			self.keywordList.append(k.rstrip())
	#Выгрузка основного рабочего словаря
	def heroDictIntoTxt(self):
		textfile=open("data/listComplete.txt","w")
		for key in self.heroDict:
			textfile.write("{0};{1}\n".format(key,self.heroDict[key]))
		textfile.close()
		print("listComplete.txt updated!")
	#Загрузка раб словаря с ткст
	def txtIntoHeroDict(self):
		textfile=open("data/listComplete.txt","r")
		for k in textfile:
			formedString=re.sub(r'[^\w]',' ',k).split()
			print(formedString)
			tempDict={}
			for k in formedString[1::2]:
				tempDict[k]=int(formedString[formedString.index(k)+1])
			self.heroDict[formedString[0]]=tempDict
	#Выгрузка рабочих данных с помщью базы данных
	def pickleDump(self):
		pickleFile=[self.heroDict, self.keywordList,self.lastRollParam]
		pickle.dump(pickleFile,open(self.deafaultDB,"wb"))
	#Загрузка рабочих данных с помощью базы данных
	def pickleLoad(self):
		try:
			pickleFile=pickle.load(open(self.deafaultDB,"rb"))
		except FileNotFoundError:
			return "There is no database with {0} name".format(self.deafaultDB)
		else:
			#unpack
			self.heroDict=pickleFile[0]
			self.keywordList=pickleFile[1]
			self.lastRollParam=pickleFile[2]
	'''
	Вспомогательные функции для работы с Базами Данных
	'''
	#Выбор нестандартной БД для загрузки
	def setDBName(self):
		getName=input("Type in name for DB to search(without .dat): ")
		self.deafaultDB=getName+".dat"
		getAnswer=input("If you want to load data from it enter 'y' or anything to continue without loading 'n': ")
		if getAnswer=="y":
			self.pickleLoad()
	#Проверка на наличие БД в раб каталоге программы
	def oldsAreHere(self):
		#returns False if file not found, otherwise True
		try:
			open(self.deafaultDB,"rb")
		except FileNotFoundError:
			self.olds=0
			return self.olds#поддержка непосредственного вызова ф-ии, планирую убрать
		else:
			self.olds=1
			return self.olds
	#Получение разрешение у пользователя на перезапись БД
	def initDBOverwriteCheck(self):
		if self.oldsAreHere()==0:
			inputGrade=input("There are alrady DB. If you want to overwrite it enter 'y', to close initilization 'n', to create a new DB write its name: ")
			if inputGrade=="y":
				self.initDict()
			elif inputGrade=="n":
				pass
			else:
				self.deafaultDB=inputGrade+".dat"
				self.initDict()
		else:
			self.initDict()
	'''
	Основные рабочие функции
	'''
	#Создание Словаря: {"Герой":{"Сильный":"2", "Быстрый":"3", "Ловкий":"1"}}
	#Запускается при первом запуске программы или для ручной перенастройки
	def initDict(self):
		print("Type in a grade in {0}..{1} range, or anything else to continue".format(self.gradeList[0],self.gradeList[-1]))
		for hero in self.heroList:
			tempKeywordDict={}
			for keyword in self.keywordList:
				inputGrade=input("Does {0} is {1}? ".format(hero, keyword))
				if inputGrade in self.gradeList:
					tempKeywordDict[keyword]=inputGrade
			self.heroDict[hero]=tempKeywordDict
		self.pickleDump()
	#Изменеие рабочего словаря в процессе работы программы
	def changeAttributeInHeroDict(self, firstrun=1):
		if firstrun==1:
			self.printHeroDict()
		getName=input("Enter name of hero: ")
		if getName in self.heroDict:
			print("."*4+getName)
			for k in self.heroDict[getName]:
				print("."*16+k)
			formedList=sorted(list(self.heroDict[getName].keys()))
			formedList+=["--Add Attribute","--Remove Attribute","--Back"]
			print("Change what?")			
			getChoice=cutie.select(formedList)
			if getChoice==(len(formedList)-1):
				pass
			elif getChoice==(len(formedList)-2):
				getName2=input("Write name of Attribute to remove: ")
				self.heroDict[getName].pop(getName2,"There are no such Attribute")
			elif getChoice==(len(formedList)-3):
				getName2=input("Write name of Attribute to add: ")
				try:
					getGrade=int(input("Write grade from {0}..{1} of Attribute to add: ".format(self.gradeList[0],self.gradeList[-1])))
				except ValueError:
					print("Invalid input")
				else:
					self.heroDict[getName][getName2]=getGrade
			else:
				currentAttr=formedList[getChoice]
				try:
					getGrade=int(input("Change grade of {0} to which? (in {1}..{2} range) ".format(currentAttr, self.gradeList[0],self.gradeList[-1])))
				except ValueError:
					print("Invalid input")
				else:
					if not getGrade==0:
						self.heroDict[getName][currentAttr]=getGrade
					else:
						self.heroDict[getName].pop(formedList[getChoice],None)
		else:
			getAnswer=input("No hero with such name found. Try again?(y/n) ")
			if getAnswer=='y':
				self.changeAttributeInHeroDict(firstrun=0)				
	#Основной цикл Ролла вызывающий вспомгательные функции
	def workRoll(self):
		if len(self.lastRollParam)>0:
			for key in self.lastRollParam:
				print(key+"-->"+str(self.lastRollParam[key]))
			print("Do you want to load previous roll-settings?(y to continue without changes) ")
			if input()=='y':
				self.prepareDataAndCallRoll()
			else:
				self.initRoll()
		else:
			self.initRoll()


	"""
	Вспомогательные рабочие функции
	"""
	#Интерфейс, который рассказывает нам что хочет найти пользователь
	def initRoll(self,listOut=0):
		self.searchingFor={}
		cutieKeywordList=[]
		for k in self.keywordList:
			cutieKeywordList.append([k,0])
		#print(cutieKeywordList)
		cutieKeywordList.sort()
		cutieKeywordList+=["--Back","--Next"]
		while(1):
			getChoice = cutie.select(cutieKeywordList)#[Tank, DD, Heal]
			if getChoice==(len(cutieKeywordList)-1):
				#next
				self.prepareDataAndCallRoll(listOut)
				break
			elif getChoice==(len(cutieKeywordList)-2):
				break
			else:# getChoice in  list(range(len(cutieKeywordList))):
				getGrade=int(input("Type in grade for {0} parameter in range {1}..{2}: ".format(cutieKeywordList[getChoice],self.gradeList[0],self.gradeList[-1])))
				self.searchingFor[cutieKeywordList[getChoice][0]]=getGrade
				cutieKeywordList[getChoice][1]=getGrade
	#Цикл производящий поиск данных подходящих под критерии
	def prepareDataAndCallRoll(self,listOut=0):
		self.heroToRandom=[]
		self.lastRollParam=self.searchingFor
		lenSearchList=len(self.searchingFor)
		#print(self.searchingFor)
		#print(lenSearchList)
		for hero in self.heroDict:
			lenCompareList=0
			for keyword in self.heroDict[hero]:
				if keyword in self.searchingFor:
					#print(hero, keyword, int(self.heroDict[hero][keyword]),int(self.searchingFor[keyword]))
					if int(self.heroDict[hero][keyword])>=int(self.searchingFor[keyword]):
						#print('es' if int(self.heroDict[hero][keyword])>=int(self.searchingFor[keyword]) else 'no')
						lenCompareList+=1
						#print(lenCompareList, lenSearchList)
			if lenCompareList==lenSearchList:
				#print(hero)
				self.heroToRandom.append(hero)
		if len(self.heroToRandom)==0:
			print("There are no heroes with such parameters")		
		else:
			self.pickleDump()
			if listOut==0:
				self.roll()
			else:
				print("Fitting heroes:")
				for k in self.heroToRandom:
					print("|"+k+"..."+str(self.heroDict[k]))
				print("-"*21)

	#Проведение операции Рандом для отобранного списка и вывод на экран резульата
	def roll(self):
		#print(self.heroToRandom)
		print("Your hero is "+random.choice(self.heroToRandom))
		if cutie.select(["--ReRoll","--Back"])==0:
			self.roll()
	#Вывод всех значений словаря на экран
	def printHeroDict(self):
		print("-"*6+"Hero List"+"-"*6)
		for key in self.heroDict:
			print("|"+key+"..."+str(self.heroDict[key]))
		print("-"*21)
	
	'''
	Главный рабочий цикл
	'''
	def mainWorkflow(self):
		self.oldsAreHere()
		if self.olds==1:
			self.pickleLoad()
		else:
			print("No database found, avalible options:")
			getChoice = cutie.select(["Do initialization cycle","Change DB deafult name and search again"])
			if getChoice == 1:
				self.setDBName()
			else:
				self.initFile()#получаем список героев
				self.initFileKeywords()#получаем список кейвордов
				self.initDict()#формируем словарь
		while(1):
			getChoice=cutie.select(["Roll The Dice!","Print contents of Hero Table","Change atrributes of Hero","Initilaze DataBase(can overwrite it)","Change DataBase name","!!!Manualy save DataBase","Unload formed Hero-Attributes list to txt","Load HeroDict from txt","Select Attr get heroes", "Exit"])#добавть Change Hero Attribute Value+-
			#оптимизировать case/switch через словарь
			if getChoice==0:
				self.workRoll()
			elif getChoice==1:
				self.printHeroDict()
			elif getChoice==2:
				self.changeAttributeInHeroDict()
			elif getChoice==3:
				self.initDBOverwriteCheck()
			elif getChoice==4:
				self.setDBName()
			elif getChoice==5:
				self.pickleDump()
			elif getChoice==6:
				self.heroDictIntoTxt()
			elif getChoice==7:
				self.txtIntoHeroDict()
			elif getChoice==8:
				self.initRoll(listOut=1)
			else:
				self.pickleDump()
				exit()
		



if __name__ == '__main__':
	C=WorkingPicker()
	C.mainWorkflow()



#C.initFile()
#C.heroList=['Axe','Abbadon']
#C.keywordList=['Fun','Lame']
#C.initDBOverwriteCheck()
#C.initRoll()
#print(C.heroDict)
#C.pickleLoad(C.heroDict)
#C.heroDict={}
#C.pickleLoad()
#print(C.heroDict)

"""
try: 
	open("pckDB.dat","rb")
except FileNotFoundError:
	print("lol")
else:
	print("ugar")

try: 
	open("pckDasdasdB.dat","rb")
except FileNotFoundError:
	print("lol")
else:
	print("ugar")
"""