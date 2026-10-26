import os
import numpy as np
import matplotlib.pyplot as plt

# =========================================================================
# ANÁLISIS DE SEÑALES EN EL DOMINIO DEL TIEMPO Y FRECUENCIA (FFT)
# =========================================================================

# Crear carpeta para guardar gráficas si no existe
carpeta_destino = os.path.join(os.getcwd(), 'graphics')
if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

# -------------------------------------------------------------------------
# CONFIGURACIÓN INICIAL DE MUESTREO
# -------------------------------------------------------------------------
Fs = 1000               # Frecuencia de muestreo (Hz)
T = 1 / Fs              # Período de muestreo (s)
L = 2000                # Número de puntos (duración de 2 segundos)
t = np.arange(-L/2, L/2) * T  # Vector de tiempo centrado en 0

# Vector de frecuencias centradas para la visualización espectral
freqs = np.arange(-L/2, L/2) * (Fs / L)

# -------------------------------------------------------------------------
# FUNCIÓN AUXILIAR PARA CÁLCULO DE FFT
# -------------------------------------------------------------------------
def calcular_fft(signal, L):
    """Calcula la FFT centrada y normalizada de una señal."""
    fft_vals = np.fft.fftshift(np.fft.fft(signal)) / L
    mag = np.abs(fft_vals)
    fase = np.angle(fft_vals)
    
    # Filtrar ruido numérico en la fase cuando la magnitud es casi cero
    fase[mag < 1e-5] = 0
    return mag, fase

# -------------------------------------------------------------------------
# 1. GENERACIÓN DE SEÑALES ELEMENTALES
# -------------------------------------------------------------------------
# A) Pulso Rectangular (Ancho de 0.2 s)
pulso_rect = np.where(np.abs(t) <= 0.1, 1.0, 0.0)

# B) Escalón Unitario
escalon = np.where(t >= 0, 1.0, 0.0)

# C) Senoidal (50 Hz)
f_seno = 50
senoidal = np.sin(2 * np.pi * f_seno * t)

senales = [
    ('Pulso Rectangular', pulso_rect, 'pulso_rectangular'),
    ('Escalón Unitario', escalon, 'escalon_unitario'),
    ('Senoidal (50 Hz)', senoidal, 'senoidal_50hz')
]

# Loop para calcular FFT y graficar cada señal
for nombre, s, filename in senales:
    mag, fase = calcular_fft(s, L)
    
    fig, axs = plt.subplots(3, 1, figsize=(8, 6))
    fig.suptitle(f'Análisis de Fourier: {nombre}', fontsize=12, fontweight='bold')
    
    # Dominio del tiempo
    axs[0].plot(t, s, 'b', linewidth=1.5)
    axs[0].set_title('Dominio del Tiempo')
    axs[0].set_xlabel('Tiempo [s]')
    axs[0].set_ylabel('Amplitud')
    axs[0].grid(True)
    axs[0].set_xlim([-1, 1])
    
    # Magnitud en Frecuencia
    axs[1].plot(freqs, mag, 'r', linewidth=1.5)
    axs[1].set_title('Espectro de Magnitud |X(f)|')
    axs[1].set_xlabel('Frecuencia [Hz]')
    axs[1].set_ylabel('Magnitud')
    axs[1].grid(True)
    axs[1].set_xlim([-100, 100])
    
    # Fase en Frecuencia
    axs[2].plot(freqs, fase, 'g', linewidth=1.5)
    axs[2].set_title(r'Espectro de Fase $\angle X(f)$')
    axs[2].set_xlabel('Frecuencia [Hz]')
    axs[2].set_ylabel('Fase [rad]')
    axs[2].grid(True)
    axs[2].set_xlim([-100, 100])
    
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_destino, f'{filename}.png'))
    plt.close()

# -------------------------------------------------------------------------
# 2. VERIFICACIÓN DE PROPIEDADES DE LA TRANSFORMADA DE FOURIER
# -------------------------------------------------------------------------

# --- A) Propiedad de Linealidad: F[a*x1 + b*x2] = a*F[x1] + b*F[x2] ---
a = 2.0
b = 0.5
x1 = np.sin(2 * np.pi * 30 * t)
x2 = np.sin(2 * np.pi * 70 * t)

x_comb = a * x1 + b * x2
mag_comb, _ = calcular_fft(x_comb, L)

mag_x1, _ = calcular_fft(x1, L)
mag_x2, _ = calcular_fft(x2, L)
mag_teorica = a * mag_x1 + b * mag_x2

plt.figure(figsize=(8, 4))
plt.plot(freqs, mag_comb, 'm', linewidth=2, label=r'FFT($a \cdot x_1 + b \cdot x_2$)')
plt.plot(freqs, mag_teorica, 'k--', linewidth=1.5, label=r'$a \cdot$FFT($x_1$) + $b \cdot$FFT($x_2$)')
plt.title('Propiedad de Linealidad')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Magnitud')
plt.xlim([-100, 100])
plt.grid(True)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig(os.path.join(carpeta_destino, 'linealidad.png'))
plt.close()

# --- B) Desplazamiento Temporal: x(t - t0) ---
t0 = 0.2
pulso_desp = np.where(np.abs(t - t0) <= 0.1, 1.0, 0.0)

mag_orig, fase_orig = calcular_fft(pulso_rect, L)
mag_desp, fase_desp = calcular_fft(pulso_desp, L)

fig, axs = plt.subplots(2, 1, figsize=(8, 5))

axs[0].plot(freqs, mag_orig, 'b', linewidth=1.5, label='Original')
axs[0].plot(freqs, mag_desp, 'r--', linewidth=1.5, label=r'Desplazada ($t_0 = 0.2s$)')
axs[0].set_title('Desplazamiento Temporal: Conservación de Magnitud')
axs[0].set_xlim([-50, 50])
axs[0].grid(True)
axs[0].legend()

axs[1].plot(freqs, fase_orig, 'b', linewidth=1.5, label='Fase Original')
axs[1].plot(freqs, fase_desp, 'r', linewidth=1.5, label='Fase Desplazada')
axs[1].set_title('Desplazamiento Temporal: Variación en la Fase')
axs[1].set_xlim([-50, 50])
axs[1].grid(True)
axs[1].legend()

plt.tight_layout()
plt.savefig(os.path.join(carpeta_destino, 'desplazamiento_temporal.png'))
plt.close()

# --- C) Escalamiento Temporal vs Frecuencial ---
pulso_comp = np.where(np.abs(2 * t) <= 0.1, 1.0, 0.0)
mag_comp, _ = calcular_fft(pulso_comp, L)

plt.figure(figsize=(8, 4))
plt.plot(freqs, mag_orig, 'b', linewidth=1.5, label='Pulso Ancho (Tiempo)')
plt.plot(freqs, mag_comp, 'g', linewidth=1.5, label='Pulso Angosto (Compresión Temporal)')
plt.title('Propiedad de Escalamiento (Compresión Temporal = Expansión Frecuencial)')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Magnitud')
plt.xlim([-100, 100])
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(carpeta_destino, 'escalamiento.png'))
plt.close()

print('¡Simulación completada! Las gráficas se guardaron en la carpeta "graphics".')