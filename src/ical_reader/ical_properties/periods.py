from typing import List, Literal, Optional, Tuple, Union

import pendulum
from pendulum import Date, DateTime, Duration

from ical_reader.base_classes.property import Property


class _PeriodFunctionality(Property):
    """
    Provide methods to help to parse duration values.

    This class should be inherited by a Property.
    """

    def _parse_period_values(self) -> List[Tuple[DateTime, DateTime]]:
        """
        Parse multiple values, delimited by comma's, representing periods.

        Example value for self.value: 19960403T020000Z/19960403T040000Z,19960404T010000Z/PT3H
        :return: List of tuples containing two DateTimes representing the start and end of the duration respectively.
        """
        list_of_periods: List[Tuple[DateTime, DateTime]] = []
        for item in self.value.split(","):
            item = item.strip()
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
    def _parse_individual_duration_str(period_str: str) -> Tuple[DateTime, DateTime]:
        """
        Parse an individual period represented by DateTime/DateTime or DateTime/Duration.

        :param period_str: The period to parse. Examples: 19960403T020000Z/19960403T040000Z or 19960404T010000Z/PT3H
        :return: A tuple containing two DateTimes representing the start and end of the duration respectively.
        """
        first_str, second_str = period_str.split("/")
        first_instance: DateTime = _ExOrRDate._parse_individual_datetime_or_duration_str(first_str)
        second_instance: Union[DateTime, Duration] = _ExOrRDate._parse_individual_datetime_or_duration_str(second_str)
        if not isinstance(first_instance, DateTime):
            raise TypeError(f"Expected {period_str=} to contain a DateTime as first argument.")
        if isinstance(second_instance, DateTime):
            return first_instance, second_instance
        elif isinstance(second_instance, Duration):
            computed_datetime: DateTime = first_instance + second_instance
            return first_instance, computed_datetime
        else:
            raise TypeError(f"Expected {period_str=} to contain a DateTime or Duration as second argument.")


class _ExOrRDate(_PeriodFunctionality):
    """
    Provide methods to help to parse different kind of values a Property could find.

    This class should be inherited by a Property.
    """

    def _parse_datetime_values(self) -> List[DateTime]:
        """
        Parses DateTime values. Example of a possible value of self.value: 19970714T123000Z,19970714T123300Z
        :return: A List of DateTimes representing the start of an event/component.
        """
        list_of_datetimes: List[DateTime] = []
        for item in self.value.split(","):
            item = item.strip()
            instance = self._parse_individual_datetime_or_duration_str(item)
            if not isinstance(instance, DateTime):
                raise TypeError(f"{instance} is of {type(instance)=} while it should be a DateTime.")
            list_of_datetimes.append(instance)
        return list_of_datetimes

    @staticmethod
    def _parse_individual_datetime_or_duration_str(datetime_or_duration_str: str) -> Union[DateTime, Duration]:
        """
        Parse an individual datetime or duration string.
        :param datetime_or_duration_str: A string represent either a datetime or duration.
        :return: A pendulum.DateTime if the string represented a datetime. Return a pendulum.Duration otherwise.
        """
        return pendulum.parse(datetime_or_duration_str, tz=None)

    def _parse_date_values(self) -> List[Date]:
        """
        Parse Date values. Example of a possible value of self.value: 19970101,19970120,19970217
        :return: A list of pendulum.Date representing the start of an event/component.
        """
        list_of_dates: List[Date] = []
        for item in self.value.split(","):
            instance = self._parse_individual_date_str(item)
            if not isinstance(instance, Date):
                raise TypeError(f"{instance} is of {type(instance)=} while it should be a Date.")
            list_of_dates.append(instance)
        return list_of_dates

    @staticmethod
    def _parse_individual_date_str(date: str) -> Date:
        """
        Parse an individual date string.
        :param date: A string representing a date.
        :return: A pendulum.Date.
        """
        return Date(int(date[0:4]), int(date[4:6]), int(date[6:8]))


class FreeBusyProperty(_PeriodFunctionality):
    """
    The FREEBUSY property defines one or more free or busy time intervals.

    Note: This class is called FreeBusyProperty to not be confused with the VFreeBusy component.
    """

    @classmethod
    def get_ical_name_of_class(cls) -> str:
        """Overwrite the iCal name of this class as it is not *FREEBUSYPROPERTY* but *FREEBUSY*."""
        return "FREEBUSY"

    @property
    def free_busy_type(self) -> str:
        """
        Specifies the free or busy time type.

        Values are usually in the following list but can be anything: FREE, BUSY, BUSY-UNAVAILABLE, BUSY-TENTATIVE
        """
        return self.get_property_parameter_default("FBTYPE", "BUSY")

    @property
    def periods(self) -> List[Tuple[DateTime, DateTime]]:
        """
        All the periods present in this property for which we define a free or busy time.
        :return: A list of tuples, where each tuple values consists of two DateTimes indicating the start and end
        respectively.
        """
        return self._parse_period_values()


class EXDate(_ExOrRDate):
    """
    The EXDATE property defines the list of DATE-TIME exceptions for recurring events, to-dos, journal entries,
    or time zone definitions.
    """

    @property
    def kind(self) -> Optional[Literal["DATE-TIME", "DATE"]]:
        """The kind of the values. It is either DATE-TIME or DATE. The default is DATE-TIME."""
        return self.property_parameters.get("VALUE", "DATE-TIME")

    @property
    def excluded_date_times(self) -> Union[List[DateTime], List[Date]]:
        """A list of all excluded Dates or DateTimes. The type will be according to kind reported by `self.kind()`."""
        if self.kind == "DATE-TIME":
            return self._parse_datetime_values()
        elif self.kind == "DATE":
            return self._parse_date_values()
        else:
            raise ValueError(f"{self.kind=} should be one in ['DATE-TIME', 'DATE'].")


class RDate(_ExOrRDate):
    """
    The RDATE property defines the list of DATE-TIME values for recurring events, to-dos, journal entries,
    or time zone definitions.
    """

    @property
    def kind(self) -> Optional[Literal["DATE-TIME", "DATE", "PERIOD"]]:
        """The kind of the values. It is either DATE-TIME, DATE or PERIOD. The default is DATE-TIME."""
        return self.property_parameters.get("VALUE", "DATE-TIME")

    @property
    def all_values(self) -> Union[List[DateTime], List[Date], List[Tuple[DateTime, DateTime]]]:
        """
        A list of all recurring Dates, DateTimes or Periods. The periods are defined by tuples containing two
        datetimes representing the start and stop respectively. The returned types in the list will be according to
        the kind reported by `self.kind()`.
        """
        if self.kind == "DATE-TIME":
            return self._parse_datetime_values()
        elif self.kind == "DATE":
            return self._parse_date_values()
        elif self.kind == "PERIOD":
            return self._parse_period_values()
        else:
            raise ValueError(f"{self.kind=} should be one in ['DATE-TIME', 'DATE', 'PERIOD'].")
