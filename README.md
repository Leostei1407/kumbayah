# Kumbayah - Calendario de Reservas (offline)

Aplicación de escritorio en Python (Tkinter) para el campamento Kumbayah: registrar disponibilidad, crear reservas y ver clientes en días ocupados. Funciona offline usando SQLite.

## 🏗️ **Arquitectura del Proyecto**

El proyecto ha sido completamente refactorizado con una arquitectura modular y componentes reutilizables:

```
kumbayah/
├── main.py                    # Orquestación principal
├── config/                     # Configuración centralizada
│   ├── __init__.py
│   └── app_config.py          # Constantes y configuración
├── utils/                      # Utilidades reutilizables
│   ├── __init__.py
│   └── validators.py           # Lógica de validación
├── ui/                         # Componentes de interfaz gráfica
│   ├── __init__.py
│   ├── styles.py              # Gestión de estilos y temas
│   ├── components.py          # Componentes UI reutilizables
│   ├── calendar_events.py     # Manejo de eventos del calendario
│   ├── calendar_renderer.py   # Renderizado del calendario
│   └── forms.py              # Formularios de la aplicación
└── modules/                    # Lógica de negocio (sin cambios)
    ├── database.py            # Gestión de base de datos SQLite
    ├── clients.py             # CRUD de clientes
    ├── reservations.py        # CRUD de reservas
    └── calendar_logic.py      # Lógica del calendario
```

## 📋 **Requisitos**

- Python 3.8+ (incluye `tkinter` en la mayoría de distribuciones)
- `tkinter` (usualmente incluido con Python)
- `sqlite3` (incluido con Python)

### **Dependencias opcionales:**

- `ttkbootstrap` - Para temas modernos (fallback automático a tkinter estándar)

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## 🚀 **Uso**

### **Ejecutar la aplicación:**

1. Abrir una terminal en la carpeta del proyecto
2. Ejecutar:

```bash
python main.py
```

### **Uso de la interfaz:**

- **Click izquierdo** en un día disponible: abre formulario para registrar cliente
- **Click derecho** en un día (modo staff): alterna disponibilidad
- **Click en día reservado**: muestra detalles y permite editar/eliminar

### **Campos del formulario:**

- **Cliente:** Nombre, Apellido, Teléfono
- **Pago:** Monto, Estado (Completo/Mitad/Nada), Método
- **Referencia:** Requerida para PagoMovil/Transferencia (mínimo 6 dígitos)

## 🎨 **Componentes de la Interfaz**

### **Cabecera del Calendario**

- Navegación entre meses (`<` y `>`)
- Título del mes/año actual

### **Leyenda de Estados**

- 🟩 **Disponible:** Verde claro
- 🟥 **Reservado:** Rosa claro (completo) / Naranja (parcial)
- 🟧 **No disponible:** Gris claro
- ⬜ **Bloqueado:** Gris

### **Celdas de Día**

- **Dimensiones:** 140x110px cada celda
- **Información:** Número del día + nombre del cliente (si aplica)
- **Colores dinámicos** según estado

## 💾 **Persistencia de Datos**

- **Base de datos:** `kumbayah.db` (SQLite)
- **Ubicación:** Carpeta del proyecto
- **Tablas:**
  - `clients`: Información de clientes
  - `reservations`: Datos de reservas con relación a clientes

## 🔧 **Estructura de Componentes**

### **config/app_config.py**

Centraliza todas las constantes:

- Colores y estilos
- Dimensiones de UI
- Textos y mensajes
- Configuración de validación

### **utils/validators.py**

Lógica de validación pura:

- Validación de datos de cliente
- Validación de datos de reserva
- Funciones reutilizables para testing

### **ui/styles.py**

Gestión de estilos:

- Configuración de fuentes
- Gestión de temas
- Colores por estado

### **ui/components.py**

Componentes UI reutilizables:

- `CalendarHeader`: Navegación y título
- `CalendarLegend`: Leyenda de colores
- `CalendarControls`: Controles combinados
- `WeekdayHeader`: Encabezado de días

### **ui/calendar_events.py**

Manejo de eventos:

- `CalendarEventHandler`: Clicks izquierdo/derecho
- `EventCoordinator`: Coordinación entre componentes

### **ui/calendar_renderer.py**

Renderizado visual:

- Dibujado de cuadrícula del calendario
- Actualización dinámica de celdas
- Gestión de layouts responsivos

### **ui/forms.py**

Formularios modales:

- `ReservationForm`: Crear nuevas reservas
- `ReservationDetailsDialog`: Ver/editar/eliminar
- `FormManager`: Coordinador de formularios

## 🧪 **Testing y Validación**

### **Validaciones implementadas:**

- ✅ Nombre y apellido: requeridos
- ✅ Teléfono: solo dígitos
- ✅ Monto: debe ser numérico
- ✅ Referencia: mínimo 6 dígitos (métodos digitales)

### **Manejo de errores:**

- Mensajes claros en español
- Validación en tiempo real
- Fallback graceful para widgets destruidos

## 🔮 **Extensiones Posibles**

El código está diseñado para facilitar extensiones:

- **Exportación:** CSV, PDF de reservas
- **Reportes:** Estadísticas por período
- **Múltiples días:** Reservar varios días consecutivos
- **Notificaciones:** Alertas de reservas próximas
- **Temas:** Personalización completa de colores
- **Internacionalización:** Soporte multiidioma

## 🐛 **Troubleshooting**

### **Problemas comunes:**

- **Import error**: Verificar Python 3.8+ y tkinter instalado
- **Theme error**: Desinstalar ttkbootstrap o asegurar compatibilidad
- **Database locked**: Cerrar otras instancias de la aplicación

### **Desarrollo:**

- **Extensiones**: Agregar nuevos componentes en `ui/`
- **Validaciones**: Extender `validators.py`
- **Estilos**: Modificar `app_config.py`

## 📝 **Notas de Desarrollo**

Este proyecto implementa buenas prácticas:

- **Arquitectura modular**: Separación clara de responsabilidades
- **Inyección de dependencias**: Components desacoplados
- **Single Responsibility**: Cada clase con un propósito claro
- **Configuración externa**: Valores centralizados y modificables
- **Documentación completa**: Código comentado en español
