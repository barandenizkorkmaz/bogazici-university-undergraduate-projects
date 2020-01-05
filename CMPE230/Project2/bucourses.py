#!/usr/bin/env python3
import requests
import urllib.request
from bs4 import BeautifulSoup
import bisect
import sys
import pandas as pd
import csv

tupleList=[['AD','MANAGEMENT'], ['ASIA','ASIAN+STUDIES'], ['ASIA','ASIAN+STUDIES+WITH+THESIS'], ['ATA','ATATURK+INSTITUTE+FOR+MODERN+TURKISH+HISTORY'],
           ['AUTO','AUTOMOTIVE+ENGINEERING'], ['BIO','MOLECULAR+BIOLOGY+%26+GENETICS'], ['BIS','BUSINESS+INFORMATION+SYSTEMS'], ['BM','BIOMEDICAL+ENGINEERING'],
           ['CCS','CRITICAL+AND+CULTURAL+STUDIES'], ['CE','CIVIL+ENGINEERING'], ['CEM','CONSTRUCTION+ENGINEERING+AND+MANAGEMENT'], ['CET','COMPUTER+EDUCATION+%26+EDUCATIONAL+TECHNOLOGY'],
           ['CET','EDUCATIONAL+TECHNOLOGY'], ['CHE','CHEMICAL+ENGINEERING'], ['CHEM','CHEMISTRY'], ['CMPE','COMPUTER+ENGINEERING'],
           ['COGS','COGNITIVE+SCIENCE'], ['CSE','COMPUTATIONAL+SCIENCE+%26+ENGINEERING'], ['EC','ECONOMICS'], ['ED','EDUCATIONAL+SCIENCES'],
           ['EE','ELECTRICAL+%26+ELECTRONICS+ENGINEERING'], ['EF','ECONOMICS+AND+FINANCE'], ['ENV','ENVIRONMENTAL+SCIENCES'], ['ENVT','ENVIRONMENTAL+TECHNOLOGY'],
           ['EQE','EARTHQUAKE+ENGINEERING'], ['ETM','ENGINEERING+AND+TECHNOLOGY+MANAGEMENT'], ['FE','FINANCIAL+ENGINEERING'],
           ['FLED','FOREIGN+LANGUAGE+EDUCATION'], ['GED','GEODESY'], ['GPH','GEOPHYSICS'], ['GUID','GUIDANCE+%26+PSYCHOLOGICAL+COUNSELING'], ['HIST','HISTORY'], ['HUM','HUMANITIES+COURSES+COORDINATOR'],
           ['IE','INDUSTRIAL+ENGINEERING'], ['INCT','INTERNATIONAL+COMPETITION+AND+TRADE'], ['INT','CONFERENCE+INTERPRETING'], ['INTT','INTERNATIONAL+TRADE'], ['INTT','INTERNATIONAL+TRADE+MANAGEMENT'],
           ['LING','LINGUISTICS'], ['LL','WESTERN+LANGUAGES+%26+LITERATURES'], ['LS','LEARNING+SCIENCES'], ['MATH','MATHEMATICS'], ['ME','MECHANICAL+ENGINEERING'],
           ['MECA','MECHATRONICS+ENGINEERING'], ['MIR','INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST'], ['MIR','INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST+WITH+THESIS'],
           ['MIS','MANAGEMENT+INFORMATION+SYSTEMS'], ['PA','FINE+ARTS'], ['PE','PHYSICAL+EDUCATION'], ['PHIL','PHILOSOPHY'], ['PHYS','PHYSICS'],
           ['POLS','POLITICAL+SCIENCE%26INTERNATIONAL+RELATIONS'], ['PRED','PRIMARY+EDUCATION'], ['PSY','PSYCHOLOGY'], ['SCED','MATHEMATICS+AND+SCIENCE+EDUCATION'], ['SCED','SECONDARY+SCHOOL+SCIENCE+AND+MATHEMATICS+EDUCATION'],
           ['SCO','SYSTEMS+%26+CONTROL+ENGINEERING'], ['SOC','SOCIOLOGY'], ['SPL','SOCIAL+POLICY+WITH+THESIS'], ['SWE','SOFTWARE+ENGINEERING'], ['SWE','SOFTWARE+ENGINEERING+WITH+THESIS'],
           ['TK','TURKISH+COURSES+COORDINATOR'], ['TKL','TURKISH+LANGUAGE+%26+LITERATURE'], ['TR','TRANSLATION+AND+INTERPRETING+STUDIES'], ['TRM','SUSTAINABLE+TOURISM+MANAGEMENT'], ['TRM','TOURISM+ADMINISTRATION'],
           ['WTR','TRANSLATION'], ['XMBA','EXECUTIVE+MBA'], ['YADYOK','SCHOOL+OF+FOREIGN+LANGUAGES']]

