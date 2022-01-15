import json

import click

from .airkorea import MsrstnAcctoRltmMesureDnsty
from .kma import UltraSrtFcst, UltraSrtNcst, VilageFcst, WthrDataList


def _out(records):
    for record in records:
        print(record.dict())


@click.group()
def datagokr():
    pass


@datagokr.command()
@click.option("-s", "--service-key", default=None, help="API Key")
@click.option("-d", "--base-date", default=None, help="baseDate")
@click.option("-t", "--base-time", default=None, help="baseTime")
@click.option("-x", "--nx", default=None, help="nx")
@click.option("-y", "--ny", default=None, help="ny")
def ultra_srt_ncst(service_key, base_date, base_time, nx, ny):
    params = {
        "serviceKey": service_key,
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }
    api = UltraSrtNcst(**{k: v for k, v in params.items() if v is not None})
    records = api.get_records()
    _out(records)


@datagokr.command()
@click.option("-s", "--service-key", default=None, help="API Key")
@click.option("-d", "--base-date", default=None, help="baseDate")
@click.option("-t", "--base-time", default=None, help="baseTime")
@click.option("-x", "--nx", default=None, help="nx")
@click.option("-y", "--ny", default=None, help="ny")
def ultra_srt_fcst(service_key, base_date, base_time, nx, ny):
    params = {
        "serviceKey": service_key,
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }
    api = UltraSrtFcst(**{k: v for k, v in params.items() if v is not None})
    records = api.get_records()
    _out(records)


@datagokr.command()
@click.option("-s", "--service-key", default=None, help="API Key")
@click.option("-d", "--base-date", default=None, help="baseDate")
@click.option("-t", "--base-time", default=None, help="baseTime")
@click.option("-x", "--nx", default=None, help="nx")
@click.option("-y", "--ny", default=None, help="ny")
def vilage_fcst(service_key, base_date, base_time, nx, ny):
    params = {
        "serviceKey": service_key,
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }
    api = VilageFcst(**{k: v for k, v in params.items() if v is not None})
    records = api.get_records()
    _out(records)
