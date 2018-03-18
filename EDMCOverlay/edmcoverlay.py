"""
Client library for EDMCOverlay
"""

import sys
import socket
import json
import os
import subprocess
import time


SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 5010

HERE = os.path.dirname(os.path.abspath(__file__))
PROG = "EDMCOverlay.exe"


def find_server_program():
    """
    Look for EDMCOverlay.exe
    :return:
    """

    locations = [
        os.path.join(HERE, PROG),
        os.path.join(HERE, "EDMCOverlay", PROG),
        os.path.join(HERE, "EDMCOverlay", "EDMCOverlay", "bin", "Release", PROG),
        os.path.join(HERE, "EDMCOverlay", "EDMCOverlay", "bin", "Debug", PROG),
    ]
    for item in locations:
        if os.path.isfile(item):
            print "found {}...".format(item)
            return item
    return None

_service = None


def ensure_service():
    """
    Start the overlay service program
    :return:
    """
    if HERE not in sys.path:
        sys.path.append(HERE)

    global _service
    program = find_server_program()

    if program:
        # if it isnt running, start it
        try:
            exedir = os.path.abspath(os.path.dirname(program))
            if _service:
                if _service.poll() is not None:
                    _service = None
            if not _service:
                print "starting {}".format(program)
                _service = subprocess.Popen([program], cwd=exedir)

            time.sleep(2)
            if _service.poll() is not None:
                subprocess.check_call([program], cwd=exedir)
                raise Exception("{} exited".format(program))
        except Exception as err:
            print "error in ensure_service: {}".format(err)


def shutdown_service():
    """
    Shutdown the overlay service program
    :return:
    """
    global _service
    try:
        # if it is running, shut it down
        if _service:
            pid = _service.pid
            if _service.poll() is None:
                _service.terminate()
            time.sleep(2)
            if _service.poll() is not None:
                print "{} service {} exited".format(PROG, pid)
        else:
            print "{} service not running.".format(PROG)
    except Exception as err:
        print "error in shutdown_service: {}".format(err)


class Overlay(object):
    """
    Client for EDMCOverlay
    """

    def __init__(self, server=SERVER_ADDRESS, port=SERVER_PORT):
        self.server = server
        self.port = port
        self.connection = None

    def connect(self):
        """
        open the connection
        :return:
        """
        connection = socket.socket()
        connection.connect((self.server, self.port))
        self.connection = connection

    def send_message(self, msgid, text, color, x, y, ttl=0, size="normal"):
        """
        Send a message
        :param msgid:
        :param text:
        :param color:
        :param x:
        :param y:
        :param ttl:
        :param size:
        :return:
        """
        if not self.connection:
            ensure_service()
            self.connect()

        msg = {"id": msgid,
               "color": color,
               "text": text,
               "size": size,
               "x": x, "y": y,
               "ttl": ttl}
        try:
            self.connection.send(json.dumps(msg))
            self.connection.send("\n")
        except Exception as err:
            print "error in send_message: {}".format(err)
            self.connection = None
            raise

    def send_rectangle(self, msgid, color, fill, x, y, w, h, ttl=0):
        """
        Send a message
        :param msgid:
        :param color: outline color
        :param fill: fill color
        :param x:
        :param y:
        :param w:
        :param h:
        :param ttl:
        :return:
        """
        if not self.connection:
            ensure_service()
            self.connect()

        msg = {"id": msgid,
               "shape": "rect",
               "color": color,
               "fill": fill,
               "x": x, "y": y,
               "w": w, "h": h,
               "ttl": ttl}
        try:
            self.connection.send(json.dumps(msg))
            self.connection.send("\n")
        except Exception as err:
            print "error in send_rectangle: {}".format(err)
            self.connection = None
            raise

    def vectorpoint(self, x, y, color, marker="", text=""):
        """
        Convert point values to vector point object
        :param x:
        :param y:
        :param color: line color
        :param marker: mark point as "cross" or "circle"
        :param text: mark point with text
        :return:
        """
        return {"x": x, "y": y,
                "color": color,
                "marker": marker,
                "text": text}

    def send_vector(self, msgid, color, points, ttl=0):
        """
        Send a message
        :param msgid:
        :param color: line color
        :param points: list of points [[x,y,color,marker,text],...]
        :param ttl:
        :param size: font size, either "normal" or "large"
        :return:
        """
        if not self.connection:
            ensure_service()
            self.connect()
    
        msg = {"id": msgid,
               "shape": "vect",
               "color": color,
               "vector": [apply(self.vectorpoint, point) for point in points],
               "ttl": ttl}
        try:
            self.connection.send(json.dumps(msg))
            self.connection.send("\n")
        except Exception as err:
            print "error in send_vector: {}".format(err)
            self.connection = None
            raise


def debugconsole():
    """
    Print stuff
    """
    import load as loader

    print >> sys.stderr, "Loading..\n"
    loader.plugin_start()

    cl = Overlay()

    print >> sys.stderr, "Reading..\n"
    while True:
        line = sys.stdin.readline().strip()
        print >> sys.stderr, "sending... {}".format(line)
        cl.send_message("msg", line, "red", 100, 100)


if __name__ == "__main__":
    debugconsole()
