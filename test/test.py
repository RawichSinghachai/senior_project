import logging

# ตั้งค่าระบบ Logging และบันทึกลงไฟล์ "app.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),  # บันทึกลงไฟล์
        logging.StreamHandler()  # แสดงใน Console ด้วย
    ]
)

# ทดสอบ Log
logging.info("เริ่มต้นการทำงาน")
logging.error("พบข้อผิดพลาด")
