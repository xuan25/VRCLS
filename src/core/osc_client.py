from typing import Any, Optional
from pythonosc import udp_client
from .logger import MyLogger

class OSCClient:
    """OSC 客户端基础类"""
    def __init__(self,logger, host: str = "127.0.0.1", port: int = 9000):
        self.client = udp_client.SimpleUDPClient(host, port)
        self.logger = logger

    def sendOSCMesssage(self, address: str, value: Any) -> None:
        """发送 OSC 消息
        
        Args:
            address: OSC 地址
            value: 要发送的值
        """
        self.logger.debug(f"Sending OSC message to {address}: {value}")
        self.client.send_message(address, value) 