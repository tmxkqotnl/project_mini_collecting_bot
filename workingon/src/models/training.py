from sqlalchemy import CHAR, DATE, INTEGER, TEXT, VARCHAR, NUMERIC, Column
from src.db.db import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

# fix - tel_no type
class Training(Base):
    __tablename__ = "training_item"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tr_id = Column(TEXT())  # 훈련과정ID
    base_adrs = Column(TEXT())  # 시도군주소
    base_adrs_sub = Column(TEXT())  # 시군구주소

    fee = Column(TEXT())  # 수강비
    actual_fee = Column(TEXT())  # 실제_훈련비

    emp_3_month_cnt = Column(TEXT())  # 고용보험3개월 취업인원 수
    emp_rate_3 = Column(TEXT())  # 고용보험3개월 취업률
    emp_rate_6 = Column(TEXT())  # 고용보험6개월 취업률

    ncs_code = Column(TEXT())
    yard = Column(TEXT())  # 정원
    registerd = Column(TEXT())  # 수강신청_인원

    inst_name = Column(TEXT())  # 부제목
    inst_link = Column(TEXT())  # 부제목 링크 (훈련기관정보 hrd-net link)

    tr_name = Column(TEXT())  # 제목
    tr_link = Column(TEXT())  # 제목 링크 (훈련과정 정보 hrd-netlink)

    supervisor = Column(TEXT())  # 주관부처
    tel_no = Column(TEXT())  # 전화번호 (담당자 전화번호)

    tr_start_dt = Column(TEXT())  # 훈련시작일자
    tr_end_dt = Column(TEXT())  # 훈련종료일자

    target = Column(TEXT())  # 훈련대상
    target_category = Column(TEXT())  # 훈련구분 (훈련종류코드)

    inst_code = Column(TEXT())  # 훈련기관_코드
    inst_id = Column(TEXT())  # 훈련기관ID

    degree = Column(INTEGER())  # 훈련과정_순차(회차)
