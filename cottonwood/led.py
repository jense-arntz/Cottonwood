from blinkt import set_all, show, clear
from random import randint
from time import sleep


def blink():
	for i in range(1, 4):
		r = 255
		g = 0
		b = 0
		set_all(r, g, b, brightness=1)
		show()
		sleep(1)
		clear()
		show()


def error():
	for i in range(1, 4):
		r = randint(0, 255)
		g = randint(0, 255)
		b = randint(0, 255)
		set_all(r, g, b, brightness=0.5)
		show()
		sleep(1)
		clear()

