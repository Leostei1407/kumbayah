"""
Constantes de configuración de la aplicación para Kumbayah Calendar App.

Todos los valores codificados extraídos de main.py para centralización y mantenibilidad.
"""


class AppConfig:
    # Configuración de ventana (línea 15)
    WINDOW_TITLE = 'Kumbayah - Calendario de Reservas (offline)'
    
    # Dimensiones de formulario (líneas 212, 373)
    FORM_DIMENSIONS = {
        'reservation': '420x340',
        'details': '420x340'
    }
    
    # Esquema de colores (líneas 53-56, 125, 133)
    COLORS = {
        'available': '#c8e6c9',           # Verde para días disponibles
        'available_legend': '#dcedc8',     # Verde claro para leyenda
        'reserved_complete': '#ffc0cb',    # Rosa para reservas pagadas completamente
        'reserved_legend': '#ffcdd2',     # Rosa claro para leyenda
        'reserved_partial': '#ffcc80',    # Naranja para reservas pagadas parcialmente
        'partial_legend': '#ffe0b2',      # Naranja claro para leyenda
        'unavailable': '#eeeeee',         # Gris claro para días no disponibles
        'blocked': '#e0e0e0',             # Gris para días bloqueados
        'current_month': '#ffffff',       # Blanco para días del mes actual
        'other_month': '#f5f5f5',         # Gris muy claro para otros meses
        'text_current': '#000000',        # Texto negro para mes actual
        'text_other': '#9e9e9e'          # Texto gris para otros meses
    }
    
    # Dimensiones de celda de calendario (línea 100)
    CELL_SIZE = {
        'width': 140,
        'height': 110
    }
    
    # Configuración de pago (líneas 257, 266, 384, 389)
    PAYMENT_STATUSES = ['Completo', 'Mitad', 'Nada']
    PAYMENT_METHODS = ['PagoMovil', 'Efectivo', 'Transferencia']
    
    # Configuración de UI
    WEEKDAYS = ['Lun','Mar','Mié','Jue','Vie','Sáb','Dom']  # línea 86
    FONT_FAMILY = 'Segoe UI'  # líneas 32-34
    
    # Tamaños de fuente (líneas 32-34)
    FONT_SIZES = {
        'title': 16,
        'day': 14,
        'client': 10
    }
    
    # Configuración de botones de navegación (líneas 39, 43)
    NAV_BUTTONS = {
        'text_prev': '<',
        'text_next': '>',
        'width': 3
    }
    
    # Espaciado y relleno del calendario
    PADDING = {
        'main_frame': (12, 10),
        'controls': (12, 6),
        'cell': (6, 6),
        'legend_item': 4,
        'form_field': (6, 4),
        'button': 6
    }
    
    # Etiquetas de texto y mensajes
    LABELS = {
        'legend_available': 'Disponible',
        'legend_reserved': 'Reservado',
        'legend_partial': 'Parcial/Nada',
        'legend_blocked': 'Bloqueado',
        'availability_hint': 'Marcar disponibilidad (click derecho)',
        'unavailable_msg': 'No disponible',
        'unavailable_detail': 'Este día no está disponible para reservas.',
        
        # Form labels (lines 242, 249, 256, 265, 274, 375)
        'name': 'Nombre',
        'last_name': 'Apellido',
        'phone': 'Teléfono',
        'amount': 'Monto a pagar',
        'payment_status': 'Estado de pago',
        'payment_method': 'Método de pago',
        'reference': 'Referencia (>=6 dígitos)',
        
        # Etiquetas de botones
        'edit': 'Editar',
        'delete': 'Eliminar reserva',
        'close': 'Cerrar',
        'save': 'Guardar',
        'cancel': 'Cancelar',
        
        # Mensajes de error
        'name_required': 'Nombre y apellido son obligatorios.',
        'phone_digits': 'Teléfono debe contener sólo dígitos.',
        'amount_invalid': 'Monto inválido.',
        'reference_length': 'Referencia debe tener al menos 6 dígitos.',
        'confirm_delete': '¿Eliminar esta reserva?',
        
        # Form titles
        'reservation_title_prefix': 'Reservar ',
        'details_title_prefix': 'Reserva '
    }
    
    # Configuración de tema (línea 29)
    THEME_NAME = 'clam'
    
    # Longitud mínima de referencia (líneas 317-320, 428-431)
    MIN_REFERENCE_LENGTH = 6
    
    # Métodos que requieren referencia
    METHODS_REQUIRING_REFERENCE = ['PagoMovil', 'Transferencia']