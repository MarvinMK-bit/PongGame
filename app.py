import random
import socket
from _thread import *
import pickle
import pygame

# Game related global variables
window_width = 700
window_height = 700
player1_start_x = 10
player1_start_y = 300
player2_start_x = 670
player2_start_y = 300
ball_start_x = 350
ball_start_y = 350
ball_start_velocity_x = 3
ball_start_velocity_y = 1
bat_width = 20
bat_height = 100
bat_movement_speed = 20
ball_diameter = 20

# Packet size for sending and receiving between server and clients
data_size = 4096

# FPS speed for the game clock
game_speed = 30