import machine
import utime

# Initialize the SPI bus
# Settings

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
def send_packet():
    addr = 0x0D
    data = 0x80
    
def main():
    addr = 0b0000001
    data = 0b00000000
    # Send the first data through SPI
    send_data(addr,data)

    addr = 0b0000001
    data = 0b10000000
    
    # Send the first data through SPI
    send_data(addr,data)

    addr = 0b0000001
    data = 0b00000011
    # Send the first data through SPI
    send_data(addr,data)
   # while True:
        # Read the response from the slave and print it
        addr = 0b0000001
        response_data = read_data(addr)
        
        print(f"Received data from the slave: {response_data:08b}")  # Print the response in binary format
        utime.sleep_ms(1000)

if __name__ == "__main__":
    main()


# Continue with other code or functions after receiving the NAV-PVT message


#Now the split method is called on the hex_data bytes object, and each message is printed without the 'b5' prefix. If you need to process each complete message separately, you can do it inside the loop where we are printing the messages. For example, you can check the message IDs and extract specific data from each message as needed.


    #b"\xb5\x62\x01\x07": "NAV-PVT",

#Now, the error message is inside quotes, as requested. This code will continuously send Message 4 and check for the desired message in the received data. If the received data contains invalid characters or incomplete bytes, it will print the error message and continue processing the next batch of data.

    # Concatenate 'var_name' with 'b5' using an f-string
    #string_concat = f"b5{var_name}"
'''
while True:
    # Check if there is data available in the UART buffer
    if uart.any():
        # Read the data as bytes
        raw_data = uart.read(uart.any())

        # Convert raw_data to hexadecimal representation
        hex_data = raw_data.hex()

        # Process the hex_data as needed
        # For example, print it or extract specific information from the message
        print("Received Hex Data:", hex_data)
   '''     

# Function to calculate the Fletcher 8-bit checksum

'''
# Function to send UBX frame
def send_ubx_frame(msg_class, msg_id, payload):
    preamble_sync_char1 = b"\xB5"  # 0xB5 in hex
    preamble_sync_char2 = b"\x62"  # 0x62 in hex

    # Calculate payload length (N)
    payload_length = len(payload)

    # Send the UBX frame
    uart.write(preamble_sync_char1)
    uart.write(preamble_sync_char2)
    uart.write(msg_class)
    uart.write(msg_id)
    uart.write(bytes([payload_length]))
    uart.write(bytes(payload))
    uart.write(b"\x1F")  # CK_A = 0x1F
    uart.write(b"\x3E")  # CK_B = 0x3E

# Example usage with correct message class (0x01), message ID (0x02), and 28-byte payload (all zeros)
msg_class = b"\x01"
msg_id = b"\x02"
payload_data = b"\x00" * 28  # 28-byte payload data (all zeros)
send_ubx_frame(msg_class, msg_id, payload_data)
'''