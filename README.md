# SO De Vesten STEM Robot

Abstractie van de STEM Robot componenten zodat leerlingen snel aan de slag kunnen om hun robot te programmeren met Python.

## Vereisten

### STEM Robot

Dit werkt alleen met deze robots:

TODO: foto toevoegen

| Poort | Sensor
|-------|-------------|
| 1     | Touch       |
| 2     | Gyro        |
| 3     | Kleur/Licht |
| 4     | Ultrasoon   |

| Poort | Motor  |
|-------|--------|
| A     | Medium |
| B     | Groot  |
| C     | Groot  |
| D     | Geen   |

### EV3Dev

Ev3dev is een besturingssysteem voor de Lego EV3 brick gebaseerd op Debian Linux. Dit moet op een SD-kaartje geschreven worden dat in de Robot geplaatst wordt. Volg de instructies op de website van [ev3dev](http://www.ev3dev.org).

### Verbind je laptop met de robot

De makkelijkste manier is werken met bluetooth maar met een usb-kabel lukt het ook. Volg de instructies van [ev3dev](https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-bluetooth/).

### Visual Studio Code

Download [Visual Studio Code](https://code.visualstudio.com/) en configureer dit om met Python en Mindstorms te werken. Volg hiervoor de instructies op [deze pagina](https://github.com/ev3dev/vscode-hello-python) maar in plaats van het vscode-hello-python project te downloaden download je best dit STEM Robot project, dat kan je doen bovenaan deze pagina.

## DeVestenBot.py

Deze klasse bevat een abstractie voor de robot met een aantal nuttige functies die je kan gebruiken in je eigen scripts. Zo kan je de robot laten rijden tot aan een hindernis zonder dat je de afzonderlijke motors en sensors moet bedienen en uitlezen.

Een kort overzicht van de beschikbare functies staat hieronder, voor de details kan je in de klasse kijken of gebruik maken van de tips in VSCode.
