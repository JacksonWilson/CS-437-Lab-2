#!/usr/bin/env python3
"""PyBluez simple example rfcomm-server.py

Simple demonstration of a server application that uses RFCOMM sockets.

Author: Albert Huang <albert@csail.mit.edu>
$Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $
"""

import bluetooth
import picar_4wd as fc

direction = "N/A"

def car_stop(client):
    global direction
    direction = "N/A"
    fc.stop()
    client.sendall(b"Car stopped.")

def car_forward(client):
    global direction
    direction = "forward"
    fc.forward(10)
    client.sendall(b"Car moving forward.")

def car_backward(client):
    global direction
    direction = "backward"
    fc.backward(10)
    client.sendall(b"Car moving backward.")

def car_left(client):
    global direction
    direction = "left"
    fc.turn_left(10)
    client.sendall(b"Car moving left.")

def car_right(client):
    global direction
    direction = "right"
    fc.turn_right(10)
    client.sendall(b"Car moving right.")

def send_status(client):
    global direction
    status = "Direction: {}| PI Temperature: {}| PI Power: {}\r\n".format(direction, fc.cpu_temperature(), fc.power_read())
    client.sendall(status.encode('UTF-8'))

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print("Received", data)
        if data == b"forward":
            if direction == "forward":
                car_stop(client_sock)
            else:
                car_forward(client_sock)
        elif data == b"backward":
            if direction == "backward":
                car_stop(client_sock)
            else:
                car_backward(client_sock)
        elif data == b"left":
            if direction == "left":
                car_stop(client_sock)
            else:
                car_left(client_sock)
        elif data == b"right":
            if direction == "right":
                car_stop(client_sock)
            else:
                car_right(client_sock)
        elif data == b"stop":
            car_stop(client_sock)
        elif data == b"status":   
            send_status(client_sock)
        else:
            client_sock.sendall(b"Unknown command")

except OSError:
    pass
finally:
    fc.stop()
    print("Disconnected.")
    client_sock.close()
    server_sock.close()
    print("All done.")
