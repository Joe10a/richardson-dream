from microbit import *
class I2C_LCD1602:
    def __init__(self, LCD_I2C_ADDR):
        self.ADDR=LCD_I2C_ADDR
        self.buf = bytearray(1)
        self.BK = 0x08
        self.RS = 0x00
        self.E = 0x04
        self.setcmd(0x33)
        sleep(5)
        self.send(0x30)
        sleep(5)
        self.send(0x20)
        sleep(5)
        self.setcmd(0x28)
        self.setcmd(0x0C)
        self.setcmd(0x06)
        self.setcmd(0x01)
        self.version = '1.0'
    def setReg(self, dat):
        self.buf[0] = dat
        i2c.write(self.ADDR, self.buf)
        sleep(1)
    def send(self, dat):
        d = dat & 0xF0
        d |= self.BK
        d |= self.RS
        self.setReg(d)
        self.setReg(d | 0x04)
        self.setReg(d)
    def setcmd(self, cmd):
        self.RS = 0
        self.send(cmd)
        self.send(cmd << 4)
    def setdat(self, dat):
        self.RS = 1
        self.send(dat)
        self.send(dat << 4)
    def clear(self):
        self.setcmd(1)
    def backlight(self, on):
        if on:
            self.BK = 0x08
        else:
            self.BK = 0
        self.setdat(0)
    def on(self):
        self.setcmd(0x0C)
    def off(self):
        self.setcmd(0x08)
    def char(self, ch, x=-1, y=0):
        if x >= 0:
            a = 0x80
            if y > 0:
                a = 0xC0
            a += x
            self.setcmd(a)
        self.setdat(ch)
    def puts(self, s, x=0, y=0):
        if len(s) > 0:
            self.char(ord(s[0]), x, y)
            for i in range(1, len(s)):
                self.char(ord(s[i]))
    def shl(self):
        self.setcmd(0x18)
    def shr(self):
        self.setcmd(0x1c)

lcd = I2C_LCD1602(0x27)

while True:
    for v in range(1, 6, 4): #v:velocity
        t = 1000 / v #sleep time
        lcd.puts("velocity:", 0, 0)
        lcd.puts("velocity:", 0, 1)
        lcd.puts("1", 9, 0)
        lcd.puts("2", 9, 1)
        #lcd.puts("sleep", 11, 0)
        #lcd,puts("=" + str(t), 11, 1)
        sleep(1000)
        lcd.clear()
        sleep(500)

        for n in range(16):
            k = n * 1
            l = n * 2
            lcd.puts("o", k, 0)
            lcd.puts("o", l, 1)
            sleep(t)
            lcd.clear()
            #lcd.shr()
    sleep(500)
    lcd.puts("Finish", 0, 0)

    break
