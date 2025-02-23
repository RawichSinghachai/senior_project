import logging

class AppLogger:
    _logger = None  # เก็บ instance ของ logger 

    @staticmethod
    def get_logger(log_file="app.log"):
        """ คืนค่า Logger ที่มีเพียงหนึ่ง instance """
        if AppLogger._logger is None:
            # สร้าง Logger ใหม่เมื่อยังไม่มี
            AppLogger._logger = logging.getLogger("AppLogger")
            AppLogger._logger.setLevel(logging.DEBUG)

            # ตรวจสอบว่ามี Handler อยู่แล้วหรือยัง ถ้ามีแล้วไม่ต้องเพิ่มซ้ำ
            if not AppLogger._logger.handlers:
                log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

                # Handler สำหรับบันทึกลงไฟล์
                file_handler = logging.FileHandler(log_file, encoding="utf-8")
                file_handler.setFormatter(log_format)

                # Handler สำหรับแสดงผลใน Console
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(log_format)

                # เพิ่ม Handler เข้า Logger (ครั้งเดียว)
                AppLogger._logger.addHandler(file_handler)
                AppLogger._logger.addHandler(console_handler)

        return AppLogger._logger  # คืนค่า Logger ที่มีอยู่แล้ว
