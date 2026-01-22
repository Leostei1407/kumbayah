# Kumbayah - Calendario de Reservas (offline)

Aplicación de escritorio en Python (Tkinter) para que el campamento Kumbayah: registrar disponibilidad, crear reservas y ver clientes en días ocupados. Funciona offline usando SQLite.

Requisitos
- Python 3.8+ (incluye `tkinter` en la mayoría de distribuciones de Windows)

Archivos principales
- `main.py`: Interfaz gráfica y lógica principal.
- `db.py`: Helper SQLite para `bookings` y `availability`.

Uso
1. Abrir una terminal en la carpeta del proyecto.
2. Ejecutar:

```bash
python main.py
```

Cómo funciona
- Click izquierdo en un día disponible: abre formulario para registrar cliente (nombre, apellido, teléfono, monto, estado de pago, método).
- Si el método es `PagoMovil` o `Transferencia`, se pide una referencia de al menos 6 dígitos.
- Click derecho en un día (modo staff): alterna disponibilidad (disponible / no disponible).
- Días ocupados muestran el nombre del cliente; al hacer click se puede ver y eliminar la reserva.

Persistencia
- Los datos se guardan en `kumbayah.db` (SQLite) en la carpeta del proyecto.

Notas
- Esta es una implementación inicial. Si quieres mejoras (exportar a CSV, impresión, multiple días por reserva, UI más bonita), dime y lo amplío.
