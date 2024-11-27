from typing import Dict, List, Optional, Callable
from .connection.manager import MT5ConnectionManager
from .constants import MT5ServerConfig, MT5_SERVERS
from .exceptions import MT5ConnectionError
from .sinks import MT5UserSink, MT5DealSink
class MT5ConnectionPools:
  _instance = None
  
  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(MT5ConnectionPools, cls).__new__(cls)
      cls._instance._initialized = False
    return cls._instance
  
  def __init__(self):
    print("DEBUG: MT5ConnectionPools.__init__ called")  # Debug print
    if self._initialized:
      return
        
    self._demo_pool = None
    self._live_pool = None
    self._initialized = True
    self._user_sink = MT5UserSink()
    self._deal_sink = MT5DealSink()
    print("DEBUG: MT5ConnectionPools initialized")  # Debug print
    
    # Connect to all servers during initialization
    # try:
    #   connection_results = self.connect_all()
    #   print("MT5 Connection Results:", connection_results)
    #   self.setup_sinks()
    #   print("MT5 sinks setup")
    #   self.add_deal_callback('deal_add', on_deal_add)
    # except Exception as e:
    #   print(f"Failed to connect to MT5 servers: {str(e)}")
  
  def setup_sinks(self):
    """Setup sinks for all connections"""
    if self._demo_pool:
      self._demo_pool.setup_user_sink(self._user_sink)
      self._demo_pool.setup_deal_sink(self._deal_sink)
    if self._live_pool:
      self._live_pool.setup_user_sink(self._user_sink)
      self._live_pool.setup_deal_sink(self._deal_sink)
  
  def add_user_callback(self, event: str, callback: Callable):
    """Add callback for user events"""
    self._user_sink.add_callback(event, callback)
  
  def add_deal_callback(self, event: str, callback: Callable):
    """Add callback for deal events"""
    print(f"Adding deal callback for {event}")
    self._deal_sink.add_callback(event, callback)
  
  @property
  def demo(self) -> MT5ConnectionManager:
    """Get demo server connection"""
    if not self._demo_pool:
      config = next((server for server in MT5_SERVERS if server.type == 'demo'), None)
      if not config:
        raise MT5ConnectionError("No demo server configuration found")
      self._demo_pool = MT5ConnectionManager(config)
    return self._demo_pool
  
  @property
  def live(self) -> MT5ConnectionManager:
    """Get live server connection"""
    if not self._live_pool:
      config = next((server for server in MT5_SERVERS if server.type == 'live'), None)
      if not config:
        raise MT5ConnectionError("No live server configuration found")
      self._live_pool = MT5ConnectionManager(config)
    return self._live_pool
  
  def get_by_type(self, server_type: str) -> MT5ConnectionManager:
    """Get connection by server type"""
    if server_type == 'demo':
      return self.demo
    elif server_type == 'live':
      return self.live
    raise ValueError(f"Invalid server type: {server_type}")
  
  def get_by_id(self, server_id: int) -> MT5ConnectionManager:
    """Get connection by server ID"""
    config = next((server for server in MT5_SERVERS if server.id == server_id), None)
    if not config:
      raise ValueError(f"No server found with ID: {server_id}")
    
    if config.type == 'demo':
      return self.demo
    return self.live
  
  def connect_all(self) -> Dict[str, bool]:
    """Connect to all servers"""
    results = {}
    for server in MT5_SERVERS:
      try:
        connection = self.get_by_type(server.type)
        connection.connect()
        results[server.name] = True
      except Exception as e:
        results[server.name] = False
    return results
  
  def disconnect_all(self):
    """Disconnect from all servers"""
    if self._demo_pool:
      self._demo_pool.disconnect()
    if self._live_pool:
      self._live_pool.disconnect() 

# Global instance
mt5_pools = MT5ConnectionPools() 