base = 'https://registration.boun.edu.tr/scripts/sch.asp?donem='

startSemester = sys.argv[1]
endSemester = sys.argv[2]

start1 = int(startSemester[:4])
start2Tmp = startSemester[5:]
start2 = 0
semester1 = 0

end1 = int(endSemester[:4])
end2Tmp = endSemester[5:]
end2 = 0
semester2 = 0
#Here these two if-else blocks creates two terms in the form of XXXX/YYYY-S (e.g. 2018/2019-1) kept in start1,start2,semester1 and end1,end2,semester2
if start2Tmp == 'Fall':
    tmp = int(start1)
    start2 = tmp + 1
    semester1 = 1
elif start2Tmp == 'Spring':
    start2 = int(start1)
    start1 = start2 - 1
    semester1 = 2
elif start2Tmp == 'Summer':
    start2 = int(start1)
    start1 = start2 - 1
    semester1 = 3

if end2Tmp == 'Fall':
    tmp = int(end1)
    end2 = tmp + 1
    semester2 = 1
elif end2Tmp == 'Spring':
    end2 = int(end1)
    end1 = end2 - 1
    semester2 = 2
elif end2Tmp == 'Summer':
    end2 = int(end1)
    end1 = end2 - 1
    semester2 = 3

semesters = []
semesterNames = []

##creating all the terms in order, and storing in the list semesters
while 1:
    if start1 == end1 and start2 == end2 and semester1 == semester2:
        semesters.append(str(start1) + '/' + str(start2) + '-' + str(semester1))
        break

    if semester1 == 4:
        semester1 = 1
        start1 += 1
        start2 += 1
    else:
        semesters.append(str(start1) + '/' + str(start2) + '-' + str(semester1))
        semester1 += 1
##creating terms as headers of the table.
for i in range(0, len(semesters)):
    currentSemester = semesters[i]
    termNumber = int(currentSemester[-1:])
    semesterName = ''
    if termNumber == 1:
        semesterName = currentSemester[0:4] + '-Fall'
    elif termNumber == 2:
        semesterName = currentSemester[5:9] + '-Spring'
    else:
        semesterName = currentSemester[5:9] + '-Summer'
    semesterNames.append(semesterName)

## mainCol that is a list and used to keep a the data is later converted into a table.
mainCol = []
mainCol.append(("Dept./Prog. (name)", []))
mainCol.append(("Course Code", []))
mainCol.append(("Course Name", []))
semesterCount = len(semesters)

# Appending all the semesters to the mainCol list.
for i in range(0, semesterCount):
    mainCol.append((semesterNames[i], []))
mainCol.append(("Total Offerings", []))

