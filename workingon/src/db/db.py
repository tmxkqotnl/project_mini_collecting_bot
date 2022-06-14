from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

engine = create_engine(
    "postgresql://{user}:{password}@{url}/{db_name}".format(
        user=getenv("POSTGRES_JOB_TRAINING_USER"),
        password=getenv("POSTGRES_JOB_TRAINING_PASSWORD"),
        url=getenv("POSTGRES_JOB_TRAINING_URL"),
        db_name=getenv("POSTGRES_JOB_TRAINING_DB"),
    )
)

Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
