from blinkt import set_all, show, clear
from random import randint
from time import sleep


def blink():
	for i in range(1, 4):
		r = 0
		g = 255
		b = 0
		set_all(r, g, b, brightness=1)
		show()
		sleep(.5)
		clear()
		show()


def error():
	for i in range(1, 4):
		r = 255
		g = 0
		b = 0
		set_all(r, g, b, brightness=1)
		show()
		sleep(.5)
		clear()
		show()

