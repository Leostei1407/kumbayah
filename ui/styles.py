"""
Gestión de estilos para Kumbayah Calendar App.

Extraído de main.py líneas 26-35 para centralizar toda la lógica de estilo de UI.
Maneja fuentes, colores, temas y configuración ttk.
"""
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from config.app_config import AppConfig


class StyleManager:
    """
    Gestiona todo el estilo de UI para la aplicación.
    
    Configuración centralizada para:
    - Configuración de tema (fallback ttkbootstrap)
    - Configuración de fuentes
    - Gestión de colores
    """
    
    def __init__(self):
        """Inicializar gestor de estilos y configurar tema."""
        self.style = ttk.Style()
        self._setup_theme()
        self.fonts = self._create_fonts()
    
    def _setup_theme(self):
        """
        Configurar el tema de la aplicación.
        
        Intenta usar tema 'clam', con fallback al predeterminado.
        ttkbootstrap se maneja a nivel de aplicación en main.py.
        
        Extraído de líneas 28-31
        """
        try:
            self.style.theme_use(AppConfig.THEME_NAME)
        except Exception:
            # Fallback al tema predeterminado si 'clam' no está disponible
            pass
    
    def _create_fonts(self):
        """
        Crear y devolver todas las fuentes de la aplicación.
        
        Returns:
            dict: Diccionario que contiene todas las fuentes configuradas
            
        Extraído de líneas 32-34
        """
        fonts = {
            'title': tkfont.Font(
                family=AppConfig.FONT_FAMILY, 
                size=AppConfig.FONT_SIZES['title'], 
                weight='bold'
            ),
            'day': tkfont.Font(
                family=AppConfig.FONT_FAMILY, 
                size=AppConfig.FONT_SIZES['day'], 
                weight='bold'
            ),
            'client': tkfont.Font(
                family=AppConfig.FONT_FAMILY, 
                size=AppConfig.FONT_SIZES['client']
            )
        }
        return fonts
    
    def get_font(self, font_type):
        """
        Obtener una fuente específica por tipo.
        
        Args:
            font_type (str): Tipo de fuente ('title', 'day', 'client')
            
        Returns:
            tkfont.Font: La fuente solicitada
            
        Raises:
            KeyError: Si font_type no es reconocido
        """
        if font_type not in self.fonts:
            raise KeyError(f"Tipo de fuente '{font_type}' no encontrado. Disponibles: {list(self.fonts.keys())}")
        return self.fonts[font_type]
    
    def get_all_fonts(self):
        """
        Obtener todas las fuentes configuradas.
        
        Returns:
            dict: Diccionario con todas las fuentes
        """
        return self.fonts
    
    def get_color(self, color_name):
        """
        Obtener un color por nombre desde la configuración.
        
        Args:
            color_name (str): Nombre del color
            
        Returns:
            str: Código de color hex
            
        Raises:
            KeyError: Si color_name no se encuentra
        """
        if color_name not in AppConfig.COLORS:
            raise KeyError(f"Color '{color_name}' no encontrado en configuración.")
        return AppConfig.COLORS[color_name]
    
    def get_color_for_status(self, reservation_status=None, is_available=True, is_current_month=True):
        """
        Obtener el color apropiado basado en el estado del día.
        
        Args:
            reservation_status (str): Estado de pago ('Completo', 'Mitad', 'Nada')
            is_available (bool): Si el día está disponible
            is_current_month (bool): Si el día está en el mes actual
            
        Returns:
            str: Código de color hex para el fondo de la celda
        """
        if not is_current_month:
            return AppConfig.COLORS['other_month']
            
        if reservation_status:
            if reservation_status == 'Completo':
                return AppConfig.COLORS['reserved_complete']
            else:
                return AppConfig.COLORS['reserved_partial']
        elif not is_available:
            return AppConfig.COLORS['unavailable']
        else:
            return AppConfig.COLORS['available']
    
    def get_text_color(self, is_current_month=True):
        """
        Obtener color de texto basado en el contexto del mes.
        
        Args:
            is_current_month (bool): Si el día está en el mes actual
            
        Returns:
            str: Código de color hex para texto
        """
        return AppConfig.COLORS['text_current'] if is_current_month else AppConfig.COLORS['text_other']