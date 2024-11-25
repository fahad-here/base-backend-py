from typing import List, NamedTuple

class MT5ServerConfig(NamedTuple):
  name: str
  ips: List[str]
  username: int
  manager_password: str
  api_password: str
  type: str
  id: int

MT5_SERVERS = [
  MT5ServerConfig(
    name='MT5 MAIN DEMO',
    ips=['104.46.38.179'],
    username=1111,
    manager_password='B@Fe4rQa',
    api_password='P-2lEhNy',
    type='demo',
    id=1
  ),
  MT5ServerConfig(
    name='MT5 MAIN LIVE',
    ips=['104.46.38.179'],
    username=1111,
    manager_password='B@Fe4rQa',
    api_password='P-2lEhNy',
    type='live',
    id=2
  ),
]