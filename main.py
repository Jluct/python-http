import http.client
import os.path
from urllib.parse import urlparse
import datetime


def myConnection(address: str, method="GET", params=''):
    setting = {
        "Accept": "text/html, text/plain, application/xml",
        "Accept-Language": "ru, ru-RU",
        "Accept-Charset": "utf-8",
    }

    connect = http.client.HTTPConnection(address)
    connect.request(method, params, headers=setting)
    return connect.getresponse()


userAddressUrl = False
while userAddressUrl == False:

    userAddressUrl = str(input('Enter address : '))
    addressUrl = "www." + userAddressUrl + ":80"
    if (addressUrl):
        break
    else:
        print("Вы не ввели адрес URL")

result = myConnection(addressUrl)

if (result.status != 200):
    if (int(result.status) == 302 or int(result.status) == 301):
        params = list(urlparse(str(result.getheader('Location'))))
        urlPatch = params[2] + params[3] + params[4] + params[5]
        print(result.getheader('Location'))
        print(urlPatch)

        result = myConnection(address=params[1], params=urlPatch)
    elif (result.status == 405):
        result = myConnection(addressUrl, "POST")
    else:
        print("Ошибка получения страницы! Статус ответа {0}".format(result.status))
        print(result.read())
        print(result.getheader('Location'))
        input()

pageFile = userAddressUrl + '.html'
userRequest = False
while userRequest == False:
    if (os.path.isfile(pageFile)):
        print("Файл {0} существует. Перезаписать его? Y/N ".format(pageFile))
        userRequest = input()
        if (userRequest == 'Y' or userRequest == 'y'):
            userRequest = True
            break
        elif (userRequest == 'N' or userRequest == 'n'):
            now = datetime.datetime.now()
            pageFile = 'D:\Книги\\' + addressUrl + "_" + now.strftime("%d-%m-%Y_%H:%M") + '.html'
            userRequest = True
            break
        else:
            print('Не корректный ответ. Введите Y/N')
            userRequest = False
    else:
        userRequest = True
        break

dataUrl = str(result.read().decode('UTF-8'))
print(pageFile)
file = open(pageFile, 'w+')
file.write(dataUrl)
file.close()

result.close()
print('Ok')
