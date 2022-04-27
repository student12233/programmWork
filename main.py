



import numpy as np
class Processor:
    def __init__(self,ver,name):
        self.coof=ver
        self.time_work=0
        self.name=name
        self.enabled=0
        self.orders=0
        self.time_start=0
        self.zakaz=0
        self.mass_orders=0
        self.orders_koll=[]
    def connect_timeline(self,timeline):
        self.timeline=timeline
    def start_create_obr(self,time):
        if self.enabled==0:
            self.timeline.add_event({"name":self.name+" конец создания", "time":self.ver(),"functions":[self.end_create_obr]})
            self.enabled=1
            self.time_start = self.timeline.time
            self.orders_koll[0]["time_queue"]=self.orders_koll[0]["time_queue"]+(self.timeline.time-self.orders_koll[0]["tec_time"])
    def end_create_obr(self,time):
        self.time_work =self.time_work+ (time-self.time_start)
        self.orders_koll[0]["time_work"] = self.orders_koll[0]["time_work"] + (time-self.time_start)
        self.enabled=0
        self.pop_orders(0)
        self.zakaz+=1
        if self.orders !=0:
            self.timeline.add_event({"name": self.name + " начало создания", "time": time, "functions": [self.start_create_obr]})
    def get_orders(self,time):
        self.orders+=1
        self.timeline.orders_all+=1
        tec_orders=self.timeline.tec_order.copy()
        tec_orders["path"]=tec_orders["path"]+"_"+self.name
        self.orders_koll.append(tec_orders)
    def pop_orders(self,time):
        self.orders-=1
        self.orders_koll[0]["tec_time"]=timeline.time
        self.timeline.tec_order=self.orders_koll.pop(0)
    def get_statistics(self):
        return self.name+"\n     время работы: "+str(self.time_work)+"\n     количество обработанных задач: "+str(self.zakaz)+"\n     количество заявок в очереди: "+str(self.orders)+"\n     коэффициент загрузки: "+str(round(self.time_work/self.timeline.time,2))+"\n     простой: "+str(round((self.timeline.time-self.time_work)/self.timeline.time,2)*100)+"%" + "\n <--------------------------------->"
    def ver(self):
       return np.random.normal(self.coof[0],self.coof[1])+self.timeline.time



class Timeline:
    def __init__(self,mass_proc):
        self.processors=mass_proc
        for i in self.processors:
            i.connect_timeline(self)
        self.enabled=0
        self.orders_all=0
        self.time=0
        self.zakaz=0
        self.history=[]
        self.order_history=[]
        self.tec_order={"path":"","time_queue":0,"time_work":0,"tec_time":self.time}
        self.events = [{"name": "заявка", "time": 0, "functions": [self.get_order,self.get_processors]}]
        self.time_work=0
        self.time_save_enable=0
        self.order_stats=0
        self.path=[]
        self.rasp=[]
    def add_event(self,el):
        self.events.append(el)
        self.events.sort(key=lambda x: x["time"])
    def get_order(self,time):
        new_time= self.order_stats(self.time)
        self.add_event({"name": "заявка", "time": new_time, "functions":[self.get_order,self.get_processors]})
    def get_processors(self,time):
        tec_proc = self.get_rand_processor()
        self.tec_order = {"path": "", "time_queue": 0, "time_work": 0, "tec_time": self.time}
        self.add_event({"name": tec_proc.name+" отослана заявка", "time": self.time,"functions": [tec_proc.get_orders]})
        if tec_proc.enabled==0:
            self.add_event({"name": tec_proc.name + " начало создания", "time": self.time, "functions": [tec_proc.start_create_obr]})
    def get_processors_con(self,proc):
        self.add_event({"name": proc.name + " отослана заявка", "time": self.time, "functions": [proc.get_orders]})
        if proc.enabled == 0:
            self.add_event({"name": proc.name + " начало создания", "time": self.time,"functions": [proc.start_create_obr]})
    def get_rand_processor(self):
        rd = np.random.rand()
        k = 0
        for i in self.rasp:
            if rd >= i[0] and rd < i[1]:
                return self.processors[k]
            k+=1
    def is_enabled(self):
        c=0
        for i in self.processors:
            if i.enabled ==1:
                c=1
        if c == 0 and self.enabled!=0:
            self.time_save_enable = self.time
        elif c==1 and self.enabled!=1:
            self.time_work = self.time_work + (self.time - self.time_save_enable)
        self.enabled=c
    def get_tik_simulator(self):
        tec_events = self.events.pop(0)
        self.time = tec_events["time"]
        if tec_events["name"].find("конец создания")!=-1:
            for i in tec_events["functions"]:
                i(self.time)
            root=[]
            for i in self.path:
                if tec_events["name"].find(i[0])!=-1:
                    root.append(i)
            rand_two=np.random.rand()
            for i in root:
                if rand_two>=i[2] and rand_two<i[3]:
                    if i[1]=="T":
                        self.zakaz += 1
                        self.order_history.append(self.tec_order)
                    else:
                        self.get_processors_con(self.search_process(i[1]))
                    break
        else:
            for i in tec_events["functions"]:
                i(self.time)
        self.history.append({"name":tec_events["name"],"time":tec_events["time"]})
        self.is_enabled()
    def get_history(self):
        str_rez=""
        for i in self.history:
            str_rez=str_rez+str(i)+"\n"
        return str_rez
    def get_statistic(self):
        str_rez = ""
        for i in self.processors:
            str_rez = str_rez + i. get_statistics() + "\n"
        str_rez = str_rez + "время: "+str(self.time)+"\nколичество выполненых задач: "+str(self.zakaz)+"\n" + "<---------------------------------> \n"
        mass_path=set()
        for i in self.order_history:
             mass_path.add(i["path"])
        for i in mass_path:
            mass_con_path=[]
            for j in self.order_history:
                if i==j["path"]:
                    mass_con_path.append(j)
            time_och=0
            time_work=0
            for j in mass_con_path:
                time_och=time_och+j["time_queue"]
                time_work=time_work+j["time_work"]
            kol = len(mass_con_path)
            str_rez = str_rez + "статистика заявок на данном пути: "+ i+"\n     Среднее время очереди: "+ str(time_och/kol)+"\n     Среднее время задачи: "+ str(time_work/kol)+ "\n     Количество заявок: "+str(kol)+"\n     Процентное соотношение относительно всех заявок: "+str(round(kol/len(self.order_history)*100,0))+"%\n" + "<--------------------------------->\n"
        time_och = 0
        time_work = 0
        for i in self.order_history:
            time_och = time_och + i["time_queue"]
            time_work = time_work + i["time_work"]
        kol = len(self.order_history)
        # str_rez = str_rez + "Статистика по всем заявкам:" + "\n     Среднее время очереди: " + str(time_och / kol) + "\n    Среднее время задачи: " + str(time_work / kol) + "\n<--------------------------------->\n"
        # str_rez = str_rez + "абсолютная пропускная способность: " + str(self.zakaz/self.time)+"\n<--------------------------------->\n"
        # str_rez = str_rez + "относительная пропускная способность: " + str((self.zakaz / self.time)/(self.orders_all/self.time)) + "\n<--------------------------------->\n"
        # str_rez = str_rez + "коэффициент загрузки всей программы: " + str(1-self.time_work/self.time) + "\n<--------------------------------->\n"
        return str_rez
    def get_orders_history(self):
        str_rez = ""
        for i in self.order_history:
            str_rez = str_rez + str(i) + "\n"
        return str_rez

    def get_order_stat(self,val):
        self.order_stats = val
    def set_path(self,val):
        self.path=val
    def set_rasp(self,val):
        self.rasp=val
    def search_process(self,name):
        for i in self.processors:
            if name.find(i.name)!=-1:
                return i

