from urllib.parse import quote


class Config:
    SECRET_KEY = "HJGGHD*^&R$YGFGHDYTRER&*TRTYCHG^R&^TYHGH"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:%s@localhost/librarydb?charset=utf8mb4" % quote(
    "root")

