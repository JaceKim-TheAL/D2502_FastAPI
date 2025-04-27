# 실습1. FastAPI Start

- S01. [개발환경셋팅    ](./S01_개발환경셋팅.md) 
- S02. [컨트롤러확장    ](./S02_컨트롤러확장.md)
- S03. <b> PGSQL준비   </b>
- S04. [PGSQL연동      ](./S04_PGSQL연동.md)

---

### S03_PGSQL준비 : 설치 및 구동
> - PostgreSQL DB 설치
> - PostgreSQL DB 구동
---

- Database는 `PostgreSQL` 을 사용
> 오픈 소스 객체-관계형 데이터베이스 관리 시스템(ORDBMS)
> 참조 : [PostgreSQL 설치 방법](https://github.com/JaceKim-TheAL/D2502_PostgreSQL)

- DB 구동 및 테스트사용자 등록
```
C:\>pg_ctl start 
.......
서버 시작됨

C:\>psql -U postgres
psql (17.4)
도움말을 보려면 "help"를 입력하십시오.

postgres=# 
postgres=# CREATE USER test_user WITH PASSWORD 'test1234';
CREATE ROLE

postgres=# \du
                           롤 목록
  롤 이름   |                      속성
------------+------------------------------------------------
 admin_user | 슈퍼유저
 postgres   | 슈퍼유저, 롤 만들기, DB 만들기, 복제, RLS 통과
 test_user  |

postgres=# \quit

C:\>psql -U test_user -d test_db
psql (17.4)

test_db=> 

```

- 테스트데이터 등록
```
test_db=> 
CREATE TABLE TB_ADMIN (
    ADMIN_NO Serial NOT NULL,
    LOGIN_ID Varchar(20) NOT NULL UNIQUE,
    PASSWD   Varchar(20) NOT NULL,
    NICK     Varchar(20) NOT NULL,
    EMAIL    Varchar(40),
    PRIMARY KEY (ADMIN_NO)
) Without Oids;
CREATE TABLE
test_db=>
test_db=> \d
                    릴레이션 목록
 스키마 |         이름          |  형태  |  소유주
--------+-----------------------+--------+-----------
 public | tb_admin              | 테이블 | test_user
 public | tb_admin_admin_no_seq | 시퀀스 | test_user
(2개 행)

test_db=> \d tb_admin
                                      "public.tb_admin" 테이블
  필드명  |         형태          | 정렬규칙 | NULL허용 |                   초기값
----------+-----------------------+----------+----------+--------------------------------------------
 admin_no | integer               |          | not null | nextval('tb_admin_admin_no_seq'::regclass)
 login_id | character varying(20) |          | not null |
 passwd   | character varying(20) |          | not null |
 nick     | character varying(20) |          | not null |
 email    | character varying(40) |          |          |
인덱스들:
    "tb_admin_pkey" PRIMARY KEY, btree (admin_no)
    "tb_admin_login_id_key" UNIQUE CONSTRAINT, btree (login_id)

test_db=> SELECT * FROM tb_admin;
 admin_no | login_id | passwd | nick | email
----------+----------+--------+------+-------
(0개 행)

test_db=> INSERT INTO TB_ADMIN(LOGIN_ID, PASSWD, NICK, EMAIL)
test_db-> VALUES('hong_gd', 'hong123', '홍길동', 'hong@gmail.com');
INSERT 0 1
test_db=> INSERT INTO TB_ADMIN(LOGIN_ID, PASSWD, NICK, EMAIL)
test_db-> VALUES('jang_nr', 'jang123', '장나라', 'jang@gmail.com');
INSERT 0 1
test_db=> SELECT * FROM tb_admin;
 admin_no | login_id | passwd  |  nick  |     email
----------+----------+---------+--------+----------------
        1 | hong_gd  | hong123 | 홍길동 | hong@gmail.com
        2 | jang_nr  | jang123 | 장나라 | jang@gmail.com
(2개 행)

```

- Procedure 생성
```
CREATE OR REPLACE PROCEDURE public.SP_L_ADMIN(out1 refcursor)
    LANGUAGE plpgsql
AS $procedure$
    BEGIN 
        OPEN out1 FOR
        SELECT admin_no, log_id, passwd, nick, email FROM tb_admin;
    END;
$procedure$
;

CREATE PROCEDURE
test_db=>

CREATE OR REPLACE FUNCTION public.FN_L_ADMIN(out1 refcursor)
    RETURNS SETOF refcursor
    LANGUAGE plpgsql
AS $function$
    BEGIN 
        OPEN out1 FOR
        SELECT admin_no, log_id, passwd, nick, email FROM tb_admin;
        RETURN NEXT out1;
    END;
$function$
;

CREATE FUNCTION
test_db=>

```
