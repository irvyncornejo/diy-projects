# Ping Pong básico

> Ping-Pong básico para raspberry jam

![Status](https://img.shields.io/badge/status-in--progress-yellow)
![Platform](https://img.shields.io/badge/platform-raspberry-pi-pico-blue)
![Language](https://img.shields.io/badge/language-python-green)

## 📋 Descripción

<!-- Ampliar descripción aquí -->

## 🗂 Estructura

```
ping-pong/
├── project.yml          # Metadata del proyecto
├── README.md
├── CHANGELOG.md
├── code/                # Código fuente
├── hmi/                 # Archivos .HMI (Nextion)
├── docs/                # Documentación
├── assets/
│   ├── images/          # Fotos y capturas
│   ├── schematics/      # Diagramas de circuito
│   └── 3d-files/        # Archivos STL/CAD
└── tests/
```

## 🛒 Bill of Materials

| Qty | Componente | Descripción | Precio | Links |
|-----|-----------|-------------|--------|-------|
| 1 | **Rapsberrypi pico** | Soc | $130 | — |
| 1 | **Neopixel 16*16** |  | $200 | — |
| 2 | **Joytick** |  | $30 | — |
| 1 | **Módulo 7 segmentos** | Módulo contador de 4 segmentos | $0 | — |

## 🚀 Cómo empezar

1. Clona el repositorio
2. Revisa `project.yml` para el listado de componentes
3. Sube el código de `code/` a tu raspberry-pi-pico

## Dependencias usadas
- [TM1637](https://github.com/mcauser/micropython-tm1637)
- [GPIO PICO](https://github.com/irvyncornejo/hardware-lib/tree/main/raspberry-pico/rpi-gpio-pico)

## Circuito
![ping-pong](https://drive.google.com/uc?export=view&id=1oGVBbBDUQTjw6hEn6nSU2g4db0po56et)

---
*Generado con new-diy-project.sh v2.1 — 2026-06-14*
