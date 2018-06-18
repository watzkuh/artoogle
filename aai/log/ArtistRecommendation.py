import collections
import aai.predict as p

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
                birthDate = self.db.get_birthdate(artist)
                if birthDate:
                    birthDate = birthDate.split("-")[0]
                birthPlace = self.db.get_birthplace(artist)
                if not birthPlace:
                    birthPlace = "Buxtehude"
                movement = p.predict_movement(birthPlace, birthDate)
                print("Prediction: ", movement)
            movements.append(movement)
            previous = ""
            for mov in movements:
                if previous == mov:
                    self.recommendations[id] = movement
                previous = mov

    def get_recommendations(self, id):
        return self.db.get_artists_for_movement(self.recommendations.get(id))
