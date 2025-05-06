"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""


class ResettableTimer:
    def __init__(self):
        
        self.timer = None

    def schedule_task(self, task_func):
        import threading
        # 取消已有定时器
        if self.timer:
            self.timer.cancel()
        # 新建定时器（5秒后执行任务）
        self.timer = threading.Timer(5.0, task_func)
        self.timer.start()







    
    
def startServer(params,logger):
    
    from pythonosc.dispatcher import Dispatcher
    from pythonosc import osc_server
    
    # 使用示例
    timer_manager = ResettableTimer()
    # def clearData():
    #     params['serverdata']=''
    def renewData(unused_addr, args,text,b1, b2):
        params=args[0]
        logger=args[1]
        logger.put({'text':f'收到外源数据: {text}','level':'info'})
        params['serverdata']=text
        # on_data_updated()
    # def on_data_updated():
    #     print("数据更新，重置计时器")
    #     timer_manager.schedule_task(clearData)
    ip=params['config']['oscServerIp']
    port=int(params['config']['oscServerPort'])
    params['serverdata']=''
    dispatcher = Dispatcher()
    dispatcher.map("/chatbox/input", renewData,params,logger)
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    logger.put({'text':"OSC服务端启动 {}".format(server.server_address),'level':'info'})
    server.serve_forever()

# if __name__ == "__main__":

#   dispatcher = Dispatcher()
#   dispatcher.map("/chatbox/input", renewData,'abc123','cba12')

#   server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 9003), dispatcher)
#   print("Serving on {}".format(server.server_address))
#   server.serve_forever()