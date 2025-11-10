from .state import AbstractState
import time

# Durations in seconds
SHORT_PRESS_DURATION = 3
LONG_PRESS_DURATION = 6

class Init(AbstractState):
    """Init state: initialize device, check button long-press and settings,
    then transition to FactoryReset / Configuration / Diagnostics accordingly.

    This implementation is hardware-agnostic: it will try to use helper
    methods on `device` if they exist (e.g. `is_button_pressed()` or
    `led.set_color(...)`). If they are not present it falls back to
    simple checks (e.g. device.settings).
    """

    def enter(self):
        # indicate startup: try to set LED to green
        try:
            if getattr(self.device, "led", None) is not None:
                # prefer a set_color API if available
                if hasattr(self.device.led, "set_color"):
                    self.device.led.set_color("GREEN")
                elif hasattr(self.device.led, "color"):
                    try:
                        self.device.led.color = "GREEN"
                    except Exception:
                        pass
        except Exception:
            # be resilient to any LED/driver errors
            pass

    def exec(self):
        # 1) detect button long-press if device provides a method
        hold_time = 0.0
        is_pressed_fn = getattr(self.device, "is_button_pressed", None)
        # also accept a boolean attribute `button_pressed` that may be polled
        has_button_attr = hasattr(self.device, "button_pressed")

        if callable(is_pressed_fn) or has_button_attr:
            start = None
            # poll until LONG_PRESS_DURATION or until button released
            while True:
                pressed = False
                try:
                    if callable(is_pressed_fn):
                        pressed = bool(is_pressed_fn())
                    else:
                        pressed = bool(getattr(self.device, "button_pressed", False))
                except Exception:
                    pressed = False

                if pressed:
                    if start is None:
                        start = time.time()
                    hold_time = time.time() - start
                    # change LED color at thresholds
                    try:
                        if hold_time >= LONG_PRESS_DURATION:
                            if hasattr(self.device, "led") and hasattr(self.device.led, "set_color"):
                                self.device.led.set_color("ORANGE")
                        elif hold_time >= SHORT_PRESS_DURATION:
                            if hasattr(self.device, "led") and hasattr(self.device.led, "set_color"):
                                self.device.led.set_color("CYAN")
                    except Exception:
                        pass
                else:
                    # button not pressed -> break the polling loop
                    break

                if start is not None and (time.time() - start) >= LONG_PRESS_DURATION:
                    # reached max threshold, stop polling
                    break

                time.sleep(0.05)

        # 2) decide next state
        try:
            # factory reset (long press)
            if hold_time >= LONG_PRESS_DURATION:
                from states.factory_reset import FactoryReset
                self.device.change_state(FactoryReset(self.device))
                return

            # configuration (short press)
            if hold_time >= SHORT_PRESS_DURATION:
                from states.configuration import Configuration
                self.device.change_state(Configuration(self.device))
                return

            # if no settings or invalid settings -> configuration
            settings = getattr(self.device, "settings", None)
            if settings is None:
                from states.configuration import Configuration
                self.device.change_state(Configuration(self.device))
                return

            # basic validity check: expect settings to be a dict-like object
            if not isinstance(settings, dict):
                from states.configuration import Configuration
                self.device.change_state(Configuration(self.device))
                return

            # otherwise -> diagnostics
            from states.diagnostics import Diagnostics
            self.device.change_state(Diagnostics(self.device))

        except Exception as e:
            # on unexpected error, fall back to Error state
            try:
                from states.error import Error
                # preserve exception information if possible
                setattr(e, "code", getattr(e, "code", None))
                self.device.change_state(Error(self.device))
            except Exception:
                # if we cannot transition to Error, re-raise to be handled by Device.run
                raise

    def exit(self):
        # nothing special to do on exit for now
        pass
