from enum import Enum


class Authority(Enum):
    NO_AUTHORITY = 0  # 환자등의 외부 사용자
    USER = 1  # 진찰, 검사, 처방 등을 수행하는 의료진
    ADMIN = 2  # 진료일정, 권한관리를 수행하는 관리자(원무)
