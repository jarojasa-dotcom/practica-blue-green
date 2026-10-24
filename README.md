# Practica Blue/Green

## Objetivo
Demostrar la conmutacion entre dos versiones de una aplicacion
y verificar los endpoints de salud.

## Versiones
- Blue: 1.3.0 (version estable)
- Green: 1.4.0 (nueva version)

## Ejecucion
Iniciar la aplicacion:
python app.py

Activar Green:
./deploy.sh green

Rollback a Blue:
./deploy.sh blue

## Verificaciones
- GET /version
- GET /health
- GET /readiness

## Resultado
Se comprobo la activacion de Green y la recuperacion de Blue
mediante el script de despliegue.

## Limitaciones
Practica de laboratorio con dos backends y un router
ejecutados en un mismo entorno. No representa dos servidores
independientes en produccion.
