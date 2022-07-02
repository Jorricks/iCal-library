from typing import List, Literal, Optional, Tuple, Union

import pendulum
from pendulum import Date, DateTime, Duration

from ical_reader.base_classes.property import Property


class _PeriodFunctionality(Property):
    def _parse_period_values(self) -> List[Tuple[DateTime, DateTime]]:
        list_of_periods: List[Tuple[DateTime, DateTime]] = []
        for item in self.value.split(","):
            instance = self._parse_individual_duration_str(item)
            if not isinstance(instance, tuple) or len(instance) != 2:
                raise TypeError(f"{instance} is of {type(instance)=} while it should be a tuple.")
            for index, sub_instance in enumerate(instance):
                if not isinstance(sub_instance, DateTime):
                    raise TypeError(
                        f"{instance[index]=} is of {type(sub_instance)=} while it should be of type "
                        f"Tuple[DateTime, DateTime]."
                    )
            list_of_periods.append(instance)
        return list_of_periods

    @staticmethod
    def _parse_individual_duration_str(duration: str) -> Tuple[DateTime, DateTime]:
        first_str, second_str = duration.split("/")
        first_instance: DateTime = _ExOrRDate._parse_individual_datetime_or_duration_str(first_str)
        second_instance: Union[DateTime, Duration] = _ExOrRDate._parse_individual_datetime_or_duration_str(second_str)
        if not isinstance(first_instance, DateTime):
            raise TypeError(f"Expected {duration=} to contain a DateTime as first argument.")
        if isinstance(second_instance, DateTime):
            return first_instance, second_instance
        elif isinstance(second_instance, Duration):
            computed_datetime: DateTime = first_instance + second_instance
            return first_instance, computed_datetime
        else:
            raise TypeError(f"Expected {duration=} to contain a DateTime or Duration as second argument.")


class _ExOrRDate(_PeriodFunctionality):
    def _parse_datetime_values(self) -> List[DateTime]:
        list_of_datetimes: List[DateTime] = []
        for item in self.value.split(","):
            instance = self._parse_individual_datetime_or_duration_str(item)
            if not isinstance(instance, DateTime):
                raise TypeError(f"{instance} is of {type(instance)=} while it should be a DateTime.")
            list_of_datetimes.append(instance)
        return list_of_datetimes

    @staticmethod
    def _parse_individual_datetime_or_duration_str(datetime_str: str) -> Union[DateTime, Duration]:
        return pendulum.parse(datetime_str, tz=None)

    def _parse_date_values(self) -> List[Date]:
        list_of_dates: List[Date] = []
        for item in self.value.split(","):
            instance = self._parse_individual_date_str(item)
            if not isinstance(instance, Date):
                raise TypeError(f"{instance} is of {type(instance)=} while it should be a Date.")
            list_of_dates.append(instance)
        return list_of_dates

    @staticmethod
    def _parse_individual_date_str(date: str) -> Date:
        return Date(int(date[0:4]), int(date[4:6]), int(date[6:8]))


class FreeBusyProperty(_PeriodFunctionality):
    @classmethod
    def get_property_ical_name(cls) -> str:
        return "FREEBUSY"

    @property
    def free_busy_type(self):
        return self.get_property_parameter("FBTYPE", "BUSY")

    @property
    def all_values(self) -> List[Tuple[DateTime, DateTime]]:
        return self._parse_period_values()


class EXDate(_ExOrRDate):
    @property
    def kind(self) -> Optional[Literal["DATE-TIME", "DATE"]]:
        return self.property_parameters.get("VALUE", "DATE-TIME")

    @property
    def all_values(self) -> Union[List[DateTime], List[Date]]:
        if self.kind == "DATE-TIME":
            return self._parse_datetime_values()
        elif self.kind == "DATE":
            return self._parse_date_values()
        else:
            raise ValueError(f"{self.kind=} should be one in ['DATE-TIME', 'DATE'].")


class RDate(_ExOrRDate):
    @property
    def kind(self) -> Optional[Literal["DATE-TIME", "DATE", "PERIOD"]]:
        return self.property_parameters.get("VALUE", "DATE-TIME")

    @property
    def all_values(self) -> Union[List[DateTime], List[Date], List[Tuple[DateTime, DateTime]]]:
        if self.kind == "DATE-TIME":
            return self._parse_datetime_values()
        elif self.kind == "DATE":
            return self._parse_date_values()
        elif self.kind == "PERIOD":
            return self._parse_period_values()
        else:
            raise ValueError(f"{self.kind=} should be one in ['DATE-TIME', 'DATE', 'PERIOD'].")
