# Spain's_Medicine_Admissions_App

## 1. Introduction
### 1.1 Context summary
Historically, Medicine has always been one of the most demanded careers to study in Spain. Nowadays, it’s still one of the hardest careers to get in, due to the high demand of people wanting to study this career in a public university (because of economic pricing, big difference in comparison to a private university, plus reputational reasons) and the very few available slots for students.

To be able to study this career in Spain, you need to achieve a certain average score in “Selectividad”. “Selectividad” is the popular name given to the Spanish University Admission Tests ("Evaluación de Acceso a la Universidad", E.v.A.U.), a non-compulsory exam taken by students after secondary school. Students must take six 90-minute written exams over three days in June/July, consisting of common and specific subjects taken in "Bachillerato" (the last two non-compulsory years of secondary education). “Selectividad” exams are set by the Public Universities of each autonomous community and allow students access to the Spanish university system.

Once you do “Selectividad” the universities publish the score you need in order to enter their university, this score is a number ranging from 0 to 14. They publish these scores in the web pages corresponding to each university, meaning that applicants need to consult these scores in each of the university web pages, making it hard to have a holistic view. There are a few web pages that consolidate this information and put it in one single place to have centralized platform. However, these web pages show just a table containing the scores from the different universities and do not show any visualizations or filters in order to facilitate students consult this information. In addition, many students suffer uncertainty every year because of not knowing what the scores would be the next year (to see if they could finally be admitted in a university to study this career), therefore, one of the objectives will be to predict the next year scores (2022).

### 1.2 Objective
There are two objectives for this project:
1)	Predict next year scores (2022): data source has data ranging from 2010 to 2021
2)	Create a centralized and accessible place, in this case it will be a web app, to consult the different Medicine admission grades from all the universities in Spain, in a visual and helpful manner. This app will help people save time by not having to go to each of the universities web pages to consult the different scores. Also, it will help guide the user in order to make the decision that works best for them.

### 1.3 Repository
This repository has three different folders:
-	final_master_thesis: folder in which a .pdf document is stored which explains the entire project
-	notebook: jupyter notebook (Spain_Medicine_Admissions_App.ipynb) containing all the code from this project except for the front-end
-	streamlit: file (myapp.py) containing code corresponding to the front-end application built on streamlit. To execute this file just run the following command on your terminal, entering your directory: streamlit run “your directory” /myapp.py

Please see below a diagram showcasing the workflow followed to build this project:

<img width="719" alt="image" src="https://user-images.githubusercontent.com/92814876/173615749-e047e1e9-c976-40e8-a106-88c468787b48.png">

In order to replicate the work done you will need to have access to Python 3.

To execute the two coding files (Spain_Medicine_Admissions_App.ipynb and myapp.py), you would need to create two folders within your home directory:
1)	 “raw_data”, being your directory ‘/Users/your_home/raw_data’: here you would store the different csv files. Details of the data source will be explained on section 2 (data obtention). Enter highlighted directory in Spain_Medicine_Admissions_App.ipynb.
2)	“output”, being your directory ‘/Users/your_home/output’: the output csv coming from 
Spain_Medicine_Admissions_App.ipynb will be stored here. Enter highlighted directory in myapp.py.

All Python libraries that need to be installed appear at the beginning of the coding files (Spain_Medicine_Admissions_App.ipynb and myapp.py).

## 2. Data Obtention
In this section we will be describing the source from which we got the data to do this project.
### 2.1 Web page
The source of data is coming from a web page called “ACCESO A LAS FACULTADES DE MEDICINA DE ESPAÑA Y NOTAS DE CORTE” that you can find in the following link:
-	https://sites.google.com/site/notasdecorte/

The data we are using is found on the left side of the web page (“Notas de corte de medicina year/year+1”):

<img width="725" alt="image" src="https://user-images.githubusercontent.com/92814876/173616174-85433f2e-8a98-4624-80e5-1cb02887555b.png">


Data used for this project is going from the period of year 2010-2011 till 2021-2022, 12 years:
1)	2010/2011
2)	2011/2012
3)	2012/2013
4)	2013/2014
5)	2014/2015
6)	2015/2016
7)	2016/2017
8)	2017/2018
9)	2018/2019
10)	2019/2020
11)	2020/2021
12)	2021/2022


## 3. Front-end
The front-end has been done on streamlit, to use it you will need to run the “myapp.py” file: streamlit run “your directory” /myapp.py

Preview of front-end:


https://user-images.githubusercontent.com/92814876/173628140-ad8b6d85-f1ad-41cb-a274-4b9be916f0a4.mp4



Link to complete video on YouTube: https://youtu.be/hWlolS7YmA4![image](https://user-images.githubusercontent.com/92814876/173616864-93e320fd-cd47-4c76-8136-cd0c2e4b7743.png)
