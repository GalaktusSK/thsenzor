"""device.py

Device state machine controller. Ensures SystemExit is handled so MicroPython/Pico
doesn't do a soft reset when a state requests a restart/exit via sys.exit().
"""

import time

class Device:
    def __init__(self):
        # základné členy, inicializované na None
        self.state = None
        self.settings = None
        # miesto pre senzory / akčné členy
        self.dht_sensor = None
        self.led = None
        # chybový kód podľa požiadavky (krok 8.1)
        self.error_code = None

        # inicializujeme miesto pre prvý stav
        # import tu, aby sa predišlo cyklickému importu pri importovaní modulu states
        from states.init import Init
        self.state = Init(self)

    def change_state(self, new_state):
        """
        new_state: inštancia AbstractState
        Volá exit() na starom stave (ak existuje) a nastaví nový stav.
        (enter() sa volá až v run() pred exec()).
        """
        try:
            if self.state is not None:
                # pokus o korektné opustenie starého stavu
                try:
                    self.state.exit()
                except Exception:
                    # ignore exceptions during exit to avoid crash during prechodu
                    pass
        finally:
            self.state = new_state

    def run(self):
        """
        Nekonečná slučka stavového stroja:
        - pre každý cyklus zavolá enter(), exec(), exit()
        - ošetruje SystemExit aby predišlo mäkkému resetu zariadenia
        - pri neočakávanej chybe prejde do Error stavu (ak dostupný)

        Dôležité: SystemExit je používaný stavmi na signál "restart/ukonči".
        Táto metóda ho zachytí a korektne ukončí run slučku bez opätovného reštartu
        (čo by na MicroPythone/mali by vyvolať soft reset).
        """
        while True:
            try:
                if self.state is None:
                    # nič na vykonanie
                    break

                # vstup do stavu
                try:
                    self.state.enter()
                except Exception as e:
                    # logovanie / ignorovanie chýb v enter
                    print("Warning: exception in state.enter():", e)

                # hlavné správanie
                self.state.exec()

                # opustenie stavu
                try:
                    self.state.exit()
                except Exception as e:
                    print("Warning: exception in state.exit():", e)

            except SystemExit:
                # očakávané ukončenie -> skončíme run bez rebootu
                print("Device: SystemExit caught, stopping run loop.")
                break
            except Exception as exc:
                # Neočakávaná chyba: prepnúť do Error stavu ak je k dispozícii
                print("Unhandled exception in Device.run():", exc)
                try:
                    from states.error import Error
                    # uložíme chybový kód ak ho výnimka nesie
                    self.error_code = getattr(exc, "code", None)
                    self.change_state(Error(self))
                except Exception as e:
                    print("Cannot switch to Error state:", e)
                    # ak ani to nie je možné -> prerušíme slučku
                    break

            # malé zdržanie, aby sa slučka nezabudla (a aby sa dal prerušiť)
            # na MicroPythone by ste použili time.sleep_ms(...)
            time.sleep(0.1)
