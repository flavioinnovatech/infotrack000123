# -*- coding:utf8 -*-
#!/usr/bin/env python
import sys 
import socket
import os
import sys 
import select 
import tty 
import termios
from xml.etree import cElementTree as ElementTree
import pprint


class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})


TCP_IP = '192.168.1.119' 	# the server IP address
TCP_PORT = 5000			# the server port
BUFFER_SIZE = 20000		# the maximum buffer size (in chars) for a TCP packet
USERNAME = "extractor"		# the user that will log on CPR
PASSWORD = "extractor"		# the password for this user 


# Messages that will be sent to CPR: the ACK and the first auth message
authentication_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"1\" /><Data User=\""+USERNAME+"\" Password=\""+PASSWORD+"\" /></Package>"

ack_msg = "<?xml version=\"1.0\" encoding=\"ASCII\"?><Package><Header Version=\"1.0\" Id=\"98\" Reason=\"0\" Save=\"FALSE\"/><Data /></Package>"

#Checks if the packet sent was successful. If not,prints on screen the meaning of the reason specified.
def reasonMsg(msg):
    if msg == "0":
        return 1
    
    elif msg == "1":
        print "Error: Invalid username or password."
    elif msg == "2":
        print "Error: Session already open."
    elif msg == "3":
        print "Error: Invalid session code."
    elif msg == "4":
        print "Error: Invalid parameters."
    elif msg == "5":
        print "Error: Temporary registry created on memory."
    elif msg == "6":
        print "Error: Invalid datagram received."
    elif msg == "98":
        print "Error: User does not have permission to execute this action."
    elif msg == "99":
        print "Error: General failure. Could not execute the action"
    
    return 0

#Authentication function. Receives the connected TCP socket and starts the communication with the server
#   parameters:   s : the connected socket
#   return: the security key for the started session
def authentication(s):
    
    s.send(authentication_msg)
    try:
        data = s.recv(BUFFER_SIZE)
        #
        
        xml = ElementTree.fromstring(data[:len(data)-1])
        msg_reason = xml.find("Header").get("Reason")
        
        if reasonMsg(msg_reason):
            sec_key = xml.find("Data").get("SecurityKey")
        else:
            exit(int(msg_reason))
        return sec_key
    except:
	print ">> The connection has timed out."
        exit(1)


def isData():
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])



# ====> TESTING SEQUENCE FOR AUTHENTICATION UNDER CPR: 

os.system("clear")
print " \n\n\t\tWelcome to Infotrack CPR extractor script .\n\n"
print ">> Trying to connect to the server",TCP_IP + ":" + str(TCP_PORT)+"."

#creating and connecting trough the TCP socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

#s.connect((TCP_IP, TCP_PORT))
#sending the auth message, receiving the response and sending an ack message
print ">> Connection established. Sending authentication protocol."
key = authentication(s)
print "\n>> Authentication successful. Security key:",key

#mounting the XML response to server
seckey_msg = "<?xml version=\"1.0\" encoding=\"ASCII\" ?>\n<Package>\n  <Header Version=\"1.0\" Id=\"2\" />\n  <Data SessionId=\""+key+"\" />\n</Package>"
close_msg =  "<?xml version=\"1.0\" encoding=\"ASCII\"?>\n<Package>\n  <Header Version=\"1.0\" Id=\"99\" />\n  <Data SessionId=\""+key+"\" />\n</Package> "

blocker_msg =  "<?xml version=\"1.0\" encoding=\"ASCII\"?>\n<Package>\n  <Header Version=\"1.0\" Id=\"6\" />\n  <Data Account=\"2\" ProductId=\"41\" Serial=\"000017E8\" Priority=\"2\" />\n  <Command Blocker=\"ON\" Signal=\"ON\" Buzzer=\"ON\" Blocker=\"ON\"/>\n</Package>"

print ">> Sending session start message."

#sending the response to the server, and awaiting the outbox message
#print seckey_msg
#print len(seckey_msg)
#s.send(ack_msg)
#s.send(seckey_msg)
#s.send(blocker_msg)
#print blocker_msg

#data = s.recv(BUFFER_SIZE)
#print data

#a = sys.stdin.readline()



s.send(ack_msg)


#listening all information given by CPR. If timeout, exit the test sequence.
equipments = {}

old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())

while 1:
	
	if ([s],[],[]) == select.select([s],[],[],0):
		outbox = s.recv(BUFFER_SIZE)
		s.send(ack_msg)
		xml =  ElementTree.fromstring(outbox.strip(""))
		xmldict = XmlDictConfig(xml)
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(xmldict)

	else:
		if isData():
			c = sys.stdin.read(1)
			if c == '\x1b':
				print '>> Exiting the extraction script.'
				termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
				exit(0)
			elif c == '1':
				print ">> Sending Blocker signal to equipment with id 000017E8."
				blocker_msg =  "<?xml version=\"1.0\" encoding=\"ASCII\"?>\n<Package>\n  <Header Version=\"1.0\" Id=\"6\" />\n  <Data Account=\"2\" ProductId=\"41\" Serial=\"000017E8\" Priority=\"2\" />\n  <Command Blocker=\"ON\" Signal=\"ON\" Buzzer=\"ON\" Blocker=\"ON\"/>\n</Package>"
				s.send(blocker_msg)
			elif c == '2':
				pass
			elif c == '3':
				pass
			elif c == '4':
				pass


