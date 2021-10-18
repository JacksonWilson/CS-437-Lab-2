import socket
import picar_4wd as fc

HOST = "10.1.10.125" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

direction = "N/A"

def car_stop(client):
    global direction
    direction = "N/A"
    fc.stop()

def car_forward(client):
    global direction
    direction = "forward"
    fc.forward(10)

def car_backward(client):
    global direction
    direction = "backward"
    fc.backward(10)

def car_left(client):
    global direction
    direction = "left"
    fc.turn_left(10)

def car_right(client):
    global direction
    direction = "right"
    fc.turn_right(10)

def send_status(client):
    global direction
    status = "status:{}|{}|{}\r\n".format(direction, fc.cpu_temperature(), fc.power_read())
    client.sendall(status.encode('UTF-8'))

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        try:
            while True:
                client, clientInfo = s.accept()
                print("server recv from: ", clientInfo)
                data = client.recv(1024)      # receive 1024 Bytes of message in binary format
                if data == b"87\r\n":
                    if direction == "forward":
                        car_stop(client)
                    else:
                        car_forward(client)
                elif data == b"83\r\n":
                    if direction == "backward":
                        car_stop(client)
                    else:
                        car_backward(client)
                elif data == b"65\r\n":
                    if direction == "left":
                        car_stop(client)
                    else:
                        car_left(client)
                elif data == b"68\r\n":
                    if direction == "right":
                        car_stop(client)
                    else:
                        car_right(client)
                elif data != b"":
                    fc.stop()
                send_status(client)
        except Exception as e: 
            print(e)
            print("Closing socket") 
        finally:
            client.close()
            s.close() 

if __name__ == "__main__":
    try:
        main()
    finally:
        fc.stop()