from typing import Callable, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BaseMT5Sink:
  """Base class for MT5 event sinks"""
  def __init__(self):
    self._callbacks: Dict[str, list[Callable]] = {}
  
  def add_callback(self, event: str, callback: Callable):
    """Add callback for specific event"""
    if event not in self._callbacks:
      self._callbacks[event] = []
    self._callbacks[event].append(callback)
  
  def _trigger_callbacks(self, event: str, data: Any):
    """Trigger all callbacks for an event"""
    for callback in self._callbacks.get(event, []):
      try:
        callback(data)
      except Exception as e:
        logger.error(f"Error in {event} callback: {str(e)}")

class MT5UserSink(BaseMT5Sink):
  """Sink for user-related events"""
  def OnUserDelete(self, user) -> None:
    self._trigger_callbacks('user_delete', user)
      
  def OnUserUpdate(self, user) -> None:
    self._trigger_callbacks('user_update', user)

class MT5DealSink(BaseMT5Sink):
  """Sink for deal-related events"""
  def OnDealAdd(self, deal) -> None:
    self._trigger_callbacks('deal_add', deal) 