from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column  # 元素/主key
from sqlalchemy import exists, update
# 創接口/建立關系relationship(table.ID)
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import create_engine
# sqlalchemy 查詢前連結，结束後，調用 session.close() 關閉連結
from sqlalchemy.pool import NullPool
from sqlalchemy.sql.sqltypes import DATETIME, INTEGER, TEXT
import yaml
import datetime

yamlData = None
with open("./config/mysql.yaml", "r", encoding="utf-8") as stream:
    yamlData = yaml.load(stream, Loader=yaml.FullLoader)
    stream.close()
    print("Yaml data loading complete!")
yamlData = yamlData['Database']


# DB的資訊
DBInfo = f"mysql+pymysql://{yamlData['userName']}:{yamlData['userPwd']}@{yamlData['ip']}/{yamlData['databaseName']}?charset=utf8mb4"
DBLink = create_engine(DBInfo, poolclass=NullPool)
Base = declarative_base()
print("ORM INIT complete!")


class Navs(Base):
    __tablename__ = yamlData['navTable']
    __table_args__ = {"mysql_charset": "utf8"}
    search_key = Column(TEXT, nullable=True)
    brand = Column(TEXT, primary_key=True)
    ppath = Column(TEXT, nullable=True)
    createAt = Column(DATETIME)
    updateAt = Column(DATETIME)

    def __init__(self, search_key: str, brand: str, ppath: str):
        """Navs寫入之參數

        Args:
            search_key (str): 產品名稱
            brand (str): 廠牌名稱
            ppath (str): 廠牌之金鑰
        """
        self.search_key = search_key
        self.brand = brand
        self.ppath = ppath
        self.createAt = datetime.datetime.now()
