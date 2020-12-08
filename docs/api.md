# API
This project can be used as an api for speedtest.net and fast.com.

## Example for speedtest:
```python
from gui_speedtest_fastcom import speedtest

s = speedtest.SpeedTestObject()
s.get_best()
s.download()
s.upload()
```

#Example for fast:
```python
from gui_speedtest_fastcom import fastcom

f = fastcom.FastCom()
f.download()
f.get_token()
```
