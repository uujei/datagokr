import abc
import logging
import os
from datetime import datetime
from typing import List, Optional
from urllib.parse import quote_plus, unquote, urlencode

import pendulum
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field, HttpUrl, SecretStr, ValidationError

# logging
logger = logging.getLogger(__file__)

# timezone
KST = pendulum.timezone("Asia/Seoul")


################################################################################
# Mother Class
################################################################################
class DataGoKr(BaseModel, abc.ABC):
    """
    (NOTE)
     - numOfRows: 데이터 요청은 1,000건을 넘을 수 없음. (MAX 999)
     - pageNo: 디버그 시에만 사용.
    """

    __timezone__: KST
    __RecordModel__: BaseModel = None
    __index_names__: list = None
    __key_name__: str = None
    __value_name__: str = None

    baseUrl: HttpUrl
    route: str
    serviceKey: SecretStr
    numOfRows: Optional[int] = 999
    pageNo: Optional[int]

    class Config:
        use_enum_values = True

    def request(self, pageNo=None):
        if pageNo is not None:
            self.pageNo = pageNo

        # request and receive response
        endpoint = self.get_endpoint()
        response = self._request(endpoint=endpoint)
        if response["header"]["resultCode"] != "00":
            _msg = f"CODE[{response['header']['resultCode']}]: {response['header']['resultMsg']}"
            raise ReferenceError(_msg)

        # extract records from body
        body = response["body"]
        records = body["items"]
        if not isinstance(records, list):
            records = records["item"]

        # repeat request, extract, and append records until the last page
        if pageNo is None:
            self.pageNo = 1
            while body["totalCount"] >= body["numOfRows"]:
                self.pageNo = body["pageNo"] + 1
                endpoint = self.get_endpoint()
                response = self._request(endpoint=endpoint)
                # result code '03' means 'No data'
                if response["header"]["resultCode"] == "03":
                    break
                if response["header"]["resultCode"] != "00":
                    _msg = f"CODE[{response['header']['resultCode']}]: {response['header']['resultMsg']}"
                    raise ReferenceError(_msg)
                body = response["body"]
                records += body["items"]["item"]
        return records

    def get_endpoint(self):
        url = os.path.join(self.baseUrl, self.route)
        query = urlencode(
            {quote_plus(k): v for k, v in self.__dict__.items() if k not in ["baseUrl", "route"] and v is not None}
        )
        return "?".join([url, query])

    def check_query(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def get_records(self, sep="___"):
        items = self.request()
        items = list(map(self._drop_empty_fields, items))
        if self.__key_name__ is None or self.__value_name__ is None:
            return [self.__RecordModel__(**item) for item in items]

        records = self._items_to_records(
            Model=self.__RecordModel__,
            items=items,
            index_names=self.__index_names__,
            key_name=self.__key_name__,
            value_name=self.__value_name__,
            sep=sep,
        )

        if self.__RecordModel__ is None:
            return records

        return [self.__RecordModel__(**record) for record in records]

    @staticmethod
    def _request(endpoint):
        response = requests.get(endpoint)
        if response.text.startswith("<"):
            _msg = f"[COMMON ERROR] XML is returned - {response.text}"
            raise ReferenceError(_msg)
        response = response.json()["response"]
        return response

    @staticmethod
    def _items_to_records(Model, items, key_name, value_name, index_names, sep):
        if index_names is None:
            record = dict()
            for item in items:
                record.update({item.pop(key_name): item.pop(value_name)})
                record.update(item)
            return [record]

        records = dict()
        for item in items:
            flat_indices = sep.join([item.pop(idx) for idx in index_names])
            if flat_indices not in records.keys():
                records[flat_indices] = dict()
            records[flat_indices].update({item.pop(key_name): item.pop(value_name)})
            records[flat_indices].update(item)

        return [
            {**{k: v for k, v in zip(index_names, flat_indices.split(sep))}, **record}
            for flat_indices, record in records.items()
        ]

    @staticmethod
    def _drop_empty_fields(item: dict):
        return {k: v for k, v in item.items() if v != ""}

    @staticmethod
    def _ensure_list(x):
        if x is None or isinstance(x, list):
            return x
        return [x]
