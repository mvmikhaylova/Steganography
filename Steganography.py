import numpy as np
from PIL import Image
import math
import os
def PSNR(image):
    img = Image.open(image, 'r')  # открыть изображение
    w, h = img.size
    picture = input("Введите имя изображения для сравнения")
    picture = Image.open(picture, 'r')  # открыть изображение
    image_array = np.array(list(img.getdata()))
    picture_array = np.array(list(picture.getdata()))
    MSE = 0
    max = 0
    for i, j in len(image_array), len(picture_array):
        for a, b in range(0, 3):
            MSE += (image_array[i][a] - picture_array[j][b])**2
            if image_array[i][a] > max:
                max = image_array[i][a]
    MSE = 1/(3*h*w) *MSE
    PSNR = 20*math.log10(max/((MSE)**(1/2)))
    return PSNR

#встраивание в изображение текста
def Encode_text(image):
    choice = int(input("Выберите сколько последних бит пикселя будет использоваться для встраивания информации: 1, 2, 3, 4, 5, 6, 7, 8"))
    message_1 = input("Введите текст для встраивания: ")
    #добавим ключевое слово для удобства расшифровки
    img = Image.open(image, 'r')  # открыть изображение
    width, height = img.size
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    message_1 += "C2r3y4p"
    message = ''
    for i in message_1: #представим сообщение в бинарном виде
        c = bin(ord(i))
        c = c[2:]
        if len(c) < 8:
            c = c[::-1]
            while len(c) != 8:
                c += "0"
            c = c[::-1]
        message += c
    array = np.array(list(img.getdata()))  # возвращает двумерный массив со значениями пикселей RGB или RGBA
    #проверим достаточный ли объем пикселей для шифровки
    if len(message) > len(array) * choice/8:
        print("ОШИБКА: нужен больший размер изображения либо меньший размер текста")
    else:
        index = 0
        for i in range(len(array)):
            for q in range(0, 3):
                if index < len(message):
                    c = bin(array[i][q])
                    if choice == 1:
                        c = c[2:len(c)-1]
                        c += message[index]
                        array[i][q] = int(c, 2)
                        index += 1
                    if choice == 2:
                        c = c[2:len(c)-2]
                        c += message[index] + message[index+1]
                        array[i][q] = int(c, 2)
                        index += 2
                    if choice == 3:
                        c = c[2:len(c)-3]
                        c += message[index:index+3]
                        array[i][q] = int(c, 2)
                        index += 3
                    if choice == 4:
                        c = c[2:len(c) - 4]
                        c += message[index:index+4]
                        array[i][q] = int(c, 2)
                        index += 4
                    if choice == 5:
                        c = c[2:len(c)-5]
                        c += message[index:index+5]
                        array[i][q] = int(c, 2)
                        index += 5
                    if choice == 6:
                        c = c[2:len(c) - 6]
                        c += message[index:index + 6]
                        array[i][q] = int(c, 2)
                        index += 6
                    if choice == 7:
                        c = c[2:len(c)-7]
                        c += message[index:index+7]
                        array[i][q] = int(c, 2)
                        index += 7
                    if choice == 8:
                        c = c[2:len(c) - 8]
                        c += message[index:index + 8]
                        array[i][q] = int(c, 2)
                        index += 8
        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        dest = input("Введите имя итогового изображения: ")
        enc_img.save(dest)
        return "Встраивание завершено"

#print(Encode_text("1.png"))

