class ArtistRecommendation:
    db = {}
    recommendations = {}

    def __init__(self, db):
        self.db = db

    def on_log(self, id, logs):
        artists = []
        movements = {}
        for key, value in logs.items():
            artist = value["VALUE"]
            if artist in artists:
                continue
            else:
                artists.append(artist)

            movement = self.db.get_movement(artist)
            if not movement:
                continue

            count = movements.get(movement)
            if not count:
                count = 0
            count = count + 1
            movements[movement] = count
            if movements.get(movement) > 1:

                self.recommendations[id] = movement

    def get_recommendations(self, id):
        return self.db.get_artists_for_movement(self.recommendations.get(id))
