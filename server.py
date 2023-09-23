import socket
import threading
import time

mx_seq=7
nr_bufs=(mx_seq+1)/2
no_naq=True
seq_nr_oldest_frame=mx_seq+1
timer_active = False
window_size = 1
next_frame_to_send = 0
frame_expected = 0

# Function to simulate starting a timer
def start_timer():
    global timer_active
    timer_active = True
    threading.Timer(2, handle_timeout).start()  # Simulating a timeout of 2 seconds

# Function to handle timeout event
def handle_timeout():
    global timer_active
    timer_active = False
    print("Timeout occurred for frame", frame_expected)
    send_frame(frame_expected)  # Resend the frame on timeout

def between(a,b,c):
    return ((a <= b) and (b < c)) or ((c < a) and (a <= b)) or ((b < c) and (c < a))

def send_frame(frame_expected):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 12345)
    global fk
    global frame_nr
    global buffer

    s_kind=fk
    if(fk == "data"):
        s_info = buffer[frame_nr % nr_bufs]
    s_seq = frame_nr
    s_ack = (frame_expected + mx_seq) % (mx_seq+1)
    if(fk == "nak"):
        no_nak=False
    s_data = f"{s_info}|{s_seq}|{s_ack}".encode()
    s.sendto(s_data, server_address)
    if(fk == "data"):
        start_timer(frame_nr % nr_bufs)
    handle_timeout()

def server():
    # host = socket.gethostname()
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    print("Socket binded to %s" % port)

    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + address)

    conn.close()

def enable_network_layer():
    pass

enable_network_layer() 
ack_expected = 0 
next_frame_to_send = 0 
frame_expected = 0
too_far = nr_bufs
nbuffered = 0

if __name__ == '__main__':
    server()
