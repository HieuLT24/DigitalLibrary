from urllib.parse import quote


class Config:
    SECRET_KEY = "HJGGHD*^&R$YGFGHDYTRER&*TRTYCHG^R&^TYHGH"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:%s@localhost/librarydb?charset=utf8mb4" % quote(
    "root")
    

    
    # Cloudinary configuration
    CLOUDINARY_CLOUD_NAME = 'dsfghzlat'
    CLOUDINARY_API_KEY = '784677976657694'
    CLOUDINARY_API_SECRET = 'Y573YM27ykBpFzzWs7AIq2RWOtY'
    
    # Upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = 'Home/Library'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

