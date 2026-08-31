# Sentinel catalogue cache

After login, Resources will reveal `<host>`. Then:

```
curl -s http://<host>/api/ingest -o catalogue.last.json
```

Keep `catalogue.last.json` out of git if it contains internal hostnames. The schema file is the working hypothesis from the public integrator guide (id, location, codec, live, stream properties, three URLs). When the real payload arrives, diff it against the schema, patch `app/services/catalogue.py`, and do not assume the URL pattern ` /stream/<id>` is stable.
