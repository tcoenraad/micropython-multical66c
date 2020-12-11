# micropython-multical66c

## Installation

- [Flash MicroPython](http://docs.micropython.org/en/latest/esp8266/tutorial/intro.html)
- Setup [WebREPL](http://docs.micropython.org/en/latest/esp8266/tutorial/repl.html)
- Upload both `main.py` & `mc66c.py` files via `WebREPL`
- Disable UART REPL to prevent noise, e.g. in `boot.py` by uncommenting `uos.dupterm(None, 1) # disable REPL on UART(0)`

Run on `WebREPL` once:

- `import upip`
- `upip.install("umqtt.robust")`


## Test
- Run `mc66c_update(None)`. It logs what will be pushed to MQTT.