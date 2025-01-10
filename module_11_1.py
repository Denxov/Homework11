from time import time, sleep
import requests
from PIL import Image, ImageTk
import threading
from threading import Event
# from tkinter import Label,Tk
import tkinter
from random import random


class Utumba():
    def __init__(self, url, query):
        self.th = []
        self.data = ''
        self.lock = threading.Lock()
        self.shown = 0
        self.url_list = []
        self.full = Event()
        self.counter = 0
        self.query = query
        self.root = tkinter.Tk()
        self.label = tkinter.Label(text="Start")
        self.img = Image.new('RGB', (1280, 720), 'black')
        # self.img.save('utumba.png')
        self.photo = ImageTk.PhotoImage(self.img)
        self.panel = tkinter.Label(self.root, image=self.photo)
        self.panel.pack(side="bottom", fill="both", expand="yes")
        self.label.pack()
        # посылаем запрос в Ютуб с использованием библиотеки Requests
        while self.data == '':
            try:
                self.data = requests.get(url + query, timeout=2.7).text
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                sleep(random() * 2)
        self.start_time = time()
        self.go(23)  # запускаем 23 потока (плюс добавляются случайное число дублирующих потоков
        self.update()
        self.root.mainloop()

    def update(self):
        now = time() - self.start_time
        # now=now.strftime("%M:%S")
        self.go(1)
        self.photo = ImageTk.PhotoImage(self.img)
        self.panel.configure(image=self.photo)
        if self.full.is_set() == False:
            self.label.configure(
                text=f'Запрос={self.query} Threads={self.counter} Images={self.shown} Время:{round(now, 1)}')
        self.root.after(int(random() * 1000), self.update) # Обновляем окно раз в сек

    # поиск ссылки в коде страницы возвращенной ютуб по текстовому запросу
    def get_img_url(self, num):
        cont_str = str(self.data)
        counter = 0
        pos_in_content = 0
        # pos_in_content=cont_str.find('maxresdefault')
        while counter < num and pos_in_content > -1:
            pos_in_content = cont_str.find('https://i.ytimg.com/vi', pos_in_content + 1)
            counter += 1
        if pos_in_content != -1:
            endpos = cont_str.find('.jpg' or '.png', pos_in_content)
            url_str = cont_str[pos_in_content:endpos + 4]
            if len(url_str) < 100:
                return url_str
            else:
                return ''
        else:
            return 'end'

    def add_thumb(self, url_str):
        print(url_str)
        if url_str != '' and self.full.is_set() == False:
            try:
                # raw = requests.get(url_str, stream=True,timeout=(random()*4.7,17)).raw
                raw = requests.get(url_str, stream=True).raw
            except requests.exceptions.Timeout:
                print("Timed out")
                # sleep(random()*5)
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
            else:
                img = Image.open(raw)
                if img.width >= 320:
                    img_res = img.resize((320, 240)) #масштабируем картинку под размер плитки
                    if not url_str in self.url_list and self.full.is_set() == False:# проверяем на дубли и заполненность
                        self.lock.acquire()  # Включение блокировки при добавлении новой плитки
                        self.img.paste(img_res, ((self.shown + 4) % 4 * 320, 240 * (self.shown // 4)))
                        img.close()
                        self.shown += 1
                        self.url_list.append(url_str)
                        self.lock.release()
                        if self.shown >= 12: self.full.set()# установка флага заполнения поля 12 плиток

    def go(self, num_threads):
        for i in range(num_threads):
            if self.full.is_set() == False:
                url_str = self.get_img_url(self.counter)
                if url_str == 'end':
                    self.counter = 0
                    self.full.set()
                for i in range(round(random() * 2) + 1):  # Случайное к-во потоков на 1 картинку
                    self.th.append(threading.Thread(target=self.add_thumb, args=(url_str,)))
                    self.th[len(self.th) - 1].start()
                    self.counter += 1
                    sleep(random() * self.counter // 250)

strin=input('Введите текстовый запрос для отправки в Ютуб(по умолчанию (Etnter=Природа) -->')
if strin=='':
    strin='Природа'
url='https://www.youtube.com/results?search_query='
UT1=Utumba(url,strin)







