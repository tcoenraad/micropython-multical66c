import mc66c
from machine import Timer


def mc66c_update(_timer):
    mc66c.update()


updater = Timer(0)
updater.init(period=30*60*1000, mode=Timer.PERIODIC, callback=mc66c_update)
