import socket
from _thread import start_new_thread
import pickle

class PongDTO:
    def __init__(self):
        self.game_id = 0
        self.player_id = 0
        self.player_x = []
        self.player_y = []
        self.ball_x = 0
        self.ball_y = 0
        self.ball_velocity_x = 0
        self.ball_velocity_y = 0
        self.ball_direction_x = ''
        self.ball_direction_y = ''
        self.start_play = False
        self.msg = ''
        self.end_play = False
        self.points = [0, 0]

class Game:
    def __init__(self):
        self.game_id = 0
        self.player_ids = []
        self.game_dto = PongDTO()

    def initiate_dto(self):
        self.game_dto.player_x = [player1_start_x, player2_start_x]
        self.game_dto.player_y = [player1_start_y, player2_start_y]
        self.game_dto.ball_x = ball_start_x
        self.game_dto.ball_y = ball_start_y
        self.game_dto.ball_velocity_x = ball_start_velocity_x
        self.game_dto.ball_velocity_y = ball_start_velocity_y
        self.game_dto.ball_direction_x = random.choice(('positive', 'negative'))
        self.game_dto.ball_direction_y = random.choice(('positive', 'negative'))
        self.game_dto.game_id = self.game_id
        self.game_dto.start_play = False
        self.game_dto.points = [0, 0]

# Global variables
game_ids = []

def get_game_player_id():
    game_id = len(game_ids)
    player_id = 0 if game_id % 2 == 0 else 1
    if len(game_ids) == 0 or player_id == 0:
        game = Game()
        game.game_id = game_id
        game.player_ids.append(player_id)
        game.initiate_dto()
        game_ids.append(game)
    return game_id, player_id

def threaded_client(conn, game_id, player_id):
    send_dto = get_game_dto(game_id)
    send_dto.player_id = player_id
    send_dto.msg = f"Welcome to game {game_id}, Player {player_id}"
    conn.send(pickle.dumps(send_dto))

    run = True
    while run:
        try:
            receive_dto = pickle.loads(conn.recv(data_size))
            if not receive_dto:
                print('DTO not received')
                run = False
            else:
                receive_dto.player_id = player_id
                if receive_dto.start_play:
                    update_game_state(receive_dto)
                else:
                    update_game_dto(receive_dto)
                game_dto = get_game_dto(game_id)
                game_dto.player_id = player_id
                conn.sendall(pickle.dumps(game_dto))
        except Exception as e:
            run = False
            print("An error occurred:", e)

    print("Lost connection")
    game = get_game(game_id)
    game.player_ids.remove(player_id)
    if len(game.player_ids) == 0:
        game_ids.remove(game)
    else:
        game.initiate_dto()
    conn.close()

def get_game_dto(game_id):
    for game in game_ids:
        if game_id == game.game_id:
            return game.game_dto

def update_game_dto(dto):
    game_dto = get_game_dto(dto.game_id)
    game_dto.player_y[dto.player_id] = dto.player_y[dto.player_id]

def update_game_state(dto):
    game_dto = get_game_dto(dto.game_id)
    game_dto.player_y[dto.player_id] = dto.player_y[dto.player_id]
    # Ball movement and game logic
    # ... (Implement ball movement and collision logic here)

# Server setup
server = "localhost"
port = 5555
data_size = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    print(f"Binding failed: {e}")
    exit()

s.listen()
print("Waiting for a connection, Server Started")

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    game_id, player_id = get_game_player_id()
    print("Game id -", game_id, ", Player id -", player_id)
    print('Game length -', len(game_ids))
    start_new_thread(threaded_client, (conn, game_id, player_id))
