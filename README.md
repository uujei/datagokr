# DataGoKr

#### 설치하기

```bash
pip install datagokr
```



#### 사용하기

```python
# 동네예보 서비스 사용 예
import datagokr.kma import VilageFcst

# 파라미터는 data.go.kr API 문서와 동일 (secretKey, base_data, ...)
api = VilageFcst(secretKey="<my_api_key>", base_date="20220110", base_time="0500")

# API 호출하여 값 얻기
records = api.get_records()

# (DEBUG 목적) endpoint 확인 (출력된 주소 복사하여 브라우저에서 접근)
api.get_endpoint()
```



#### pydantic

datagokr 패키지는 schema validation을 위해 pydantic model을 사용합니다. get_records() 메소드는 pydantic 모델을 따르는 record들의 list로 반환됩니다. 이를 dictionary, DataFrame으로 변환하는 방법은 다음과 같습니다.

```python
records = api.get_records()

# list of pydantic model records을 dictionary of dictionary로 변환
list_of_dict = [r.dict() for r in records]

# list of dictionary records를 Pandas DataFrame으로 변환
df = pd.DataFrame.from_records(list_of_dict)
```



#### 현재 사용 가능한 API 목록

**기상청**

```python
# 기상청 (KMA)
from datagokr.kma import UltraSrtNcst, UltraSrtFcst, VilageFcst, WthrDataList

# (1) 기상청 동네예보 초단기실황
api = UltraSrtNcst(secretKey=<required>, base_date=<req.>, base_time=<req.>, nx=<req.>, ny=<req.>)
api.get_records()

# (2) 기상청 동네예보 초단기예보
api = UltraSrtFcst(secretKey=<req.>, base_date=<req.>, base_time=<req.>, nx=<req.>, ny=<req.>)
api.get_records()

# (3) 기상청 동네예보 단기예보
api = VilageFcst(secretKey=<req.>, base_date=<req.>, base_time=<req.>, nx=<req.>, ny=<req.>)
api.get_records()

# (4) 지상종관 기상자료 (시간대별)
api = WthrDataList(secretKey=<req.>, dataCd=<req.>, dateCd=<req.>, startDt=<req.> endDt=<req.>, startHh=<req.>, endHh=<req.>)
api.get_records()
```



**환경공단 (에어코리아)**

```python
# 에어코리아
from datagokr.airkorea import MsrstnAcctoRltmMesureDnsty, UnityAirEnvrnIdexSnstiveAboveMsrstnList, CtprvnRltmMesureDnsty, MinuDustFrcstDspth

# (1) 측정소별 실시간 측정정보 조회
api = MsrstnAcctoRltmMesureDnsty(secretKey=<req.>, stationName=<req.>, dataTerm=<req.>, ver=<req.>)
api.get_records()

# (2) 통합대기환경지수 나쁨 이상 측정소 목록조회
api = UnityAirEnvrnIdexSnstiveAboveMsrstnList(secretKey=<req.>)
api.get_records()

# (3) 시도별 실시간 측정정보 조회 상세기능명세
api = CtprvnRltmMesureDnsty(secretKey=<req.>, sidoName=<req.>, ver=<req.>)
api.get_records()

# (4) 대기질 예보통보 조회
api = MinuDustFrcstDspth(secretKey=<req.>)
api.get_records()
```