for element in tupleList:  ## Reading departments one by one.
    col = []
    col.append(("Dept.", []))
    col.append(("Course Code", []))
    col.append(("Course Name", []))

    kisaAdi = '&kisaadi=' + element[0]
    bolum = '&bolum=' + element[1]
    isFirst = 1
    n = 3 # used in order to know which semester is currently being examined.
    ##These variables are used to keep data about the courses and instructors in a department
    courseListDept = []
    numOfOccurencesList = []
    instructorSetDept = set()
    undergraduateCourseCounterDept = 0
    graduateCourseCounterDept = 0
    instructorListForEachCourse = []
    graduateCourseCounterDeptUnique = 0
    undergraduateCourseCounterDeptUnique = 0

    semesterStatsList = []
    exceptionColumns = []
    for semesterElement in semesters:  ## Reading semesters one by one
        try:
            url = base + semesterElement + kisaAdi + bolum

            r = requests.get(url)

            html_content = r.text

            soup = BeautifulSoup(html_content, 'html.parser')

            myTable = soup.find_all('table', width="1300px")

            myTable = myTable[0]

            if isFirst:
                col.append((semesterElement, []))#adding the first semester column
                isFirst = 0
            else:
                col.append((semesterElement, [' '] * len(col[len(col) - 1][1])))#adding semester columns after the first semester column is added.
            ##These variables are used to keep data about the courses and instructors in a semester for a department.
            tmpCount = 0
            instructorSetSemester = set()
            undergraduateCourseCounterSemester = 0
            graduateCourseCounterSemester = 0
            currentCourseName = ''
            prevCourseName = ''
            for tr in myTable.find_all('tr'): 
                if tmpCount == 0:
                    tmpCount = 1
                    continue
                tds = tr.find_all('td')
                myBool = 0
                i = 0
                index = 0
                for column in tds:
                    i += 1
                    if i == 1: # Reading course code
                        currentCourseName = column.get_text()[:-4]
                        if currentCourseName == '':
                            break
                        myBool = currentCourseName not in courseListDept ##checking if current course was added or not.
                        if myBool:
                            try:
                            	number = int(currentCourseName[-3:-2])
                            except:
                            	number = 0
                            if number >= 5:
                                graduateCourseCounterDeptUnique += 1
                            else:
                                undergraduateCourseCounterDeptUnique += 1
                            bisect.insort(col[i][1], currentCourseName)
                            bisect.insort(courseListDept, currentCourseName)
                            index = courseListDept.index(currentCourseName)
                            numOfOccurencesList.insert(index, 1)
                            for x in range(3, n): ## if a new course is added, mark the past terms as ' '
                                col[x][1].insert(index, ' ')
                            col[n][1].insert(index, 'x')##and mark the new course in the current semester

                        else:
                            index = courseListDept.index(currentCourseName)

                            if not currentCourseName == prevCourseName: ## Avoiding the duplicates(e.g. adding both CMPE150.01 and CMPE150.02)
                                index = courseListDept.index(currentCourseName)
                                numOfOccurences = numOfOccurencesList[index]
                                numOfOccurencesList[index] = numOfOccurences + 1
                                col[n][1][index] = 'x'
                        
                        if not currentCourseName == prevCourseName: ## Avoiding the duplicates(e.g. adding both CMPE150.01 and CMPE150.02)
                            try:
                            	number = int(currentCourseName[-3:-2])
                            except:
                            	number = 0
                            if number >= 5:
                                graduateCourseCounterSemester += 1
                            else:
                                undergraduateCourseCounterSemester += 1
                        prevCourseName = currentCourseName
                    elif i == 3: #Reading course name
                        if myBool:
                            courseName = column.get_text()
                            col[i - 1][1].insert(index, courseName[:-1])

                    elif i == 6: # Reading instructor
                        instructorName = column.get_text()
                        instructorSetSemester.add(instructorName)
                        instructorSetDept.add(instructorName)
                        if myBool:
                            instructorListForEachCourse.insert(index, set())
                        instructorListForEachCourse[index].add(instructorName)

            semesterStatsList.append(
                [undergraduateCourseCounterSemester, graduateCourseCounterSemester, len(instructorSetSemester)])
            undergraduateCourseCounterDept += undergraduateCourseCounterSemester
            graduateCourseCounterDept += graduateCourseCounterSemester
            n += 1
        except:
            exceptionColumns.append((n,semesterNames[n-3]))


    totalOfferings = []
    courseListLength = len(courseListDept)
    for i in range(0, courseListLength):
        currStr = str(numOfOccurencesList[i]) + '/' + str(len(instructorListForEachCourse[i]))
        totalOfferings.append(currStr)

    col.append(('Total Offerings', totalOfferings))
    courseCount = len(courseListDept)
    for i in range(0, courseCount):
        col[0][1].append(' ')

    ##Arranging the department names.
    deptName = element[0] + '('
    myList = element[1].split('+')
    for i in range(0, len(myList) - 1):
        currName = myList[i]
        if currName == '%26':
            deptName += '& '
            continue
        elif currName == '%3a':
            deptName += ': '
            continue
        elif currName == '%2c':
            deptName += ', '
            continue
        deptName += currName + ' '
   
    deptName += myList[len(myList) - 1]
    deptName += ')'

    #Recording the statistics after a department is examined.
    col[0][1].insert(0, deptName) 
    col1Stats = 'U' + str(undergraduateCourseCounterDeptUnique) + ' G' + str(graduateCourseCounterDeptUnique)
    col[1][1].insert(0, col1Stats)
    col[2][1].insert(0, '')
    colLastStats = 'U' + str(undergraduateCourseCounterDept) + ' G' + str(graduateCourseCounterDept) + ' I' + str(
        len(instructorSetDept))
    col[n][1].insert(0, colLastStats)
    for i in range(3, n):
        colSemesterStats = 'U' + str(semesterStatsList[i - 3][0]) + ' G' + str(
            semesterStatsList[i - 3][1]) + ' I' + str(semesterStatsList[i - 3][2])
        col[i][1].insert(0, colSemesterStats)

    totalColumnCount = semesterCount + 4
    
    #Adding the semester to the list for a department that is not opened in that semester.
    for everyElement in exceptionColumns:
        firstElement = everyElement[0]
        secondElement = everyElement[1]
        col.insert(firstElement,(secondElement,[]))
        col[firstElement][1].append('U0 G0 I0')
        for i in range (0,len(courseListDept)):
            col[firstElement][1].append('')
    ##Adding the list col to the main list mainCol
    for i in range(0, totalColumnCount):
        mainCol[i][1].extend(col[i][1])
        col[i][1].clear()

##Converting the main list mainCol into a dictionary.
Dict = {title: column for (title, column) in mainCol}
df = pd.DataFrame(Dict)
#Converting the data frame to a csv table
csv = df.to_csv(encoding='utf-8',index=False)
print(csv)
