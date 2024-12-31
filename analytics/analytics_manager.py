import pandas as pd
from database.models import GameEvent
from database.data_manager import DataManager
import json


class AnalyticsManager:
    def __init__(self):
        self.dm = DataManager()

    def get_game_events(self) -> pd.DataFrame:
        session = self.dm.session
        events = session.query(GameEvent).all()

        data = []
        for ev in events:
            data.append({
                'id': ev.player_id,
                'player_id': ev.player_id,
                'round_id': ev.round_id,
                'game_id': ev.game_id,
                'event_index': ev.event_index,
                'n_back_value': ev.n_back_value,
                'actual_number': ev.actual_number,
                'player_number_response': ev.player_number_response,
                'number_response_status': ev.number_response_status,
                'actual_position': ev.actual_position,
                'player_position_response': json.dumps(ev.player_position_response)
                    if ev.player_position_response else None,
                'position_response_status': ev.position_response_status,
                'position_response_time': ev.position_response_time,
                'number_response_time': ev.number_response_time
            })
        return pd.DataFrame(data)

    def close(self):
        self.dm.close()