#встраивание в изображение битовой последовательности
def binary_encode(image):
    choice = int(input("Выберите сколько бит пикселя будет использоваться для кодирования: 1, 2, 3, 4, 5, 6, 7, 8"))
    message_1 = input("Введите сообщение в двоичном виде: ")
    # добавим ключевое слово для удобства расшифровки
    secret = "C2r3y4p"
    for i in secret:  # представим ключевое слово в бинарном виде
        c = bin(ord(i))
        c = c[2:]
        if len(c) < 8:
            c = c[::-1]
            while len(c) != 8:
                c += "0"
            c = c[::-1]
        message_1 += c
    img = Image.open(image, 'r')  # открыть изображение
    width, height = img.size
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    message = ''
    for i in message_1:  # представим сообщение в бинарном виде
        c = bin(ord(i))
        c = c[2:]
        if len(c) < 8:
            c = c[::-1]
            while len(c) != 8:
                c += "0"
            c = c[::-1]
        message += c
    array = np.array(list(img.getdata()))  # возвращает двумерный массив со значениями пикселей RGB или RGBA
    # проверим достаточный ли объем пикселей для шифровки
    if len(message) > len(array) * choice / 8:
        print("ОШИБКА: недостаточное кол-во пикселей изображения для встраивания")
    else:
        index = 0
        for i in range(len(array) + 1):
            for q in range(0, 3):
                if index < len(message):
                    c = bin(array[i][q])
                    if choice == 1:
                        c = c[2:len(c) - 1]
                        c += message[index]
                        array[i][q] = int(c, 2)
                        index += 1
                    if choice == 2:
                        c = c[2:len(c) - 2]
                        c += message[index:index+2]
                        array[i][q] = int(c, 2)
                        index += 2
                    if choice == 3:
                        c = c[2:len(c) - 3]
                        c += message[index:index+3]
                        array[i][q] = int(c, 2)
                        index += 3
                    if choice == 4:
                        c = c[2:len(c) - 4]
                        c += message[index:index+4]
                        array[i][q] = int(c, 2)
                        index += 4
                    if choice == 5:
                        c = c[2:len(c) - 5]
                        c += message[index:index+5]
                        array[i][q] = int(c, 2)
                        index += 5
                    if choice == 6:
                        c = c[2:len(c) - 6]
                        c += message[index:index+6]
                        array[i][q] = int(c, 2)
                        index += 6
                    if choice == 7:
                        c = c[2:len(c) - 7]
                        c += message[index:index+7]
                        array[i][q] = int(c, 2)
                        index += 7
                    if choice == 8:
                        c = c[2:len(c) - 8]
                        c += message[index:index+8]
                        array[i][q] = int(c, 2)
                        index += 8
        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        dest = input("Введите имя итогового изображения: ")
        enc_img.save(dest)
        return 'Встраивание завершено'

#извлечение информации их стегоизображения
def decode_text(image):
    choice = int(input("Выберите сколько бит пикселя использовалось для встраивания информации: 1, 2, 3, 4, 5, 6, 7, 8"))
    img = Image.open(image, 'r')  # открыть изображение
    array = np.array(list(img.getdata()))  # возвращает двумерный массив со значениями пикселей RGB или RGBA
    bit_text = ''
    for i in range(len(array)): #делаем срез последних битов пикселей
        for q in range(0, 3):
            c = bin(array[i][q])
            c = c[2:]
            if choice == 1: #Если для встраивания информации использовался 1 последний бит пикселя
                c = c[-1]
            if choice == 2: #Если для встраивания информации использовалось 2 последних бита пикселя
                c = c[6:]
            if choice == 3: #Если для встраивания информации использовалось 3 последних бита пикселя
                c = c[5:]
            if choice == 4: #Если для встраивания информации использовалось 4 последних бита пикселя
                c = c[4:]
            if choice == 5: #Если для встраивания информации использовалось 5 последних бита пикселя
                c = c[3:]
            if choice == 6: #Если для встраивания информации использовалось 6 последних бита пикселя
                c = c[2:]
            if choice == 7: #Если для встраивания информации использовалось 7 последних бита пикселя
                c = c[1:]
            if choice == 8: #Если для встраивания информации использовались все 8 бит пикселя
                c = c
            bit_text += c
    # Делим строку, полученную на предыдущем этапе, по 8 элементов
    bit_text = [bit_text[i:i+8] for i in range(0, len(bit_text), 8)]
    text = ''
    for i in range(len(bit_text)):
        if text[-7:] == 'C2r3y4p': #ищем ключ среди срезанных элементов, все, что находится до него - искомый текст
            break
        else:
            text += chr(int(bit_text[i], 2))
    if 'C2r3y4p' in text:
        print("Встроенный текст:", text[:-7])
    else:
        print("Встроенный текст не найден")
    return "Извлечение завершено"


