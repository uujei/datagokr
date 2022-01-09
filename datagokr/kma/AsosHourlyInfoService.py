import logging
import os
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, SecretStr, ValidationError

from ..DataGoKr import DataGoKr

# logging
logger = logging.getLogger(__file__)

# debug only
KMA_API_KEY = os.getenv("KMA_API_KEY")


################################################################################
# Types
################################################################################
class DataType(str, Enum):
    # Only JSON Available yet
    json = "JSON"


################################################################################
# [Abstract API] 지상(종관,ASOS)
################################################################################
# ABSTRACT
class AsosHourlyInfo(DataGoKr):
    __version__ = "2.0"

    baseUrl: HttpUrl = "http://apis.data.go.kr/1360000/AsosHourlyInfoService"
    dataType: Optional[DataType] = "JSON"  # Only JSON available yet.
    serviceKey: str = KMA_API_KEY


################################################################################
# [API] 지상(종관,ASOS) 시간자료 조회
################################################################################
# Output Model
class WthrDataListModel(BaseModel):
    tm: str  # 시간
    rnum: int  # 목록순서
    stnId: int  # 지점번호
    stnNm: str  # 지점이름
    ta: Optional[float]  # 기온
    taQcflg: Optional[int]  # 기온품질검사플래그 (null: 정상, 1: 오류, 9: 결측)
    rn: Optional[float]  # 강수량
    rnQcflg: Optional[int]
    ws: Optional[float]  # 풍속
    wsQcflg: Optional[int]
    wd: Optional[str]  # 풍향 (20: 북북동, 40: 북동, ..., 360: 정북, 00: CALM, 99: 변화많음)
    wdQcflg: Optional[int]
    hm: Optional[int]  # 상대습도
    hmQcflg: Optional[int]
    pv: Optional[float]  # 증기압
    td: Optional[float]  # 이슬점온도
    pa: Optional[float]  # 현지기압
    paQcflg: Optional[int]
    ps: Optional[float]  # 해면기압
    psQcflg: Optional[int]
    ss: Optional[float]  # 일조시간
    ssQcflg: Optional[int]
    icsr: Optional[float]  # 일사량
    dsnw: Optional[float]  # 적설량
    hr3Fhsc: Optional[float]  # 3시간신적설
    dc10Tca: Optional[int]  # 전운량
    dc10LmcsCa: Optional[int]  # 중하층운량
    clfmAbbrCd: Optional[str]  # 운형
    lcsCh: Optional[int]  # 최저운고
    vs: Optional[int]  # 시정
    # gndSttCd: Optional[int]   # 2016.7.1 종료
    dmstMtphNo: Optional[str]  # 현상번호
    ts: Optional[float]  # 지면온도
    tsQcflg: Optional[int]
    m005Te: Optional[float]  # 5cm 지중온도
    m01Te: Optional[float]  # 10cm 지중온도
    m02Te: Optional[float]  # 20cm 지중온도
    m03Te: Optional[float]  # 30cm 지중온도


# API
class WthrDataList(AsosHourlyInfo):
    __RecordModel__ = WthrDataListModel
    __index_names__ = None
    __key_name__ = None
    __value_name__ = None

    route: str = "getWthrDataList"
    dataCd: str = "ASOS"
    dateCd: str = "HR"
    startDt: str = (datetime.now() - timedelta(days=2)).strftime("%Y%m%d")
    startHh: str = (datetime.now() - timedelta(days=2)).strftime("%H")
    endDt: str = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    endHh: str = (datetime.now() - timedelta(days=1)).strftime("%H")
    stnIds: int = 119  # 이동읍 최근접 - 수원 수도권기상청
