# api-python-client

```python
from forbin.client import Client

client = Client(username='username', password='password')
challenge = client.challenges()
print(challenge)
```