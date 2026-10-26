# Análisis de Señales en el Dominio del Tiempo y Frecuencia usando la Transformada de Fourier

Este proyecto realiza la simulación y análisis de señales elementales en los dominios del tiempo y la frecuencia mediante la **Transformada Rápida de Fourier (FFT)**, empleando **Python** (`NumPy` y `Matplotlib`). Adicionalmente, se verifica cuantitativa y gráficamente el impacto de las propiedades fundamentales de la Transformada de Fourier sobre el espectro de frecuencia.

---

## 🚀 Requisitos e Instalación

Para ejecutar este código en un entorno basado en Linux/Ubuntu o WSL, instala las librerías necesarias mediante la terminal:

```bash
sudo apt update
sudo apt install -y python3-numpy python3-matplotlib


## Estructura del Repositorio
ActF2-SyS-Fourier/
├── ActF2-Fourier.py     # Script principal en Python
├── README.md            # Documentación del proyecto
└── graphics/            # Gráficas generadas automáticamente
    ├── pulso_rectangular.png
    ├── escalon_unitario.png
    ├── senoidal_50hz.png
    ├── linealidad.png
    ├── desplazamiento_temporal.png
    └── escalamiento.png