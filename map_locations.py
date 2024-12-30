from map_label import MapLabel


class MapLocations():
    def __init__(self):
        self.high_importance: list[MapLabel] = []
        self.medium_importance: list[MapLabel] = []
        self.low_importance: list[MapLabel] = []

    def get_locations(self, importance: int) -> list[MapLabel]:
        if importance == 3:
            return self.high_importance
        elif importance == 2:
            return self.medium_importance
        elif importance == 1:
            return self.low_importance

    def add_location(self, label: MapLabel) -> None:
        if label.importance == 3:
            self.high_importance.append(label)
        elif label.importance == 2:
            self.medium_importance.append(label)
        elif label.importance == 1:
            self.low_importance.append(label)
