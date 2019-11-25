from __future__ import absolute_import
from Qshop.celery import app


@app.task
def Test():
    print("hello")

from sdk.sendDD import senddingding
@app.task
def sendDingDing(params):
    senddingding(params)

