# ใช้ python:
FROM python:3.10

# ตั้งค่า working directory ใน container
WORKDIR /appy

# คัดลอกไฟล์ requirements.txt ไปยัง container
COPY requirements.txt .

# ติดตั้ง dependencies
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์ทั้งหมดในโปรเจกต์ไปยัง container
COPY . .

# เปิดพอร์ต 5000 สำหรับ Flask
EXPOSE 5000

# รันเซิร์ฟเวอร์ Flask
CMD ["python", "appy.py"]
