# Import required packages
import socket
import threading

# Create socket and L3 L4 protocol(IP/TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pars = ('127.0.0.1', 8888)


# Set up the IP address and port number
s.bind(pars)
# At most five clients
s.listen(5)

# The content of HTML and CSS
html = '<html><head><link href="style.css" rel="stylesheet" type = "text/css"></head><body>good</body></html>'
css = 'Body {color: red;}'

# Data send from server to client
# Header
def resM(code,obj,file='html'):
    resH=""
    if str(code)=="200":
        resH += "HTTP/1.1 "+"200 OK"+" \r\n"
    elif str(code)=="301":
        resH += "HTTP/1.1 "+"301 Moved Permanently\r\nLocation: http://127.0.0.1:8888/good.html"+"\r\n\r\n"
    elif str(code)=="404":
        resH = "HTTP/1.1 "+"404 NotFound"+" \r\n"
    
    # Distinghish the type(CSS/HTML)
    if file=='html':
        resH += 'Content-Type: text/'+'html'+'; charset=UTF-8\r\n'
    elif file=='css':
        resH += 'Content-Type: text/'+'css'+'; charset=UTF-8\r\n'
    
    resH += "\r\n"
    
    if obj:    
        resH += str(obj)

    # print out respond message
    print(resH)
    return resH



# Client connect
def serveClient(clientsocket, address):
    while True:
        # Maximun size of the data
        data = clientsocket.recv(1024)

        # If received the data
        if data:
            # Split the data by " "
            cData = data.decode("utf-8").split(' ')
            #print((cData))

            # First one is GET method
            # Second one is address
            method = cData[0]
            url = cData[1]

            
            if url=="/":
                res = resM(200,html)
                clientsocket.send(bytes(res,"UTF-8"))

            if url=="/good.html":
                res = resM(200,html)
                clientsocket.send(bytes(res,"UTF-8"))
            
            if url=="/style.css":
                res = resM(200,css,'css')
                clientsocket.send(bytes(res,"UTF-8"))

            if url=="/redirect.html":
                res = resM(301,"redirect")
                clientsocket.send(bytes(res,"UTF-8"))
                
            if url=="/notfound.html":
                res = resM(404,'notfound')
                clientsocket.send(bytes(res,"UTF-8"))
            clientsocket.close()
            # Terminate TCP
            print("CLOSE\n")
            break

# Use (src IP, dst IP, src port, dst port) to distinguish different users
while True:
    # Accept a new client and get it's information
    (clientsocket, address) = s.accept()
    # print(clientsocket)
    # print(address)
    
    # When new clients connect, open a thread for them
    threading.Thread(target = serveClient, args = (clientsocket, address)).start()