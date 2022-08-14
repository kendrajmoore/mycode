#!/usr/bin/env python

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA.

# based on code provided by raymond mosteller (thanks!)

#This module provides functions for encoding binary data to printable ASCII characters and# decoding such encodings back to binary data.
import base64
#The getpass module provides two functions to get passwords
import getpass
#The OS module in Python provides functions for interacting with the operating system. 
import os
#the socket API are used to send messages across a network.
import socket
#This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.
import sys
#This module provides a standard interface to extract, format and print stack traces of Python programs. 
import traceback
#Paramiko is a pure-Python [1] (2.7, 3.4+) implementation of the SSHv2 protocol [2], providing both client and server functionality.
import paramiko
#Mini python 3 compatibility module
from paramiko.py3compat import input


# setup logging
paramiko.util.log_to_file("demo_sftp.log")

# Paramiko client configuration
UseGSSAPI = True  # enable GSS-API / SSPI authentication
DoGSSAPIKeyExchange = True # enable DoGSS-API
Port = 22 # ssh port

# get hostname
username = ""
#if the user inputs more than 2 words via command line
if len(sys.argv) > 1:
    #the hostname is the second work
    hostname = sys.argv[1]
    #verify that the input is correct formal
    if hostname.find("@") >= 0:
        #split on the @
    username, hostname = hostname.split("@")
else: # not more than 2 words, get user input for hostname
    hostname = input("Hostname: ")
    # if no hostnamee
if len(hostname) == 0:
    #alert the user
    print("*** Hostname required.")
    sys.exit(1) #leave the program if no hostname is provided
#if hostname find the :
if hostname.find(":") >= 0:
    #divided hostname into hostname and portstr
    hostname, portstr = hostname.split(":")
    #make port string an int
    Port = int(portstr)


# get username
if username == "":
    #get the username
    default_username = getpass.getuser()
    #use default or allow user to input username
    username = input("Username [%s]: " % default_username)
    if len(username) == 0: # if no response use default
        username = default_username
if not UseGSSAPI: # no useGSSAPI
    #get password
    password = getpass.getpass("Password for %s@%s: " % (username, hostname))
else:
    #there is no password
    password = None


# get host key, if we know one
hostkeytype = None
#no hostkey
hostkey = None

try:
    #look in this path for hostkeys
    host_keys = paramiko.util.load_host_keys(
        os.path.expanduser("~/.ssh/known_hosts")
    )
    #doesnt work look for windows computer
except IOError:
    try:
        # try ~/ssh/ too, because windows can't have a folder named ~/.ssh/
        host_keys = paramiko.util.load_host_keys(
            os.path.expanduser("~/ssh/known_hosts")
        )
    except IOError: #error
        print("*** Unable to open host keys file") #we dont have any host keys
        host_keys = {} #empty host kerys
#find hostname
if hostname in host_keys:
    #get first item in the list to make hostkeytype
    hostkeytype = host_keys[hostname].keys()[0]
    #use hostname and hostkeytype to get host key for hostkeys dict
    hostkey = host_keys[hostname][hostkeytype]
    #print oout host key type
    print("Using host key of type %s" % hostkeytype)


# now, connect and use paramiko Transport to negotiate SSH2 across the connection
try:
    #pass hostname and port to paramiko
    t = paramiko.Transport((hostname, Port))
    #to connect give hostkey, username, password, use hostname to connect to domain
    t.connect(
        hostkey,
        username,
        password,
        gss_host=socket.getfqdn(hostname),
        gss_auth=UseGSSAPI,
        gss_kex=DoGSSAPIKeyExchange,
    )
    #take al the information and use paramiko to establish sftp
    sftp = paramiko.SFTPClient.from_transport(t)

    # dirlist on remote host
    dirlist = sftp.listdir(".")
    #print dirlist
    print("Dirlist: %s" % dirlist)

    # copy this demo onto the server
    try:
        #make a folder
        sftp.mkdir("demo_sftp_folder")
    except IOError:
        #error folder already exists
        print("(assuming demo_sftp_folder/ already exists)") #print error
    with sftp.open("demo_sftp_folder/README", "w") as f:#creat and write to a file
        f.write("This was created by demo_sftp.py.\n") #write this sentence
    with open("demo_sftp.py", "r") as f: # read a file
        data = f.read() # the read infor
    sftp.open("demo_sftp_folder/demo_sftp.py", "w").write(data) # write to the file
    print("created demo_sftp_folder/ on the server") # print result

    # copy the README back here
    with sftp.open("demo_sftp_folder/README", "r") as f: # read this file
        data = f.read()
    with open("README_demo_sftp", "w") as f:
        f.write(data) # overwrite this file
    print("copied README back here") #print result

    # BETTER: use the get() and put() methods
    sftp.put("demo_sftp.py", "demo_sftp_folder/demo_sftp.py") #update this file
    sftp.get("demo_sftp_folder/README", "README_demo_sftp") #get this file

    t.close() #close the connection

except Exception as e: #catch an error
    print("*** Caught exception: %s: %s" % (e.__class__, e)) #print error
    traceback.print_exc() #print the entire error
    try: 
        t.close() #close the connection
    except:
        pass #null
    sys.exit(1) # there is an error exit program
