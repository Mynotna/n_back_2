import pygame
from game_logic.game_manager import Game
from database.data_manager import DataManager


def main():
    from analytics.analytics_manager import AnalyticsManager

    analyzer = AnalyticsManager()
    df = analyzer.get_game_events()
    print(df.head())
    analyzer.close()


# def main():
#     dm = DataManager()
#
#     # Add or retrieve a player
#     player_name = input("What's your name, Sir? :=> ")
#     player = dm.add_player(player_name)
#     print(f"Player is {player}")
#
#     # Start new session
#     new_session = dm.start_new_session()
#     print(f"New session started with id: {new_session.session_id}")
#
#     # 3. Save a test game event
#     game_event = dm.save_game_event(
#         player_id=player.id,
#         session_id=new_session.session_id,
#         game_id=1,
#         event_index=0,
#         n_back_value=2,
#         actual_number=5,
#         player_number_response=3,
#         number_response_status="incorrect",
#         actual_position=(100, 200),
#         player_position_response=None,
#         position_response_status="missed",
#         position_response_time=500.0,
#         number_response_time=700.0
#     )
#
#     print(f"Game event saved {game_event}")
#
#     dm.close()

if __name__ == "__main__":
    main()




