# EDMC Overlay (c) 2017 Ian Norton

## Custom modifications (c) 2018 Robert Shaw

Changes in this fork from original Ian Norton version:

* Fixed so TTL value of 0 properly defaults to 10 seconds.
* Adds version information to startup overlay text.
* Adjusts virtual screen dimensions to 1920x1080@0:0.
* Fixes overlay window so it can't be activated, focused or appear in task view.
* Adds auto-shutdown of overlay service on EDMC exit (issue #6).
* Adds "send_rectangle" and "send_vector" Python API methods.
* Fixes "exedir" undefined error during certain error conditions.
* Changes location of log file to %USERPROFILE%/AppData/Local/Temp folder.
* Outputs current application version to log file.
* Updated configuration files for VS2017 and VSCode build support.

## About

EDMC Overlay is a helper program for Elite:Dangerous, It provides a means for
a program such as EDMC to display simple messages in the game's DirectX window.

## Compatibility

* Currently supports 64Bit Elite:Dangerous (Horizons) on Windows Only.
* 64bit Non-Horizons may work. YMMV.
* Apple support is not likley (I don't have a Mac)
* "Windowed" or "Bordless Fullscreen" mode only.

## Installation

This is released as a standard EDMC Plugin, simple unpack the archive into the EDMC
plugin folder.  Releases of EDMC Overlay are in part inspired by the Overlay.NET
library from [Overlay.NET](https://github.com/lolp1/Overlay.NET). Though it no
longer contains this library.

## Python API

The EDMC Overlay Python API provides simple methods to send text or graphic items
to the running EDMC Overlay executable via the protocol described below. These
built-in plugin API methods allow other plugins to easily send messages without
having to communicate directly with the EDMC Overlay service for ease of use.

The following API assumes you have an overlay object from the plugin created
like the following:

```python
this.overlay = edmcoverlay.Overlay()
```

To send a text:

```python
this.overlay.send_message("test1", "You are low on fuel!", "red", 200, 100, 8, "normal")
```

The server will process this as an instruction to display the message "You are low on fuel!"
in red text at 200,100 for 8 seconds.

To send a rectangle:

```python
this.overlay.send_rectangle("fred", "#ccff00", "red", 100, 10, 30, 5, 8)
```

The server will process this as an instruction to display a red filled rectangle
with a yellow outline at 100,10 with size 30x5 for 8 seconds.

To send a vector:

```python
this.overlay.send_vector("line1", "yellow", [[100, 100, "blue", "cross", "P1"],
                                             [200, 150, "blue", "cross", "P2"],
                                             [300, 100, "blue", "cross", "P3"]], 5)
```

The server will process this as an instruction to display a vector line in yellow
that zig-zags from 100:100 to 200:150 to 300:100 and draws blue crosses at each point
with a cooresponding text label for 5 seconds.

Supported point marker values are:
 "cross" and "circle"

## Protocol

EDMC Overlay offers a very very simple line-json based network protocol.

The service when started will listen on TCP 127.0.0.1:5010.  If EDMCOverlay cannot
detect EliteDangerous64.exe it will exit silently.

Assuming EliteDangerous64.exe is running, you may send a single JSON message (on one line)
Like so:

```json
{"id": "test1", "text": "You are low on fuel!", "size": "normal", "color": "red", "x": 200, "y": 100, "ttl": 8}
```

Supported colors values are:
 "red", "green", "yellow", "blue" or "#rrggbb".

Supported size values are:
 "normal" and "large"

Supported ttl values are:
 positive number of seconds to display,
 zero defaults to 10 seconds,
 any negative number will display forever.

The server will process this as an instruction to display the message "You are low on fuel!"
in red text at 200,100 for 8 seconds.

Be sure to send a newline ("\n") character after your message. You may need to flush the
socket.

Additionally, you may draw rectangles by setting the "shap" to "rect" and setting the "color" and/or "fill" values.

```json
{"id": "fred", "shape": "rect", "x": 100, "y": 10, "w": 30, "h": 5, "fill": "red", "color": "#ccff00"}
```

The server will process this as an instruction to display a red filled rectangle
with a yellow outline at 100,10 with size 30x5 for the default 10 seconds.

There are (currently) no response values from the service.

## MIT License

Copyright 2017 Ian Norton (original plugin)

Copyright 2018 Robert Shaw (custom modifications)

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
