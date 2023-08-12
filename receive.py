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
print('hello world')

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
def send_data(addr, data):
    # Start the SPI transaction by pulling NSEL low
    cs.value(0)

    # Send the bytes through SPI
    mask = 0x80
    tmp = addr | mask
    spi.write(bytes([tmp , data]))
    # End the SPI transaction by pulling NSEL high
    cs.value(1)

def read_data(addr):
    # Start the SPI transaction by pulling NSEL low
    cs.value(0)

    # Send the address byte for read access (bit 7: 1, bits 6-1: 000000)
    mask = 0x00
    spi.write(bytes([addr | mask]))

    # Read the data from the slave (MISO line)
    response = spi.read(1)

    # End the SPI transaction by pulling NSEL high
    cs.value(1)

    return response[0]
def main():
    # Sleep

    addr = 0b0000001
    data = 0b00000000
    send_data(addr,data)
    
    # LoRa enable

    addr = 0b0000001
    data = 0b10000000
    send_data(addr,data)
    
    addr = 0b0000001
    response_data = read_data(addr)   
    print(f"Received data from the slave: {response_data:08b}")  # Print the response in binary format
    
    #Set FifoAddrPtr to FifoRxBaseAddr
    addr = 0b0001101
    data = 0b00000000
    send_data(addr,data)
    
    
    # Standby mode enable

    addr = 0b0000001
    data = 0b10000001
    send_data(addr,data)
    #mode request RXsingle
    addr = 0b0000001
    data = 0b10000110
    #read number of bytes received so far 
    while True:
        addr = 0b0010011
        response_data = read_data(addr)   
        print(f"Received data from the slave: {response_data:08b}")  # Print the response in binary format
if __name__ == "__main__":
    main()
