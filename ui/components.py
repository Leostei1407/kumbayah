"""
Componentes de UI reutilizables para Kumbayah Calendar App.

Extraído de main.py líneas 36-57 para crear componentes modulares y reutilizables.
Incluye componentes CalendarHeader y CalendarLegend.
"""
import tkinter as tk
from tkinter import ttk
from config.app_config import AppConfig


class CalendarHeader:
    """
    Componente de encabezado con controles de navegación y visualización de título del mes.
    
    Extraído de main.py líneas 36-44.
    Maneja navegación de meses y visualización de título.
    """
    
    def __init__(self, parent, font_title, on_prev_month, on_next_month):
        """
        Inicializar encabezado de calendario.
        
        Args:
            parent: Widget padre (tk.Frame)
            font_title: Fuente para etiqueta de título
            on_prev_month: Callback para botón de mes anterior
            on_next_month: Callback para botón de mes siguiente
        """
        self.parent = parent
        self.font_title = font_title
        self.on_prev_month = on_prev_month
        self.on_next_month = on_next_month
        
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill='x', padx=AppConfig.PADDING['main_frame'][0], 
                        pady=AppConfig.PADDING['main_frame'][1])
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crear widgets de navegación del encabezado."""
        # Botón de mes anterior
        prev_btn = ttk.Button(
            self.frame, 
            text=AppConfig.NAV_BUTTONS['text_prev'],
            width=AppConfig.NAV_BUTTONS['width'],
            command=self.on_prev_month
        )
        prev_btn.grid(row=0, column=0)
        
        # Etiqueta de título de Mes/Año
        self.title_label = ttk.Label(
            self.frame, 
            text='', 
            font=self.font_title
        )
        self.title_label.grid(row=0, column=1, padx=AppConfig.PADDING['legend_item'] * 3)
        
        # Botón de mes siguiente
        next_btn = ttk.Button(
            self.frame,
            text=AppConfig.NAV_BUTTONS['text_next'],
            width=AppConfig.NAV_BUTTONS['width'],
            command=self.on_next_month
        )
        next_btn.grid(row=0, column=2)
    
    def update_title(self, text):
        """
        Actualizar el texto de la etiqueta de título.
        
        Args:
            text (str): Nuevo texto de título
        """
        self.title_label.config(text=text)
    
    def get_title_label(self):
        """
        Obtener referencia al widget de etiqueta de título.
        
        Returns:
            ttk.Label: Widget de etiqueta de título
        """
        return self.title_label


class CalendarLegend:
    """
    Componente de leyenda mostrando significados de colores para estados del calendario.
    
    Extraído de main.py líneas 46-57.
    Muestra colores disponibles y sus significados.
    """
    
    def __init__(self, parent):
        """
        Inicializar leyenda del calendario.
        
        Args:
            parent: Widget padre (tk.Frame o similar)
        """
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crear indicadores de color y etiquetas de la leyenda."""
        legend = ttk.Frame(self.frame)
        
        # Elementos de leyenda con colores y etiquetas
        legend_items = [
            (AppConfig.COLORS['available_legend'], AppConfig.LABELS['legend_available']),
            (AppConfig.COLORS['reserved_legend'], AppConfig.LABELS['legend_reserved']),
            (AppConfig.COLORS['partial_legend'], AppConfig.LABELS['legend_partial']),
            (AppConfig.COLORS['blocked'], AppConfig.LABELS['legend_blocked'])
        ]
        
        for i, (color, text) in enumerate(legend_items):
            label = ttk.Label(legend, text=text, background=color)
            label.grid(row=0, column=i, padx=AppConfig.PADDING['legend_item'])
        
        legend.pack()
    
    def pack(self, **kwargs):
        """Empaquetar el frame de leyenda con opciones dadas."""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Colocar en grid el frame de leyenda con opciones dadas."""
        self.frame.grid(**kwargs)


class CalendarControls:
    """
    Frame de controles que contiene leyenda y sugerencia de disponibilidad.
    
    Extraído y mejorado de main.py líneas 46-48 y 51-57.
    Combina el botón de sugerencia y leyenda en un solo frame.
    """
    
    def __init__(self, parent):
        """
        Inicializar controles del calendario.
        
        Args:
            parent: Widget padre (tk.Frame)
        """
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self._create_widgets()
    
    def _create_widgets(self):
        """Crear controles con botón de sugerencia y leyenda."""
        # Botón de sugerencia de disponibilidad (deshabilitado, solo visual)
        hint_btn = ttk.Button(
            self.frame, 
            text=AppConfig.LABELS['availability_hint'],
            command=lambda: None
        )
        hint_btn.grid(row=0, column=0)
        
        # Leyenda
        legend = CalendarLegend(self.frame)
        legend.grid(row=0, column=1, padx=AppConfig.PADDING['legend_item'] * 2)
    
    def pack(self, **kwargs):
        """Empaquetar el frame de controles."""
        self.frame.pack(**kwargs)


class WeekdayHeader:
    """
    Componente de encabezado mostrando nombres de días de la semana.
    
    Extraído de main.py líneas 86-88.
    Crea el encabezado de Lunes a Domingo para la cuadrícula del calendario.
    """
    
    def __init__(self, parent):
        """
        Inicializar encabezado de días de la semana.
        
        Args:
            parent: Widget padre (tk.Frame donde se mostrará el calendario)
        """
        self.parent = parent
        self._create_widgets()
    
    def _create_widgets(self):
        """Crear widgets de etiquetas de días de la semana."""
        for i, day_name in enumerate(AppConfig.WEEKDAYS):
            label = ttk.Label(self.parent, text=day_name)
            label.grid(row=0, column=i, padx=AppConfig.PADDING['form_field'][0], 
                      pady=AppConfig.PADDING['form_field'][1])