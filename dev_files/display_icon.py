import time
import board
import busio
import digitalio
import adafruit_ssd1306

from PIL import Image, ImageDraw, ImageFont

class OLED_Display_Char:
    def __init__(self, width, height, addr, reset_pin, icon_path):
        self.oled_reset = digitalio.DigitalInOut(reset_pin)
        self.width = width
        self.height = height
        self.image = Image.new('1', (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.icon = Image.open(icon_path).convert('1')
        self.oled = adafruit_ssd1306.SSD1306_I2C(width, height, busio.I2C(board.SCL, board.SDA), addr=addr, reset=self.oled_reset)
        
    def clear_display(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        
    def draw_icon(self):
        self.clear_display()
        width, height = self.icon.size
        x = (self.width - width) // 2
        y = (self.height - height) // 2
        self.image.paste(self.icon, (x, y))
        self.oled.image(self.image)
        self.oled.show()

if __name__ == '__main__':
    display = OLED_Display(128, 64, 0x3C, board.D4, 'icon.bmp')
    
    while True:
        # Update the display with the icon
        display.draw_icon()
        
        # Wait for a period of time before updating the display again
        time.sleep(1.0)
