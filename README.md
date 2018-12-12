# SO De Vesten STEM Robot

Abstractie van de STEM Robot componenten zodat leerlingen snel aan de slag kunnen om hun robot te programmeren met Python.

## Vereisten

### STEM Robot

Dit werkt alleen met deze robots:

![STEM Robot](.README/STEMRobot.jpg)

| Poort | Sensor
|-------|-------------|
| 1     | Touch       |
| 2     | Gyro        |
| 3     | Kleur/Licht |
| 4     | Ultrasoon   |

| Poort | Motor  |                          |
|:-----:|:-------|:-------------------------|
| A     | Medium | grijper                  |
| B     | Groot  | aandrijving linker wiel  |
| C     | Groot  | aandrijving rechter wiel |
| D     | Geen   |                          |

### EV3Dev

Ev3dev is een besturingssysteem voor de Lego EV3 brick gebaseerd op Debian Linux. Dit moet op een SD-kaartje geschreven worden dat in de Robot geplaatst wordt. Volg de instructies op de website van [ev3dev](http://www.ev3dev.org).

### Verbind je laptop met de robot

De makkelijkste manier is werken met bluetooth maar met een usb-kabel lukt het ook. Volg de instructies van [ev3dev](https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-bluetooth/).

### Visual Studio Code

Download [Visual Studio Code](https://code.visualstudio.com/) en configureer dit om met Python en Mindstorms te werken. Volg hiervoor de instructies op [deze pagina](https://github.com/ev3dev/vscode-hello-python) maar in plaats van het vscode-hello-python project te downloaden download je best dit STEM Robot project, dat kan je doen bovenaan deze pagina.

## DeVestenBot.py

Deze klasse bevat een abstractie voor de robot met een aantal nuttige functies die je kan gebruiken in je eigen scripts. Zo kan je de robot laten rijden tot aan een hindernis zonder dat je de afzonderlijke motors en sensors moet bedienen en uitlezen.

Een kort overzicht van de beschikbare functies staat hieronder, voor de details kan je in de klasse kijken of gebruik maken van de tips in VSCode.

### Rijden

#### rij_centimeters

Laat de robot het gegeven aantal centimeters rijden. Gebruik negatieve getallen om achteruit te rijden.

#### noodstop

Stopt alle huidige beweging van de wielmotors, bv als deze in een andere thread moesten runnen, en remt actief.

### Draaien

#### orienteer

Geef het aantal graden ten opzichte van de beginrichting waarnaar de robot zich moet richten. 

Dit heeft ongeveer dezelfde afwijking
als één keer een van de draai-functies uitvoeren. De afwijking van de draai-functies is cummulatief, gebruik af en toe een oriënteer-
functie om een te grote afwijking te vermijden.

#### orienteer_noord

Oriënteer de robot in dezelfde richting als bij het begin van het programma.

#### orienteer_oost

Oriënteer de robot naar rechts ten opzichte van de beginoriëntatie.

#### orienteer_zuid

Oriënteer de robot tegengesteld ten opzichte van de beginoriëntatie.

#### orienteer_west

Oriënteer de robot naar links ten opzichte van de beginoriëntatie.

#### draai_graden

Geef het aantal graden die de robot moet draaien. Positief is naar rechts draaien, negatief naar links. Let op dat er een afwijking mogelijk is,
bij het meermaals na elkaar gebruiken van een van de draai-functies kan de cummulatieve afwijking groot worden, gebruik een van de oriënteer-functies 
om de afwijking binnen de perken te houden.

#### draai_links

Draai de robot 90° links.

#### draai_rechts

Draai de robot 90° rechts.

#### keer_om

Wat denk je zelf dat dit doet?

### Grijper

#### grijper_open

Zet de grijper omhoog.

#### grijper_sluit

Doe de grijper omlaag.

### Ultrasoon

#### meet_afstand_in_cm

Geeft het aantal centimeter terug gemeten vanaf de ultrasone sensor, als je dit gebruikt om je robot tijdig te laten stoppen hou er dan rekening mee
dat de voorkant van de robot een paar centimeter dichterbij de hindernis is dan de sensor.

### Gyroscoop

#### get_orientatie

Geeft de orientatie van de robot ten opzichte van de beginsituatie in graden.

### Druksensor

TODO

### Kleursensor

TODO

### Output

#### log

Console logging (remote)

TODO

#### Scherm

TODO

#### Geluid

TODO

#### LEDs

TODO