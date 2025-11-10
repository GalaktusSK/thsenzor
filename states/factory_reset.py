from .state import AbstractState
import os
import sys
import time

class FactoryReset(AbstractState):
    """FactoryReset state: remove user settings and restart the device.

    Behavior:
    - Attempt to remove persistent settings using device helper if available
      (device.remove_settings()).
    - Otherwise try common attribute names for settings file or fallbacks
      (device.settings_file, SETTINGS_FILE, SETTINGS_PATH).
    - As a last resort try to delete common filenames in the working directory
      (settings.json, config.json, settings.cfg, settings.txt).
    - Clear in-memory device.settings and request restart via sys.exit(0).
    """

    def enter(self):
        # indicate factory reset start (try to set LED to ORANGE if available)
        try:
            if getattr(self.device, "led", None) is not None:
                if hasattr(self.device.led, "set_color"):
                    self.device.led.set_color("ORANGE")
                elif hasattr(self.device.led, "color"):
                    try:
                        self.device.led.color = "ORANGE"
                    except Exception:
                        pass
        except Exception:
            pass

    def exec(self):
        # perform reset actions
        # 1) use device helper if provided
        try:
            remove_fn = getattr(self.device, "remove_settings", None)
            if callable(remove_fn):
                try:
                    remove_fn()
                except Exception:
                    # ignore errors from helper
                    pass
            else:
                # 2) try known attributes on device for settings path
                settings_path = getattr(self.device, "settings_file", None)
                if not settings_path:
                    settings_path = getattr(self.device, "SETTINGS_FILE", None)
                if not settings_path:
                    settings_path = getattr(self.device, "SETTINGS_PATH", None)
                if settings_path:
                    try:
                        if isinstance(settings_path, (list, tuple)):
                            for p in settings_path:
                                try:
                                    os.remove(p)
                                except Exception:
                                    pass
                        else:
                            os.remove(settings_path)
                    except Exception:
                        pass
                else:
                    # 3) fallback: try common filenames
                    for fn in ("settings.json", "config.json", "settings.cfg", "settings.txt"):
                        try:
                            os.remove(fn)
                            # if succeeded, stop trying
                            break
                        except Exception:
                            pass
        except Exception:
            # ensure we do not crash here
            pass

        # 4) clear in-memory settings if present
        try:
            self.device.settings = None
        except Exception:
            pass

        # small delay to allow LED change to be visible
        try:
            time.sleep(0.1)
        except Exception:
            pass

        # 5) request restart via SystemExit -> Device.run will handle it
        try:
            sys.exit(0)
        except SystemExit:
            # re-raise so Device.run sees it
            raise

    def exit(self):
        # nothing to do on exit
        pass
