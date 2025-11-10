#
class TemperatureMixin:
    def read_temperature(self, units='standard') -> float:
        raise NotImplementedError()


class HumidityMixin:
    def read_humidity(self):
        raise NotImplementedError()


class PressureMixin:
    def read_pressure(self):
        raise NotImplementedError()


class RTCMixin:
    def datetime(self, dt=None) -> tuple | None:
        """
        Get or set the date and time of the RTC.

        With no arguments, this method returns an 8-tuple with the current date and time. With 1 argument (being an 8-tuple) it sets the date and time.

        The 8-tuple has the following format:
            `(year, month, day, weekday, hours, minutes, seconds, subseconds)`

            The meaning of the subseconds field is hardware dependent.

        :param dt: The 8-tuple with the date and time.
        :return: The 8-tuple with the RTC's date and time.
        """
        raise NotImplementedError()


class RTCAlarmMixin:
    def set_alarm(self, alarm_id: int = 0, when: int = None, day: int = 0, hr: int = 0, min: int = 0, sec: int = 0):
        raise NotImplementedError()

    def clear(self, alarm_id: int = 0):
        raise NotImplementedError()
