
from translator.basetranslator import basetrans
import json,requests
from myutils.config import globalconfig
import websocket,time
class basetransdev(basetrans): 
    target_url=None
    def check_url_is_translator_url(self,url):
        return url.startswith(self.target_url)
    
    def Page_navigate(self,url):
        self._SendRequest(self.ws,'Page.navigate',{'url':url})
        self._wait_document_ready()
    def Runtime_evaluate(self,expression):
        return self._SendRequest(self.ws,'Runtime.evaluate',{"expression":expression})  
    def wait_for_result(self,expression,badresult=''):
        for i in range(10000):
            state =self.Runtime_evaluate( expression)
            try:
                if state['result']['value']!=badresult:
                    return state['result']['value']
            except:
                pass
            time.sleep(0.1)
#########################################
    def _private_init(self):
        self._id=1      
        self._createtarget()  
        super()._private_init()
    def _SendRequest(self,ws,method,params): 
        self._id+=1
        try:
            ws.send(json.dumps({'id':self._id,'method':method,'params':params}))
            res=ws.recv()
        except ConnectionAbortedError as e:
            self._createtarget()
            raise e
        return json.loads(res)['result']
     

    def _createtarget(self  ): 
        port=globalconfig['debugport']
        url=self.target_url
        infos=requests.get('http://127.0.0.1:{}/json/list'.format(port)).json() 
        use=None
        for info in infos: 
            if self.check_url_is_translator_url(info['url']):
                use=info['webSocketDebuggerUrl']
                break
        if use is None: 
                ws=websocket.create_connection(infos[0]['webSocketDebuggerUrl'])  
                a=self._SendRequest(ws,'Target.createTarget',{'url':url})  
                ws.close()
                use= 'ws://127.0.0.1:{}/devtools/page/'.format(port)+a['targetId']
        self.ws=websocket.create_connection(use)  
        self._wait_document_ready()
    
    def _wait_document_ready(self):  
        for i in range(10000):
            state =self.Runtime_evaluate( "document.readyState")
            try:
                if state['result']['value']=='complete':
                    break
            except:
                pass
            time.sleep(0.1)
    