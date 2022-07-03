from typing import Tuple

from ical_reader.base_classes.property import Property


class GEO(Property):
    """
    The GEO property specifies information related to the global position for the activity specified by a calendar
    component.
    """

    @property
    def geo_value(self) -> Tuple[float, float]:
        """Return the value as two floats representing the latitude and longitude."""
        latitude, longitude = self.value.split(";")
        return float(latitude), float(longitude)
