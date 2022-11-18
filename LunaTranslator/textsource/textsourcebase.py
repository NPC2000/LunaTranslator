import threading  
import time,sqlite3,json,os
from traceback import print_exc
from utils.config import globalconfig
class basetext:
    def __init__(self,textgetmethod)  : 
        self.suspending=False
        self.textgetmethod=textgetmethod  
        self.t=threading.Thread(target=self.gettextthread_)
        self.t.setDaemon(True)
        self.t.start()
        self.sqlfname='./transkiroku/'+self.prefix+'.sqlite'
        self.sqlfname_all='./transkiroku/'+self.prefix+'.premt_synthesize.sqlite'
        self.jsonfname='./transkiroku/'+self.prefix+'.json'
        try:
            def loadjson(self):
                if os.path.exists(self.jsonfname):
                    with open(self.jsonfname,'r',encoding='utf8') as ff:
                        self.json=json.load(ff)
                else:
                    self.json={}
            threading.Thread(target=loadjson,args=(self,)).start()
            
            self.sqlwrite=sqlite3.connect(self.sqlfname,check_same_thread = False, isolation_level=None)
            self.sqlwrite2=sqlite3.connect(self.sqlfname_all,check_same_thread = False, isolation_level=None)
            try:
                self.sqlwrite.execute('CREATE TABLE artificialtrans(id INTEGER PRIMARY KEY AUTOINCREMENT,source TEXT,machineTrans TEXT,userTrans TEXT);')
            except:
                pass
            try:
                self.sqlwrite2.execute('CREATE TABLE artificialtrans(id INTEGER PRIMARY KEY AUTOINCREMENT,source TEXT,machineTrans TEXT);')
            except:
                pass
        except:
            print_exc
    def gettextthread_(self):
        while True:
            if self.ending:
                
                break
            if globalconfig['sourcestatus'][self.typename]==False:
                break
            if globalconfig['autorun']==False  :
                time.sleep(1)
                continue
            #print(globalconfig['autorun'])
            try:
                t=self.gettextthread()
            except:
                t=''
                print_exc()
            if t and globalconfig['autorun']:
                self.textgetmethod(t)
                if self.typename=='ocr':
                    time.sleep(globalconfig['ocrmininterval'])
    def gettextthread(self):
        pass
    def runonce(self):
        pass
    def end(self):
        self.ending=True
 