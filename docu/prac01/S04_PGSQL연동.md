# 실습1. FastAPI Start

- S01. [개발환경셋팅    ](./S01_개발환경셋팅.md) 
- S02. [컨트롤러확장    ](./S02_컨트롤러확장.md)
- S03. [PGSQL준비      ](./S03_PGSQL준비.md)
- S04. <b> PGSQL연동   </b>
---

### S04_PGSQL연동 : python으로 DB 핸들링
> - config     : DB접속을 위한 환경변수 셋팅
> - controller : 비즈니스 로직 처리, 웹페이지 경로 설정
> - model      : DB와 연동시 주고받는 데이터모델
---


### 실습1-4 
---
- 코드작성 

> [config/config.py]
```python
# config/config.py

PGSQL_TEST_DATABASE_STRING = "host=127.0.0.1 dbname=test_db user=test_user password=test1234 port=5432"
PGSQL_TEST_POOL_MIN_SIZE = 10
PGSQL_TEST_POOL_MAX_SIZE = 20
PGSQL_TEST_POOL_MAX_IDLE = 60

```

> [controller/admins.py]
```python
# controller/admins.py

from fastapi import APIRouter
from model import pgsql_test

router = APIRouter(
    prefix="/admins",
    tags=["admins"],
    responses={404: {"description": "Not found"}},
)

@router.get("/list")
def list_admin():
    """
    List all admins from the database.
    """
    results = pgsql_test.list_admin()
    # return {"user_id": user_id}
    return results

```


> [model/pgsql_test.py]
```python
# model/pgsql_test.py

import psycopg
import psycopg_pool
from config import config

pool_default = psycopg_pool.ConnectionPool(
    config.PGSQL_TEST_DATABASE_STRING,
    min_size=config.PGSQL_TEST_POOL_MIN_SIZE,
    max_size=config.PGSQL_TEST_POOL_MAX_SIZE,
    max_idle=config.PGSQL_TEST_POOL_MAX_IDLE
)

def list_admin():
    with pool_default.connection() as conn:
        cur = conn.cursor(row_factory=psycopg.rows.dict_row)

        try:
            results = cur.execute("SELECT * FROM tb_admin").fetchall()
        except psycopg.OperationalError as err:
            print(f'Error executing query: {err}')
        except psycopg.ProgrammingError as err:
            print('Database error via psycopg. %s, err')
            resutl  = False
        except psycopg.IntegrityError as err:
            print('PostgreSQL integrity error via psycopg. %s, err')
            result = False
            
    return results


```

- 패키지 설치
```
(.venv) PS C:\GitHub\D2502_FastAPI\code\prac01> pip install "psycopg[binary,pool]"
Collecting psycopg[binary,pool]
...............
...............
Successfully installed psycopg-3.2.6 psycopg-pool-3.2.6

[notice] A new release of pip is available: 24.2 -> 25.0.1
[notice] To update, run: python.exe -m pip install --upgrade pip


```


> [pgsql_test.py]
```python
# pgsql_main.py

from fastapi import FastAPI
from controller import items, users, admins

app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)
app.include_router(admins.router)

@app.get("/")
def read_root():
    return {"Hello": "FastAPI"}

@app.get("/list")
def list_admin():
    """
    List all admins from the database.
    """
    results = admins.list_admin()
    return results


```


- 실행 : uvicorn.exe pgsql_main:app --reload
```
(.venv) PS C:\GitHub\D2502_FastAPI\code\prac01> uvicorn.exe pgsql_main:app --reload
INFO:     Will watch for changes in these directories: ['C:\\GitHub\\D2502_FastAPI\\code\\prac01']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [20612] using StatReload
INFO:     Started server process [29532]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

```


- 실행결과 : 
> http://localhost:8000/list
```
[
    {
        admin_no: 1,
        login_id: "hong_gd",
        passwd: "hong123",
        nick: "홍길동",
        email: "hong@gmail.com"
    },
    {
        admin_no: 2,
        login_id: "jang_nr",
        passwd: "jang123",
        nick: "장나라",
        email: "jang@gmail.com"
    }
]

```


### 실습1-5. 프로시저로 호출출 
---
- 코드작성 
> [model/pgsql_test.py]
```python
# model/pgsql_test.py

import psycopg
import psycopg_pool
from config import config

pool_default = psycopg_pool.ConnectionPool(
    config.PGSQL_TEST_DATABASE_STRING,
    min_size=config.PGSQL_TEST_POOL_MIN_SIZE,
    max_size=config.PGSQL_TEST_POOL_MAX_SIZE,
    max_idle=config.PGSQL_TEST_POOL_MAX_IDLE
)

# def list_admin():
#     with pool_default.connection() as conn:
#         cur = conn.cursor(row_factory=psycopg.rows.dict_row)

#         try:
#             results = cur.execute("SELECT * FROM tb_admin").fetchall()
#         except psycopg.OperationalError as err:
#             print(f'Error executing query: {err}')
#         except psycopg.ProgrammingError as err:
#             print('Database error via psycopg. %s, err')
#             resutl  = False
#         except psycopg.IntegrityError as err:
#             print('PostgreSQL integrity error via psycopg. %s, err')
#             result = False
            
#     return results

def list_admin():
    with pool_default.connection() as conn:
        cur = conn.cursor(row_factory=psycopg.rows.dict_row)

        try:
            cur.execute("CALL SP_L_ADMIN('out1')")
            results = cur.execute("FETCJH ALL FROM out1").fetchall()
            con.commit()
        except psycopg.OperationalError as err:
            print(f'Error executing query: {err}')
        except psycopg.ProgrammingError as err:
            print('Database error via psycopg. %s, err')
            resutl  = False
        except psycopg.IntegrityError as err:
            print('PostgreSQL integrity error via psycopg. %s, err')
            result = False
            
    return results

```

- 실행결과 : 
> http://localhost:8000/list
```
[
    {
        admin_no: 1,
        login_id: "hong_gd",
        passwd: "hong123",
        nick: "홍길동",
        email: "hong@gmail.com"
    },
    {
        admin_no: 2,
        login_id: "jang_nr",
        passwd: "jang123",
        nick: "장나라",
        email: "jang@gmail.com"
    }
]

```
