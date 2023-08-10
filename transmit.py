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
'''
In order to write packet data into FIFO user should:
1 Set FifoAddrPtr to FifoTxBaseAddrs.
2 Write PayloadLength bytes to the FIFO (RegFifo)
'''
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
    '''
def send_packet():
    addr = 0x0D
    data = 0x80
    send_data(addr, data)
    read_data(0x0D)
    '''
def main():
    # Sleep

    addr = 0b0000001
    data = 0b00000000
    send_data(addr,data)
    
    # LoRa enable

    addr = 0b0000001
    data = 0b10000000
    send_data(addr,data)
    # Standby mode enable

    addr = 0b0000001
    data = 0b10000001
    send_data(addr,data)

     #Set FifoAddrPtr to FifoTxBaseAddrs
    addr = 0b0001101
    data = 0b10000000
    send_data(addr,data)
     #Set RegPreambleLsb (Preamble length),left default = 12
     #addr = 0b0100000
    #Implicit header mode on 
    #RegModemConfig1
    addr = 0b0011101
    data = 0b00001101
    send_data(addr,data)
    #coding rate and spreading factor !!!
    #set RegModemconfig2
    addr = 0b0011110
    data = 0b11000100
    send_data(addr,data)
    #Set RegPayloadLength (0x22) 
    addr = 0b0100010
    data = 0b00001000 #8 bytes payload
    send_data(addr,data)
    # write the packet to the FIFO MEMORY
    #0x66 0x70 0x76 0x66 0x69 0x78 0x69 0x74 0x71 0x75 0x61 0x64 0x63 0x6F 0x70 0x74
    addr = 0b0000000
    data_values = [0b01100110, 0b01110000, 0b01110110, 0b01100110, 0b01101001, 0b01111000, 0b01101001, 0b01110100, 0b01110001, 0b01110101, 0b01100001, 0b01100100, 0b01100011, 0b01101111, 0b01110000, 0b01110100]
    for data in data_values:
        send_data(addr, data)
    #TX INIT
    addr = 0b0000001
    data = 0b00000011
    send_data(addr,data)
   # while True:
        # Read the response from the slave and print it
    addr = 0b0000001
    response_data = read_data(addr)
        
    print(f"Received data from the slave: {response_data:08b}")  # Print the response in binary format
    utime.sleep_ms(1000)
    
    response_data = read_data(addr)
    print(f"Received data from the slave: {response_data:08b}")  # Print the response in binary format


if __name__ == "__main__":
    main()
