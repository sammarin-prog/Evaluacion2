# Evaluacion2 – Software de geolocalización con GraphHopper

Proyecto de la Evaluación Parcial N°2 de la asignatura CUY6142 (Telepresencia y Entornos Innovadores de Colaboración Humana).

El script graphhopper_parse-json.py consulta la API GraphHopper Directions para entregar a los visitantes de la Biblioteca Nacional la ruta entre un punto de origen y un destino. Respecto del prototipo original se incorporaron estas mejoras:

- Todos los textos de interacción con el usuario están en español.
- Distancias y demás valores numéricos se muestran con un máximo de dos decimales.
- El programa termina al ingresar "s" o "salir" en cualquier pregunta.
- La narrativa del viaje (instrucciones paso a paso) se entrega en español (locale=es).

## Requisitos

- Python 3
- Librería requests (pip3 install requests)
- Un token (API key) de GraphHopper: https://graphhopper.com/dashboard/#/apikeys

## Cómo ejecutar

1. Clonar el repositorio:

       git clone https://github.com/sammarin-prog/Evaluacion2.git
       cd Evaluacion2

2. Instalar la dependencia:

       pip3 install requests

3. Ejecutar el script:

       python3 graphhopper_parse-json.py

4. Ingresar el token de GraphHopper cuando lo solicite (o definirlo antes con export GRAPHHOPPER_KEY=su_token).
5. Elegir el perfil de vehículo (auto, bicicleta o a pie), el origen y el destino.
6. Para terminar, escribir "s" o "salir".

## Autor

Samuel Marin