from database.data_manager import DataManager
from database.models import Player

class PlayerManager:
    def __init__(self):
        self.dm = DataManager()

    def get_or_create_player(self, name: str) -> Player:
        player = self.dm.get_player_by_name(name)

        if player:
            print(f"Welcome back, {player}")
            return player
        else:
            return self.dm.add_player(name)

    def close(self):
        self.dm.close()