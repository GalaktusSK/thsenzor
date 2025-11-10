from .state import AbstractState
import time

class Diagnostics(AbstractState):
    """Diagnostics state: test DHT sensor availability and measured ranges.

    Behavior:
    - Try to instantiate or use an existing DHT sensor object on device.
    - Measure temperature and humidity, validate ranges:
      temperature: 0 <= T <= 50
      humidity: 20 <= H <= 90
    - On error or out-of-range values transition to Error state (set device.error_code).
    - On success transition to Operation state.

    The implementation is tolerant: it tries device helpers first (device.dht_sensor,
    device.create_dht_sensor()), then falls back to importing the MicroPython dht module
    if available. It handles different sensor APIs (measure()/temperature()/humidity()).
    """

    def enter(self):
        # indicate diagnostics start if LED available
        try:
            if getattr(self.device, "led", None) is not None:
                if hasattr(self.device.led, "set_color"):
                    self.device.led.set_color("GREEN")
                elif hasattr(self.device.led, "color"):
                    try:
                        self.device.led.color = "GREEN"
                    except Exception:
                        pass
        except Exception:
            pass

    def exec(self):
        # helper to transition to Error state with optional code/message
        def goto_error(code=None):
            try:
                from states.error import Error
                self.device.error_code = code
                self.device.change_state(Error(self.device))
            except Exception:
                # if we can't switch to Error, raise to be handled by Device.run()
                raise

        # 1) ensure we have a sensor instance
        sensor = getattr(self.device, "dht_sensor", None)
        if sensor is None:
            create_fn = getattr(self.device, "create_dht_sensor", None)
            if callable(create_fn):
                try:
                    self.device.dht_sensor = create_fn()
                    sensor = self.device.dht_sensor
                except Exception:
                    goto_error(code="dht_init_failed")
                    return
            else:
                # attempt to import MicroPython dht module as a fallback
                try:
                    import dht
                    import machine
                    pin_num = getattr(self.device, "dht_pin_number", None)
                    pin_obj = getattr(self.device, "dht_pin", None)
                    if pin_obj is None:
                        if pin_num is None:
                            # default to pin 4 if nothing specified
                            pin_num = 4
                        pin_obj = machine.Pin(pin_num)
                    # prefer DHT22, but allow device to override type via attribute
                    dht_cls = getattr(self.device, "dht_class", getattr(dht, "DHT22", None))
                    if dht_cls is None:
                        goto_error(code="dht_module_no_class")
                        return
                    try:
                        self.device.dht_sensor = dht_cls(pin_obj)
                        sensor = self.device.dht_sensor
                    except Exception:
                        goto_error(code="dht_init_failed")
                        return
                except Exception:
                    goto_error(code="dht_unavailable")
                    return

        # 2) measure values
        try:
            # many DHT drivers require an explicit measure() call
            if hasattr(sensor, "measure") and callable(sensor.measure):
                sensor.measure()
            # read temperature/humidity using common names
            if hasattr(sensor, "temperature"):
                temp = sensor.temperature()
            elif hasattr(sensor, "temp"):
                temp = sensor.temp()
            else:
                # some drivers provide tuple or dict; try generic access
                temp = None

            if hasattr(sensor, "humidity"):
                hum = sensor.humidity()
            elif hasattr(sensor, "hum"):
                hum = sensor.hum()
            else:
                hum = None

            # try to coerce to float where possible
            try:
                temp = float(temp) if temp is not None else None
            except Exception:
                temp = None
            try:
                hum = float(hum) if hum is not None else None
            except Exception:
                hum = None

        except Exception:
            goto_error(code="dht_measure_failed")
            return

        # 3) validate readings
        # If either value is None => fail
        if temp is None or hum is None:
            goto_error(code="dht_invalid_readings")
            return

        # range checks
        if not (0.0 <= temp <= 50.0):
            goto_error(code=f"temp_out_of_range:{temp}")
            return
        if not (20.0 <= hum <= 90.0):
            goto_error(code=f"hum_out_of_range:{hum}")
            return

        # 4) success -> proceed to Operation state
        try:
            from states.operation import Operation
            self.device.change_state(Operation(self.device))
        except Exception:
            # if operation state can't be reached, go to Error
            goto_error(code="no_operation_state")
            return

    def exit(self):
        # no special exit behavior
        pass
