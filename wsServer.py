from simple_websocket_server import WebSocketServer, WebSocket
from snowflake import get_snowflake
import websocket, threading, zlib, json, datetime

try:
    import thread
except ImportError:
    import _thread as thread
import time

messages = []
returnMessages = []
#decompress_obj = zlib.decompressobj()
compress_obj = zlib.compressobj()
count = 0
running = False
clients = []

def compressData(data):
    global compress_obj
    return compress_obj.compress(data.encode()) + compress_obj.flush(zlib.Z_FULL_FLUSH)

with open('shidcordInject.txt') as json_file:
    messageToInject = json.load(json_file)

#print(messageToInject)

def debugMessage(message):
    with open('shidcordDebug.txt', 'a') as outfile:
        outfile.write("\n" + "\n")
        json.dump(message, outfile)

def messageWatchdog():
    global returnMessages, count, clients
    while True:
        if len(returnMessages) > count:
            for x in clients:
                print("<S<",returnMessages[count][0:10])
                x.send_message(returnMessages[count])
            count+=1

#Basic outgoing server
def on_message(ws, message):
    global returnMessages, compress_obj
    #print("OUT",message[0:40],"LEN", len(message))

    recompressedMsg = compressData(message)
    #print("COMP",recompressedMsg[0:40], "LEN", len(recompressedMsg))

    currentMsgJson = json.loads(message)["t"]
    #print("ADDING MSG TO QUEUE",message[0:20],"TYPE:",currentMsgJson)

    if currentMsgJson == "MESSAGE_CREATE":
        debugMessage(message)

    #print("DEBUG",recompressedMsg[0:10])

    returnMessages.append(recompressedMsg)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        global messages, running
        while True:
            if running == False:
                ws.close()
                break
            while len(messages) > 0:
                if running == False:
                    ws.close()
                    break
                msg = messages.pop(0)
                print(">S>",msg[0:10])
                ws.send(msg)
    thread.start_new_thread(run, ())



#Basic server for receiving data from webclient
class basicServer(WebSocket):
    def handle(self):
        global messages
        messages.append(self.data)


    def connected(self):
        global running, clients
        print("<C>", self.address)
        returnMessages.clear()
        messages.clear()
        clients.append(self)
        if running == False:
            running = True
            ws.close()
            x = threading.Thread(target=ws.run_forever)
            x.start()

    def handle_close(self):
        global running, returnMessages, clients, count, messages, compress_obj
        print("<D>", self.address)
        running = False
        returnMessages.clear()
        messages.clear()
        clients.clear()
        compress_obj = zlib.compressobj()
        count = 0


#boot up
websocket.enableTrace(False)
ws = websocket.WebSocketApp("wss://gateway.discord.gg/?encoding=json&v=9", #&compress=zlib-stream
                              on_open = on_open,
                              on_message = on_message,
                              on_close = on_close)

server = WebSocketServer('', 80, basicServer)

z = threading.Thread(target=server.serve_forever)
z.start()

w = threading.Thread(target=messageWatchdog)
w.start()



startTime = time.time()
doneOnce = False

def setTimestamp():
    global messageToInject
    messageToInject = json.loads(messageToInject)
    messageToInject['d']['id'] = str(get_snowflake())
    messageToInject['d']['timestamp'] = str(datetime.datetime.now().isoformat())
    messageToInject = json.dumps(messageToInject)

#while True:
#    if startTime + 20 < time.time() and not doneOnce:
#        print("<I<",messageToInject[0:10])
#        setTimestamp()
#        returnMessages.append(compressData(messageToInject))
#        time.sleep(120)
#        setTimestamp()
#        returnMessages.append(compressData(messageToInject))
#        doneOnce = True
