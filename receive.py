'''
_________________________   _______________._______  ___.______________
\_   _____/\______   \   \ /   /\_   _____/|   \   \/  /|   \__    ___/
 |    __)   |     ___/\   Y   /  |    __)  |   |\     / |   | |    |   
 |     \    |    |     \     /   |     \   |   |/     \ |   | |    |   
 \___  /    |____|      \___/    \___  /   |___/___/\  \|___| |____|   
     \/                              \/              \_/               

'''
import machine
import utime

# Initialize the SPI bus
# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(13, machine.Pin.OUT)

# Initialize SPI
spi = machine.SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(10),
                  mosi=machine.Pin(11),
                  miso=machine.Pin(12))