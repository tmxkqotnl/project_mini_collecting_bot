from sqlalchemy import CHAR, DATE, INTEGER, TEXT, VARCHAR, NUMERIC, Column
from src.db.db import Base

# fix - type fix
class Institution(Base):
    __tablename__ = "institution_item"

    address = Column(TEXT())
    address_detail = Column(TEXT())
    homepage = Column(TEXT())
    
    inst_name = Column(TEXT())
    inst_code = Column(TEXT(),primary_key=True)
    
    real_fee = Column(TEXT())
    ncs_code = Column(TEXT())  # fix
    ncs_name = Column(TEXT())  # fix
    ncs_yn = Column(TEXT())  # fix
    
    logo = Column(TEXT())
    grant = Column(TEXT())  # fix
    total_days = Column(TEXT())  # fix
    total_hours = Column(TEXT())  # fix
    eval_grade = Column(TEXT())  # fix
    tr_catecory_code = Column(TEXT())
    charge = Column(TEXT())
    charge_email = Column(TEXT())
    charge_tel = Column(TEXT())  # fix
    tr_class = Column(TEXT())  # fix
    tr_id = Column(TEXT())  # fix
    tr_name = Column(TEXT())  # fix

    tr_main_class = Column(TEXT())
    tr_main_class_name = Column(TEXT())
    zipcode = Column(TEXT())
    # detail
    tr_class_detail = Column(TEXT())
    tr_type = Column(TEXT())
    
    tr_day = Column(TEXT())
    tr_hours = Column(TEXT())
    tr_total_fee = Column(TEXT())
    
    tr_degree = Column(TEXT())
    # tr_code = Column(TEXT())
    tr_name_another = Column(TEXT())
    