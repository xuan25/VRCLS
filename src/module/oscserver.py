"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

def renewData(unused_addr, args,text,b1, b2):
    params=args[0]
    logger=args[1]
    logger.put({'text':f'收到外源数据: {text}','level':'info'})
    params['serverdata']=text
    
    
def startServer(params,logger):
    ip=params['config']['oscServerIp']
    port=int(params['config']['oscServerPort'])
    params['serverDataMap']=''
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