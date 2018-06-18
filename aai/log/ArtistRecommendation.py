import collections


class ArtistRecommendation:
    db = {}
    recommendations = {}

    def __init__(self, db):
        self.db = db

    def on_log(self, id, logs):
        artists = []
        movements = collections.deque(maxlen=2)
        for log in logs:
            artist = log["VALUE"]
            if artist in artists:
                continue
            else:
                artists.append(artist)

            movement = self.db.get_movement(artist)
            print(movement)
            if not movement:
                # TODO: Call our movement classifier
                continue
            movements.append(movement)
            previous = ""
            for mov in movements:
                if previous == mov:
                    self.recommendations[id] = movement
                previous = mov

    def get_recommendations(self, id):
        return self.db.get_artists_for_movement(self.recommendations.get(id))
