import socket


host = "192.168.1.65"
port = 8888


def getAlpha(string):
    """ Removes all non-alphanumeric characters from a string.
    """
    alpha = ''.join([char for char in string if char.isalpha()])
    return alpha


def msgChain(chain, connection):
    """ Continue sending messages to client connection until all are sent.

    Args:
        chain (list): Messages that will be sent over server
        connection (socket.socket): Client socket object to route messages to
    """
    if(not chain):
        return
    # the request should contain the same command string as our next response
    request = connection.recv(32)
    request = request.decode("utf-8")
    if(getAlpha(chain[0]) in request):
        print("RECEIVED: {:<25}\tSENDING: {}".format(request, chain[0]))
        connection.send(bytes(chain.pop(0), "utf-8"))
    msgChain(chain, connection)


# start sever and connect to client
print(f"Starting server on host {host}")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(3)
client_connection, client_address = s.accept()
print(f"Connected to client at {client_address}")

script_entries = ['*GM1#', '*RMD#', '*RA0#', '*LA0#', '*SWA0#', '*DA0#', '*LMD0#',
                  '*ESDT2016-06-23 09:07:21.2#', '*EDIL1234#', '*EVDA1000000#', '*ETDA1000000#', '*EVIA1234#', '*EADI1234#', '*EAGR1234#']

# allow user to continuously send inputs to the client
while(True):
    msg = input("msg: ")

    if(msg == "stop"):
        print("Stopping server")
        break
    elif(msg == "script"):
        print("Waiting for Ignition client...")
        msgChain(script_entries.copy(), client_connection)
        continue

    client_connection.send(bytes(msg, "utf-8"))

client_connection.close()
