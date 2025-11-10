from .udataclasses import Dataclass, validator
from constants import TempUnit


class WiFi(Dataclass):
    ssid: str = None
    passwd: str = None


class MQTT(Dataclass):
    server: str = None
    port: int = 1883
    user: str = None
    password: str = None
    ssl: bool = False
    cert: str = None


class Settings(Dataclass):
    department: str = None
    room: str = None
    units: str = TempUnit.STANDARD
    ntp_host: str = 'pool.ntp.org'
    admin_password: str = None
    measurement_interval: int = 60
    wifi: WiFi = WiFi()
    mqtt: MQTT = MQTT()

    @validator('units')
    def check_units(self, value):
        if value not in (TempUnit.METRIC, TempUnit.STANDARD, TempUnit.IMPERIAL):
            raise ValueError(f'Unit "{value}" is invalid.')
