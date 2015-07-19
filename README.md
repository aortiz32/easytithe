Python interface for [EasyTithe Manager](https://www.easytithe.com/cp/default.asp)
========================================

Easy Tithe is an online giving platform for churches and organizations that
makes accepting, tracking and reporting online tithing and donations, well...
easy.

The Easy Tithe Manager includes a range of reports, which can be viewed by
person, transaction, fund and date ranges. Access to the Easy Tithe Manager
is done through the Easy Tithe website at
https://www.easytithe.com/cp/default.asp.

This Easy Tithe Python library provides an API for logging into the Easy Tithe
Manager and accessing contribution data.

```python
Usage:
  import easytithe

  et = easytithe.EasyTithe('username', 'passsword')
  contributions = et.GetContributions(
    start_date='10/6/2013',
    end_date='10/13/2013')
  print contributions
```
