import requests
from bs4 import BeautifulSoup
from datetime import date


def setYear():
    year = input('Enter year: ')
    year = year.strip()
    while True:
        if year.isdigit():
            if len(year) == 3:
                if 101 <= int(year) <= (currentYear - 1911):
                    return year
            elif len(year) == 4:
                if 2012 <= int(year) <= currentYear:
                    return str(int(year) - 1911)
        year = input('Invalid input. Enter year again: ')
        year = year.strip()


def setMonth():
    month = input('Enter month: ')
    month = month.strip()
    while not month.isdigit() or int(month) > 12 or int(month) < 1:
        month = input('Invalid input. Enter month again: ')
        month = month.strip()
    if int(month) % 2 == 0:
        return str(int(month) - 1)
    else:
        return month


def checkReleased():
    if year == str(currentYear - 1911):
        if int(month) < currentMonth - 2:
            return True
        elif int(currentMonth) % 2 != 0 and int(month) == currentMonth - 2 and currentDate > 25:
            return True
        return False
    elif year == str(currentYear - 1912) and month == '11':
        if currentMonth == 1 and currentDate > 25 or currentMonth > 1:
            return True
        return False
    else:
        return True


def generateUrl():
    url = 'https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_'
    url += year

    if int(month) < 10:
        url += ('0' + month)
    else:
        url += month
    return url


def processList(li):
    for i in range(0, 4):
        li[i] = li[i].strip()
    li[2] = li[2].split()
    li[3] = li[3].split('、')
    return li


def checkNum(num):
    num = num.strip()
    if len(num) != 8:
        return 0
    else:
        if num == numList[0]:  # speceial prize
            return prize[0]
        elif num == numList[1]:  # grand prize
            return prize[1]
        else:
            for i in range(0, len(numList[2])):  # first~sixth prize
                for j in range(0, 6):
                    if numList[2][i][j:8] == num[j:8]:
                        return prize[j + 2]
            for i in range(0, len(numList[3])):  # bonus sixth
                if numList[3][i] == num[5:8]:
                    return prize[7]
        return 0


today = date.today()
currentYear = today.year
currentMonth = today.month
currentDate = today.day

while True:
    while True:
        year = setYear()
        month = setMonth()
        if checkReleased() == True:
            break
        else:
            print('Haven\'t released yet')

    url = generateUrl()
    req = requests.get(url)
    html = req.content.decode('utf8')

    bs = BeautifulSoup(html, 'html.parser')
    i = 0
    numList = ['', '', '', '']
    for result in bs.findAll('td', {'class': 'number'}):
        numList[i] = result.text
        i += 1

    numList = processList(numList)
    prize = [10000000, 2000000, 200000, 40000, 10000, 4000, 1000, 200]

    print('Special Prize:', numList[0])
    print('Grand Prize:', numList[1])
    print('First~Sixth Prizes:')
    for i in range(0, len(numList[2])):
        print(numList[2][i])
    print('Bonus Sixth Prize:')
    for i in range(0, len(numList[3])):
        print(numList[3][i])

    reward = 0
    while True:
        inNum = input('Enter invoice number (enter \'q\' to quit): ')
        if inNum == 'q':
            print('accumulated reward: $', reward)
            break
        else:
            reward += checkNum(inNum)
        print('accumulated award: $', reward)

    cmd = input('Enter \'y\'es to continue: ')
    if cmd != 'y':
        break
