# Client

The client object is the main interface to the API. You can use it to access all API endpoints.

```python
from wordcab import Client

client = Client()
stats = client.get_stats()

# Run with a context manager
with Client() as client:
   stats = client.get_stats()

# Run with a context manager and a custom API key
with Client(api_key="my_api_key") as client:
   stats = client.get_stats()
```

```{eval-rst}
.. autoclass:: wordcab.Client
   :members:
```
