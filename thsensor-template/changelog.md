# Changelog

## 27.okt.2025 (v2025.3)

* `constants.py`
  * pridaná konštanta pre nastavenie pracovnej frekvencie MCU
  * pridany GPIO pin pre alarm signal z externeho RTC modulu 
* `settings.py`
  * pridany interval merania
* `decorators.py`
  * vytvoreny dektorator `@singleton` pre oznacenie triedy
* `udataclasses.py`
  * korektne sa dumpne aj zoznam
* `models/mixins.py`
  * pridane mixiny pre RTC modul
* priecinok `www/`
  * premenovany z `webapp/` (je to cistejsie)
  * pridany modul `routes.py` s cestami `/` a cestou pre staticke subory
  * vytvorene priecinky `static/` a `templates/`
* ostatne
  * pridany prazdny subor `boot.py`

## 15.okt.2025 (v2025.2)

* pridaný prázdny súbor `boot.py`
* pridaná jednoduchá podoba súboru `main.py`
* `constants.py`
  * pridané konštanty pre zbernicu _I2C_ - `I2C_SCL_PIN` a `I2C_SDA_PIN`
  * odstránené predvolené heslo pre admin WiFi sieť
* model `Settings`
  * pridaná premenná `admin_password` pre admin WiFi sieť
* vytvorené nové modely
  * `Payload` a `Metric` - pre publikovanie nameraných dát
  * `Command` - pre príjem príkazov


## 14.okt.2025 (v2025.1)

* prvá verzia
