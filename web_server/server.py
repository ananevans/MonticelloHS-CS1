import socket
import re
from urllib import response

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while (True):
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(65537)
            requestline = str(data, 'iso-8859-1')
            requestline = requestline.rstrip('\r\n')
            print(requestline)
            words = requestline.split()
            print("===== Command", words[0])
            print("===== Resource requested", words[1])
            if (words[1] == "/main"):
                conn.sendall(b""" HTTP/1.1 200 ok \n
                    <!DOCTYPE html>
                    <html>
                    <body>

                    <h2>HTML Forms</h2>

                    <form action="/name">
                        <label for="fname">First name:</label><br>
                        <input type="text" id="fname" name="fname" value="John"><br>
                        <label for="lname">Last name:</label><br>
                        <input type="text" id="lname" name="lname" value="Doe"><br><br>
                        <input type="submit" value="Submit">
                    </form> 

                    <p>If you click the "Submit" button, the form-data will be sent to a page called "/name".</p>

                    </body>
                    </html>""")
            else: 
                args = re.split('=|&', words[1])
                if (len(args) > 3):
                    conn.sendall(bytes(""" HTTP/1.1 200 ok \n
                        <!DOCTYPE html>
                        <html>
                        <body>

                        You typed """ +  args[1] + " " + args[3] +
                        """
                        </body>
                        </html>""", 'iso-8859-1'))
                else:
                    conn.sendall(bytes("HTTP/1.1 404 Invalid request" + words[1], 'iso-8859-1'))