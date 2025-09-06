#Chọn image nền có Python
FROM python:3.11-slim

#Đặt thư mục làm việc trong container
WORKDIR /app

#Copy file requirements chứa các thư viện cần cài
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#Copy toàn bộ source code vào container
COPY . .

ENV PYTHONPATH=/app

#Mở cổng 5000
EXPOSE 5000

#Chạy ứng dụng khi container khởi động
CMD ["python", "run.py"]