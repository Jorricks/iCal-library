from typing import Tuple

from ical_reader.base_classes.property import Property


class GEO(Property):
    @property
    def geo_value(self) -> Tuple[float, float]:
        latitude, longitude = self.value.split(";")
        return float(latitude), float(longitude)
