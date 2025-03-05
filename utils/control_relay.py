from gpiozero import LED

# กำหนดพินควบคุมรีเลย์ (GPIO17)
relay = LED(17)
relay.on()

def active_relay():
    relay.off()

def deactive_relay():
    relay.on()


# try:
#     active_relay()
# except KeyboardInterrupt:
#     print("Program stopped")

