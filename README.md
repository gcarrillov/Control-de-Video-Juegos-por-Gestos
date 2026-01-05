<div align="center">
<table>
    <thead>
        <tr>
            <td style="width:25%; text-align:center;"><img src="/img/epis.png" alt="EPIS" style="width:80%; height:auto"/></td>
            <td style="text-align:center;">
                <span><b>UNIVERSIDAD NACIONAL DE SAN AGUSTIN</b></span><br />
                <span><b>FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS</b></span><br />
                <span><b>DEPARTAMENTO ACADÉMICO DE INGENIERÍA DE SISTEMAS E INFORMÁTICA</b></span><br />
                <span><b>ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS</b></span>
            </td>
            <td style="width:25%; text-align:center;"><img src="/img/abet.png" alt="ABET" style="width:80%; height:auto"/></td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan="3"><span><b>Curso</b></span>: Arquitectura de Computadoras</td>
        </tr>
        <tr>
            <td colspan="3"><span><b>Semestre:</b></span>: 2025 - B</td>
        </tr>
    </tbody>
</table>
</div>
<div align="center" style="margin-top: 10px;">
    <img src="/img/unsa.png" alt="UNSA" width="450px" height="150px">
    <h1 style="font-weight:bold; font-size: 2em;">Implementación de Interfaz Hardware-Software utilizando Webcam y OpenCV</h1>
</div>

## Control de Videojuegos por Gestos
* En una carpeta de drive se guardo tanto el informe como el video, se puede acceder mendiante el siguiente link: [drive](https://drive.google.com/drive/folders/14WTVd9dblIykYkEkugxQqYzscoX7Ju5G?usp=sharing)

### Descripción del proyecto

Este repositorio contiene el Proyecto Final del curso Arquitectura de Computadoras. El sistema implementa una interfaz hardware-software que interconecta el mundo real con el digital mediante control de videojuegos por gestos de mano utilizando una webcam.
Inspirado en el video de Pranav Mistry - SixthSense , el proyecto detecta movimientos de la mano (distancia y pendiente) para simular teclas WASD y controlar juegos simples en Pygame.

##### Caracteristicas principales
* Detección de mano con OpenCV (segmentación por color de piel, contornos, convex hull).
* Simulación de teclas virtuales en Windows (directkeys.py).
* Menú principal con 3 juegos: Snake, Tank Shooter y Carrera Infinita.
* Entrada no convencional: Webcam (gestos) → Salida: Pantalla (juegos interactivos).

### Estructura del Repositorio

* final.py — Script principal de detección de gestos (OpenCV + trackbars).
* control.py — Lógica de mapeo (distancia/slope → WASD).
* directkeys.py — Simulación de teclas en Windows.
* menu.py — Menú unificado para seleccionar juegos.
* img/ — Imágenes para README y portada (epis.png, abet.png, unsa_logo.png, etc.).

#### Instalacion de dependencias

`python -m pip install opencv-python imutils numpy scikit-learn pygame`

#### como ejecutar
1. Activar control por gestos:
    `python final.py`

2. Lanzar menu de juegos:
    `python menu.py`


