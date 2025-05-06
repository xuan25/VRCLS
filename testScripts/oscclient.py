from pythonosc import udp_client
import time
client=udp_client.SimpleUDPClient('127.0.0.1',9003)
count=0
while True:
    client.send_message("/chatbox/input", [ str(count), True, False]) 
    print(count)
    count+=1
    time.sleep(2)