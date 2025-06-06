from time import sleep
from typing import List
from .base_handler import BaseHandler
import uuid
from..module.bitLedColor import find_nearest_foreground
import random
def half_to_full(half_str):
    full_str = ''
    for char in half_str:
        if ord(char) >= 33 and ord(char) <= 126:  # 半角字符的ASCII码范围是33-126
            full_char = chr(ord(char) + 0xFEE0)  # 将半角转换为全角
            full_str += full_char
        else:
            full_str += char  # 非ASCII字符或已经是全角的字符直接添加
    return full_str



class VRCBitmapLedHandler(BaseHandler):
    def __init__(self,logger, osc_client,params):
        super().__init__(osc_client)
        self.logger=logger
        self.params=params
    """聊天框处理器"""
        
    def handle(self, message: str,params):
        self.controlFunction(message,params,self.params["config"].get("VRCBitmapLed_row"),self.params["config"].get("VRCBitmapLed_col"))
    def string_to_unicode_bytes(self,s) -> List[int]:
        bytes_array = []
        for char in s:
            bytes_array.extend(char.encode('utf-16-be'))
        return bytes_array
    def format_to_box_autowrap(self,s,row=8,col=16):
        lines = s.split('\n')
        result = []
        for line in lines:
            if len(result) >= row:
                break  # 已满8行则停止处理
            start = 0
            while start < len(line) and len(result) < row:
                # 每次取16字符并补空格
                chunk = line[start:start+col].ljust(col)
                result.append(chunk)
                start += col
        
        # 补足8行
        while len(result) < row:
            result.append(' ' * col)
        
        # 合并结果
        return ''.join(result[:row])  # 确保不超过8行

    def controlFunction(self,res,params,row=8,col=16):
        uid=str(uuid.uuid1())
        if len(params["VRCBitmapLed_taskList"])!=0:
            if params["VRCBitmapLed_taskList"][-1]=="clear":params["VRCBitmapLed_taskList"][-1]=uid
            else:params["VRCBitmapLed_taskList"].append(uid)
        else:params["VRCBitmapLed_taskList"].append(uid)
        if self.params["config"].get("VRCBitmapLed_COLOR")==True: rgb=find_nearest_foreground(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        text=res['text']
        text = half_to_full(text)
        lines=self.format_to_box_autowrap(text,row,col)

        data = self.string_to_unicode_bytes(lines)
        for i in range(row*col*2 - len(data)):
            data.append(0)
        
        for index in range(row*col):
            while params["VRCBitmapLed_taskList"][0]!=uid:sleep(0.1)
            if  params["VRCBitmapLed_Line_old"][index]!=lines[index] or lines[index]=='':

                # 发送BitmapLed/Pointer
                self.osc_client.send_message("/avatar/parameters/BitmapLed/Pointer", index)

                high_index = index * 2
                low_index = index * 2 + 1

                # 发送BitmapLed/Data
                
                if self.params["config"].get("VRCBitmapLed_COLOR")==True:self.osc_client.send_message("/avatar/parameters/BitmapLed/DataX24", rgb)
                self.osc_client.send_message("/avatar/parameters/BitmapLed/DataX16", data[high_index])
                self.osc_client.send_message("/avatar/parameters/BitmapLed/Data", data[low_index])
                if lines[index]=='。'or  lines[index]==' ':rgb=find_nearest_foreground(random.randint(0,255),random.randint(0,255),random.randint(0,255))
                # char = text[index] if len(text) > index else ""
                # print(f"\r{index}: {data[index]}, {char}", end="")
                # self.logger.put({'text':f"{index * 2}: {data[high_index]}, {data[low_index]}, {char}",'level':'debug'})
                sleep(0.2)
        params["VRCBitmapLed_Line_old"]=lines
        params["VRCBitmapLed_taskList"].pop(0)
