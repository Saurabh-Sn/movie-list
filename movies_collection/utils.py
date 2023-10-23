from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[502, 503, 504, 400]
    
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http_adapter = requests.Session()
http_adapter.mount("https://", adapter)
http_adapter.mount("http://", adapter)
