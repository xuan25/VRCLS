from abc import ABC, abstractmethod
from pythonosc import udp_client

class BaseHandler(ABC):
    """处理器基类"""
    def __init__(self, osc_client:  udp_client.SimpleUDPClient):
        self.osc_client = osc_client

    @abstractmethod
    def handle(self, *args, **kwargs):
        """处理方法
        
        Args:
            *args: 位置参数
            **kwargs: 关键字参数
        """
        pass 