#извлечение информации их стегоизображения
def decode_binary(image):
    img = Image.open(image, 'r')  # открыть изображение
    array = np.array(list(img.getdata()))  # возвращает двумерный массив со значениями пикселей RGB или RGBA
    bit_text = ''
    choice = int(input("Выберите сколько бит пикселя использовалось для встраивания информации: 1, 2, 3, 4, 5, 6, 7, 8"))
    for i in range(len(array)):
        for q in range(0, 3):
            c = bin(array[i][q])
            if choice == 1:
                c = c[-1]
            if choice == 2:
                c = c[-2]
            if choice == 3:
                c = c[-3]
            if choice == 4:
                c = c[-4]
            if choice == 5:
                c = c[-5]
            if choice == 6:
                c = c[-6]
            if choice == 7:
                c = c[-7]
            if choice == 8:
                c = c[-8]
            bit_text += c
    bit_text = [bit_text[i:i+8] for i in range(0, len(bit_text), 8)]
    text = ''
    key = 'C2r3y4p'
    for i in range(len(bit_text)):
        if key in text:
            break
        else:
            text += chr(int(bit_text[i], 2))
    if key in text:
        print("Встроенный текст:", text[:-len(key)])
    else:
        print("Встроенный текст не найден")
    return "Извлечение завершено"


#встраивание в изображение изображения
def Encode_image(image):
    choice = int(input("Выберите сколько бит пикселя будет использоваться для кодирования: 1, 2, 3, 4, 5, 6, 7, 8"))
    picture = input("Введите изображение для встраивания: ")
    picture = Image.open(picture, 'r')
    # Добавим ключевое слово для удобства расшифровки
    secret = 'C2r3y4p'
    key = ''
    for i in secret:
        check = bin(ord(i))
        check = check.replace('0b', '')
        if len(check) < 8:
            check = '0' * (8 - len(check)) + check
        key += check
    img = Image.open(image, 'r')  # открыть изображение
    width, height = img.size
    width_1, height_1 = picture.size
    width_1, height_1 = bin(width_1), bin(height_1)
    width_1, height_1 = width_1[2:], height_1[2:]
    width_1_check = ''
    height_1_check = ''
    for i in width_1:
        check = bin(ord(i))
        check = check.replace('0b', '')
        if len(check) < 8:
            check = '0' * (8 - len(check)) + check
        width_1_check += check
    for i in height_1:
        check = bin(ord(i))
        check = check.replace('0b', '')
        if len(check) < 8:
            check = '0' * (8 - len(check)) + check
        height_1_check += check
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    array = np.array(list(img.getdata()))  # возвращает двумерный массив со значениями пикселей RGB или RGBA
    array_picture = np.array(list(picture.getdata()))
    # проверим достаточный ли объем пикселей для шифровки
    bit = ''
    for i in range(len(array_picture)):
        for q in range(0, 3):
            c = bin(array_picture[i][q])
            c = c.replace('0b', '')
            if len(c) < 8:
                c = '0' * (8 - len(c)) + c
            bit += c
    bit += key + width_1 + key + height_1 + key
    index = 0
    if len(array_picture) > len(array) * choice / 8:
        print("ОШИБКА: недостаточное кол-во бит для встраивания изображения")
    else:
        for i in range(len(array)):
            for q in range(0, 3):
                if index < len(bit):
                    c = bin(array[i][q])
                    c = c.replace('0b', '')
                    if choice == 1:
                        c = c[:len(c) - 1]
                        c += bit[index]
                        index += 1
                    if choice == 2:
                        c = c[:len(c) - 2]
                        c += bit[index:index + 2]
                        index += 2
                    if choice == 3:
                        c = c[len(c) - 3]
                        c += bit[index:index + 3]
                        index += 3
                    if choice == 4:
                        c = c[len(c) - 4]
                        c += bit[index:index + 4]
                        index += 4
                    if choice == 5:
                        c = c[2:len(c) - 5]
                        c += bit[index:index + 5]
                        index += 5
                    if choice == 6:
                        c = c[2:len(c) - 6]
                        c += bit[index:index + 6]
                        index += 6
                    if choice == 7:
                        c = c[2:len(c) - 7]
                        c += bit[index:index + 7]
                        index += 7
                    if choice == 8:
                        c = c[2:len(c) - 8]
                        c += bit[index:index + 8]
                        index += 8
                    array[i][q] = int(c, 2)
        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        dest = input("Введите имя итогового изображения: ")
        enc_img.save(dest)
        return "Встраивание завершено"

