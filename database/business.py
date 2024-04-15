from dataclasses import dataclass

from database.review import Review


@dataclass
class Business:
    business_id: str
    full_address: str
    active: str
    categories: str
    city: str
    review_count: int
    business_name: str
    neighborhood: str
    latitude: float
    longitude: float
    state: str
    stars: float
    reviews: list[Review] = None

    def __eq__(self, other):
        return self.business_id == other.business_id

    def __hash__(self):
        return hash(self.business_id)

    def get_reviews(self):
        """
        lo costruisco solo quando chiamo il getter, alla creazione del business è vuoto
        :return:
        """
        if self.reviews is None:
            pass
        else:
            return self.reviews