kolwo_powtor = int(input("Количество опытов для проверки: "))
kol=int(input("Количество процессоров: "))
mass_proc=[]
for i in range(1,kol+1):
    proc1 = int(input("Введите значения мат ожидания времени работы " + str(i) + " ЭВМ: "))
    proc2 = int(input("Дисперсия: "))
    mass_proc.append([proc1,proc2])
task1 = float(input("Введите значение мат ожидания интенсивности поступления задачи: "))
task2 = float(input("Дисперсия: "))
integ =float(input("Требуемое количество деталей: "))
mass_ver =[]
tec_ver=0
for i in range(1,kol+1):
    tk =float(input("Вероятность выбора " +str(i) + " процессора(0,1): "))
    mass_ver.append([tec_ver,tec_ver+tk])
    tec_ver=tec_ver+tk
mass_path=[]
str_path=input("Начальное значение пути: ")
tec_ver = 0
while str_path!="end":
    rr1=input("Конечное значение пути: ")
    ver=float(input("Вероятность перехода: "))
    mass_path.append([str_path,rr1,tec_ver,tec_ver+ver])
    tec_ver=tec_ver+ver
    str_path = input("Начальное значение пути: ")
    if tec_ver>=1:
        tec_ver=0

time=0
absolutle=0
otnos=0
koof_zag=0
timeline=0
for j in range(1,kolwo_powtor+1):
    kol=1
    processors=[]
    for i in mass_proc:
        processor= Processor(i,"процессор"+str(kol))
        processors.append(processor)
        kol+=1
    timeline = Timeline(processors)

    timeline.get_order_stat(lambda x: np.random.normal(loc=task1,scale=task2) + x)
    timeline.set_rasp(mass_ver)
    timeline.set_path(mass_path)





    while timeline.zakaz!=integ:
        timeline.get_tik_simulator()
    time=time+timeline.time
    absolutle=absolutle+(timeline.zakaz/timeline.time)
    otnos=otnos+((timeline.zakaz / timeline.time)/(timeline.orders_all/timeline.time))
    koof_zag=koof_zag+(1 - timeline.time_work / timeline.time)

    # print(timeline.get_history())
    # print(timeline.get_orders_history())
print(timeline.get_history())
print(timeline.get_statistic())
print("время работы программы в среднем: "+str(time/kolwo_powtor))
print("абсолютная пропускная способность в среднем: "+str(absolutle/kolwo_powtor))
print("абсолютная относительная способность в среднем: "+str(otnos/kolwo_powtor))
print("коэффициент загрузки всей программы в среднем: "+str(koof_zag/kolwo_powtor))

















