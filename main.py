"""
Kumbayah - Calendario de Reservas (offline)

Aplicación principal refactorizada usando componentes extraídos para mejor modularidad y mantenibilidad.
Funcionalidad original preservada mientras se extraen componentes reutilizables.
"""
import tkinter as tk
from tkinter import ttk
from config.app_config import AppConfig
from modules.database import Database
from modules.clients import Clients
from modules.reservations import Reservations
from modules.calendar_logic import CalendarLogic
from ui.styles import StyleManager
from ui.components import CalendarHeader, CalendarControls
from ui.calendar_renderer import CalendarRenderer
from ui.calendar_events import EventCoordinator
from ui.forms import FormManager


class CalendarApp:
    """
    Clase de aplicación principal para Kumbayah Calendar.
    
    Ahora sirve como orquestador que coordina entre diferentes componentes,
    en lugar de contener toda la lógica de UI directamente.
    """
    
    def __init__(self, root):
        """Inicializar aplicación de calendario."""
        self.root = root
        self.root.title(AppConfig.WINDOW_TITLE)
        
        # Inicializar base de datos y gestores
        self._setup_database()
        
        # Inicializar componentes de UI primero
        self._setup_ui_components()
        
        # Luego inicializar coordinadores que dependen de componentes de UI
        self._setup_coordinators()
        
        # Configurar manejador de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def _setup_database(self):
        """Inicializar base de datos y gestores relacionados."""
        self.db_manager = Database('kumbayah.db')
        self.db_manager.create_tables()
        db_conn = self.db_manager.connect()
        
        self.clients_manager = Clients(db_conn)
        self.reservations_manager = Reservations(db_conn)
        self.calendar_logic = CalendarLogic(
            self.db_manager, 
            self.clients_manager, 
            self.reservations_manager
        )
    
    def _setup_ui_components(self):
        """Inicializar todos los componentes de UI."""
        # Configurar estilos y fuentes
        self.style_manager = StyleManager()
        
        # Crear estructura principal de UI
        self._create_main_layout()
    
    def _create_main_layout(self):
        """Crear diseño principal de la aplicación."""
        # Encabezado de calendario con navegación
        self.header = CalendarHeader(
            parent=self.root,
            font_title=self.style_manager.get_font('title'),
            on_prev_month=self._on_prev_month,
            on_next_month=self._on_next_month
        )
        
        # Frame de controles con leyenda
        controls = CalendarControls(self.root)
        controls.pack(fill='x', padx=AppConfig.PADDING['controls'][0], 
                    pady=AppConfig.PADDING['controls'][1])
        
        # Frame de calendario para celdas de día
        self.calendar_frame = ttk.Frame(self.root)
        self.calendar_frame.pack(padx=AppConfig.PADDING['main_frame'][0], 
                              pady=AppConfig.PADDING['main_frame'][1])
    
    def _setup_coordinators(self):
        """Inicializar coordinadores que gestionan interacciones entre componentes."""
        # Inicializar renderizador de calendario con manejador de eventos
        self.calendar_renderer = CalendarRenderer(
            calendar_frame=self.calendar_frame,
            title_label=self.header.get_title_label(),
            style_manager=self.style_manager,
            calendar_logic=self.calendar_logic,
            event_handler=None  # Se establecerá después de la creación del coordinador de eventos
        )
        
        # Gestor de formularios para manejar formularios
        self.form_manager = FormManager(
            parent=self.root,
            style_manager=self.style_manager,
            calendar_logic=self.calendar_logic,
            calendar_renderer=self.calendar_renderer
        )
        
        # Coordinador de eventos para manejar interacciones del usuario
        self.event_coordinator = EventCoordinator(
            calendar_logic=self.calendar_logic,
            calendar_renderer=self.calendar_renderer,
            form_manager=self.form_manager
        )
        
        # Conectar manejador de eventos al renderizador
        self.calendar_renderer.event_handler = self.event_coordinator.get_event_handler()
        
        # Dibujar calendario inicial
        self.calendar_renderer.draw_calendar()
    
    def _on_prev_month(self):
        """Manejar navegación de mes anterior."""
        self.event_coordinator.handle_month_navigation('prev')
    
    def _on_next_month(self):
        """Manejar navegación de mes siguiente."""
        self.event_coordinator.handle_month_navigation('next')
    
    def on_closing(self):
        """Manejar cierre de aplicación."""
        self.db_manager.close()
        self.root.destroy()


def main():
    """Punto de entrada principal para la aplicación."""
    try:
        # Intentar usar ttkbootstrap si está disponible
        from ttkbootstrap import Style
        style = Style('flatly')
        root = style.master
    except Exception:
        # Fallback a tkinter estándar
        root = tk.Tk()
    
    app = CalendarApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()