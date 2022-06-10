import mfrc522
from os import uname
from machine import Pin, SPI
from time import sleep
import utime
from utime import sleep_ms
from ssd1306 import SSD1306_SPI

       
def do_access():
    # chama o pin
    PINO_FECHADURA = 22
    pino_fechadura = Pin(PINO_FECHADURA, Pin.OUT)
    chave_lida = ""
    
    def abrir(saida):
        saida.value(1)
    
    def fechar(saida):
        saida.value(0)
        
       
    while True:
        chave_lida = do_read()
        f = open("chaves.txt", "r")
        chaves = []
        for chave in f:
            chave = chave.replace("\r\n", "")
            chaves.append(chave)
        print(chaves)
        chave_lida = str(chave_lida)
        if chave_lida in chaves:
            abrir(pino_fechadura)
            sleep(3)
            fechar(pino_fechadura)
        return
        
def do_write():

	if uname()[0] == 'WiPy':
		rdr = mfrc522.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
	elif uname()[0] == 'esp8266':
		rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
	elif uname()[0] == 'rp2':
		rdr = mfrc522.MFRC522(2,3,4,8,5)
	else:
		raise RuntimeError("Unsupported platform")

	print("")
	print("Place card before reader to write address 0x08")
	print("")

	try:
		while True:

			(stat, tag_type) = rdr.request(rdr.REQIDL)

			if stat == rdr.OK:

				(stat, raw_uid) = rdr.anticoll()

				if stat == rdr.OK:
					print("New card detected")
					print("  - tag type: 0x%02x" % tag_type)
					print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					print("")

					if rdr.select_tag(raw_uid) == rdr.OK:

						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

						if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
							stat = rdr.write(8, b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f")
							rdr.stop_crypto1()
							if stat == rdr.OK:
								print("Data written to card")
							else:
								print("Failed to write data to card")
						else:
							print("Authentication error")
					else:
						print("Failed to select tag")

	except KeyboardInterrupt:
		print("Bye")

def do_read():
	
	if uname()[0] == 'WiPy':
		rdr = mfrc522.MFRC522("GP14", "GP16", "GP15", "GP22", "GP17")
	elif uname()[0] == 'esp8266':
		rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
	elif uname()[0] == 'rp2':
		#rdr = mfrc522.MFRC522(SPI_CLK, SPI_MOSI, SPI_MISO, RESET, CS(SDA))
		rdr = mfrc522.MFRC522(2,3,4,8,5)
	else:
		raise RuntimeError("Unsupported platform")

	print("")
	print("Place card before reader to read from address 0x08")
	print("")

	try:
		while True:
			sleep(1)
			(stat, tag_type) = rdr.request(rdr.REQIDL)

			if stat == rdr.OK:

				(stat, raw_uid) = rdr.anticoll()

				if stat == rdr.OK:
					print("New card detected")
					print("  - tag type: 0x%02x" % tag_type)
					print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					print("")

					if rdr.select_tag(raw_uid) == rdr.OK:

						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

						if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
							print("Address 8 data: %s" % rdr.read(8))
							retorno = rdr.read(8)
							rdr.stop_crypto1()
							return retorno
						else:
							print("Authentication error")
					else:
						print("Failed to select tag")

	except KeyboardInterrupt:
		print("Bye")
		
class OLED:
    def __init__(self):
        spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
        self.oled = SSD1306_SPI(128, 64, spi, Pin(17),Pin(20), Pin(15))
    def exibir(self,value,posx,posy):
        #oled = SSD1306_SPI(WIDTH, HEIGHT, spi, dc,rst, cs) use GPIO PIN NUMBERS
        self.oled.text(value,posx,posy)
        self.oled.show()
    def limpar(self):
        self.oled.fill(0)
        self.oled.show()

#Para executar o código		


led = Pin(28, Pin.OUT)
pir = Pin(16, Pin.IN)

utime.sleep(2)
oled = OLED()
while True:
   print(pir.value())
   if pir.value() == 0:
       print(pir.value())
       print("LED On")
       oled.exibir("teste python", 59, 10)
       do_access()
       utime.sleep(2)
   else:
       print(pir.value())
       print("Esperando movimento")
       oled.limpar()
       utime.sleep(2)




