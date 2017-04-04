from blinkt import set_all, show, clear
from random import randint
from time import sleep


def blink():
	for i in range(1, 4):
		r = randint(255)
		g = randint(255)
		b = randint(255)
		set_all(r, g, b, brightness=0.5)
		show()
		sleep(1)
		clear()


def error():
	for i in range(1, 4):
		r = randint(255)
		g = randint(255)
		b = randint(255)
		set_all(r, g, b, brightness=0.5)
		show()
		sleep(1)
		clear()

