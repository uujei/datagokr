import logging
import os
from datetime import datetime
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
# (Type)
class DataType(str, Enum):
    # Only JSON Available yet
    json = "JSON"


# (Type)
class VilageFcstVersionFtype(str, Enum):
    ODAM = "ODAM"
    VSRT = "VSRT"
    SHRT = "SHRT"


################################################################################
# [Abstract] Abstract for VilageFcst
################################################################################
class VilageFcstInfo(DataGoKr):
    __version__ = "2.0"

    baseUrl: HttpUrl = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"
    dataType: Optional[DataType] = "JSON"  # Only JSON available yet.
    serviceKey: str = KMA_API_KEY


################################################################################
# [API] 초단기 실황  UltraSrtNcst
################################################################################
# Output Model
class UltraSrtNcstModel(BaseModel):
    baseDate: str
    baseTime: str
    T1H: Optional[float]  # 10 decimal
    RN1: Optional[str]  # 8 code
    UUU: Optional[float]  # 12 float
    VVV: Optional[float]  # 12 float
    REH: Optional[int]  # 8 int
    PTY: Optional[int]  # 4 code
    VEC: Optional[float]  # 10 decimal
    WSD: Optional[float]  # 10 decimal


# API
class UltraSrtNcst(VilageFcstInfo):
    __RecordModel__ = UltraSrtNcstModel
    __index_names__ = None
    __key_name__ = "category"
    __value_name__ = "obsrValue"

    route: str = "getUltraSrtNcst"
    base_date: str = datetime.now().strftime("%Y%m%d")
    base_time: str = "0500"
    nx: int = 64
    ny: int = 118


################################################################################
# [API] 초단기 예보 UltraSrtFcst
################################################################################
# Output Model
class UltraSrtFcstModel(BaseModel):
    baseDate: str
    baseTime: str
    fcstDate: str
    fcstTime: str
    T1H: Optional[float]  # 10 decimal
    RN1: Optional[str]  # 8 code
    SKY: Optional[int]  # 4 code
    UUU: Optional[float]  # 12 float
    VVV: Optional[float]  # 12 float
    REH: Optional[int]  # 8 int
    PTY: Optional[int]  # 4 code
    LGT: Optional[str]  # 4 code
    VEC: Optional[float]  # 10 decimal
    WSD: Optional[float]  # 10 decimal


# API
class UltraSrtFcst(VilageFcstInfo):
    __RecordModel__ = UltraSrtFcstModel
    __index_names__ = ["fcstDate", "fcstTime"]
    __key_name__ = "category"
    __value_name__ = "fcstValue"

    route: str = "getUltraSrtFcst"
    base_date: str = datetime.now().strftime("%Y%m%d")
    base_time: str = "0500"
    nx: int = 64
    ny: int = 118


################################################################################
# [API] 단기 예보 VilageFcst
################################################################################
# Output Model
class VilageFcstModel(BaseModel):
    baseDate: str
    baseTime: str
    fcstDate: str
    fcstTime: str
    POP: Optional[int]  # 8 int
    PTY: Optional[int]  # 4 code
    PCP: Optional[str]  # 8 code
    REH: Optional[int]  # 8 int
    SNO: Optional[str]  # 8 code
    SKY: Optional[int]  # 4 code
    TMP: Optional[float]  # 10 decimal
    TMN: Optional[float]  # 10 decimal
    TMX: Optional[float]  # 10 decimal
    UUU: Optional[float]  # 12 float
    VVV: Optional[float]  # 12 float
    WAV: Optional[float]  # 8 int
    VEC: Optional[float]  # 10 decimal
    WSD: Optional[float]  # 10 decimal


# API
class VilageFcst(VilageFcstInfo):
    __RecordModel__ = VilageFcstModel
    __index_names__ = ["fcstDate", "fcstTime"]
    __key_name__ = "category"
    __value_name__ = "fcstValue"

    route: str = "getVilageFcst"
    base_date: str = datetime.now().strftime("%Y%m%d")
    base_time: str = "0500"
    nx: int = 64
    ny: int = 118


################################################################################
# [API] 단기예보 수치모델 버전
################################################################################
# Output Model
class VilageFcstVersion(BaseModel):
    filetype: VilageFcstVersionFtype
    version: str


# API
class VilageFcstVersion(VilageFcstInfo):
    __RecordModel__ = VilageFcstVersion
    route: str = "getFcstVersion"
    ftype: VilageFcstVersionFtype = "ODAM"
    basedatetime: str = datetime.now().strftime("%Y%m%d0800")