#извлечение изображения из изображения
def decode_image(image):
    choice = int(input("Выберите сколько бит использовалось для встраивания: 1, 2, 3, 4, 5, 6, 7, 8"))
    img = Image.open(image, 'r')  # открыть изображение
    array = np.array(list(img.getdata()))  # возвращает двумерный массив со значениями пикселей RGB или RGBA
    bit_text = ''
    for i in range(len(array)):
        for q in range(0, 3):
            c = bin(array[i][q])
            c = c[2:]
            if len(c) < 8:
                c = c[::-1]
                while len(c) != 8:
                    c += "0"
                c = c[::-1]
            if choice == 1:
                c = c[-1]
            if choice == 2:
                c = c[6:]
            if choice == 3:
                c = c[5:]
            if choice == 4:
                c = c[4:]
            if choice == 5:
                c = c[3:]
            if choice == 6:
                c = c[2:]
            if choice == 7:
                c = c[1:]
            if choice == 8:
                c = c
            bit_text += c
    binary = bit_text
    key = 'C2r3y4p'
    secret = ''
    for i in key:  # представим секретное слово в бинарном виде
        c = bin(ord(i))
        c = c[2:]
        if len(c) < 8:
            c = c[::-1]
            while len(c) != 8:
                c += "0"
            c = c[::-1]
        secret += c
    width, height = '', ''
    text = ''
    f, y = '', ''
    bit_text = [bit_text[i:i + 8] for i in range(0, len(bit_text), 8)]
    r = ''
    for i in range(len(bit_text)):
        if text.count(key) == 1:
            width += str(bit_text[i])
        if text.count(key) == 2:
            height += str(bit_text[i])
        if text.count(key) == 3:
            break

        text += chr(int(bit_text[i], 2))
    width, height = int(width[:-len(secret)], 2), int(height[:-len(secret)], 2)
    binary = binary[:height*width*3*8]
    img2 = Image.new('RGBA', (width, height), 'white')
    w, h = img2.size
    posled2 = np.array(list(img2.getdata()))
    t = 0
    k = 0
    message_check = ''
    for i in range(len(binary)):
        message_check += binary[i]
        if len(message_check) == 8:
            message = str(int(message_check, 2))
            message_check = ''
            posled2[t][k] = int(message)
            if k == 2:
                k = -1
                t += 1
            k += 1
    posled2 = posled2.reshape(h, w, 4)
    enc_img = Image.fromarray(posled2.astype('uint8'), img.mode)
    dest = input("Введите имя итогового изображения: ")
    enc_img.save(dest)
    return "Извлечение завершено"


while True:
    a = input("Введите номер операции: \n"
                  "1. Встраивание текста в изображение \n"
                  "2. Извлечение текста из изображения \n"
                  "3. Встраивание битовой последовательности в изображение\n"
                  "4. Извлечение битовой последовательности из изображения\n"
                  "5. Встраивание изображения в изображение\n"
                  "6. Извлечение изображения из изображения\n"
                  "7. Закончить")
    if a == '1':
        print(Encode_text(input('Введите изображение, в которое будет встраиваться текст: ')))
    if a == '2':
        print(decode_text(input('Введите изображение, из которого будет извлекаться текст: ')))
    if a == '3':
        print(binary_encode(input('Введите изображение, в которое будет встраиваться битовая последовательность: ')))
    if a == '4':
        print(decode_binary(input('Введите изображение, из которого будет извлекаться битовая последовательность: ')))
    if a == '5':
        print(Encode_image(input('Введите изображение, в которое будет встраиваться изображение: ')))
    if a == '6':
        print(decode_image(input('Введите изображение, из которого будет извлекаться изображение: ')))
    else:
        break
