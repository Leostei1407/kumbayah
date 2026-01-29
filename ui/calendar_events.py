"""
Manejo de eventos de calendario para Kumbayah Calendar App.

Extraído de main.py líneas 185-206 para centralizar la lógica de interacción del usuario.
Maneja eventos de clic, alternancia de disponibilidad e interacciones de día.
"""
from tkinter import messagebox
from config.app_config import AppConfig


class CalendarEventHandler:
    """
    Maneja todas las interacciones del usuario relacionadas con el calendario.
    
    Gestiona eventos de clic izquierdo y derecho en los días del calendario,
    delega a manejadores apropiados y coordina con otros componentes.
    
    Extraído de main.py líneas 185-206.
    """
    
    def __init__(self, calendar_logic, update_cell_callback, show_details_callback, open_form_callback):
        """
        Inicializar manejador de eventos de calendario.
        
        Args:
            calendar_logic: Instancia de CalendarLogic para lógica de negocio
            update_cell_callback: Función para actualizar celda de día específica
            show_details_callback: Función para mostrar diálogo de detalles de reserva
            open_form_callback: Función para abrir formulario de reserva
        """
        self.calendar_logic = calendar_logic
        self.update_cell_callback = update_cell_callback
        self.show_details_callback = show_details_callback
        self.open_form_callback = open_form_callback
    
    def toggle_availability(self, day):
        """
        Manejar evento de clic derecho para alternar disponibilidad del día.
        
        Args:
            day (datetime.date): Día para alternar disponibilidad
            
        Extraído de main.py líneas 185-190
        """
        current_month, _ = self.calendar_logic.get_current_month_year()
        
        # Solo permitir alternar disponibilidad para días del mes actual
        if day.month != current_month:
            return
            
        # Alternar disponibilidad usando lógica de calendario
        self.calendar_logic.toggle_day_availability(day)
        
        # Actualizar la celda para reflejar el cambio
        self.update_cell_callback(day)
    
    def on_day_click(self, day):
        """
        Manejar evento de clic izquierdo en día del calendario.
        
        Muestra detalles de reserva para días reservados,
        abre formulario para días disponibles o muestra mensaje de no disponible.
        
        Args:
            day (datetime.date): Día clickeado
            
        Extraído de main.py líneas 192-206
        """
        current_month, _ = self.calendar_logic.get_current_month_year()
        
        # Solo manejar clics para días del mes actual
        if day.month != current_month:
            return
        
        # Obtener información de estado del día
        day_info = self.calendar_logic.get_day_status(day)
        reservation = day_info['reservation']
        is_available = day_info['is_available']
        
        # Determinar acción apropiada basada en el estado del día
        if reservation:
            # Mostrar detalles de reserva si existe
            self.show_details_callback(reservation)
        elif not is_available:
            # Mostrar mensaje de no disponible
            messagebox.showinfo(
                AppConfig.LABELS['unavailable'], 
                AppConfig.LABELS['unavailable_detail']
            )
        else:
            # Abrir formulario de reserva para días disponibles
            self.open_form_callback(day_info['date_str'])
    
    def create_day_cell_bindings(self, canvas, day):
        """
        Crear enlaces de eventos de clic para celda de día del canvas.
        
        Args:
            canvas: Widget canvas al que enlazar eventos
            day (datetime.date): Día asociado con el canvas
            
        Returns:
            tuple: (enlace_clic_izquierdo, enlace_clic_derecho)
        """
        def _on_left_click(event):
            self.on_day_click(day)
            
        def _on_right_click(event):
            self.toggle_availability(day)
        
        # Enlazar los eventos
        canvas.bind('<Button-1>', _on_left_click)
        canvas.bind('<Button-3>', _on_right_click)
        
        return _on_left_click, _on_right_click


class EventCoordinator:
    """
    Coordina entre diferentes componentes de UI y manejadores de eventos.
    
    Actúa como un hub central para manejo de eventos, asegurando comunicación
    adecuada entre eventos del calendario y componentes de UI.
    """
    
    def __init__(self, calendar_logic, calendar_renderer, form_manager):
        """
        Inicializar coordinador de eventos.
        
        Args:
            calendar_logic: Instancia de lógica de negocio
            calendar_renderer: Componente de renderizado de calendario
            form_manager: Componente de gestión de formularios
        """
        self.calendar_logic = calendar_logic
        self.calendar_renderer = calendar_renderer
        self.form_manager = form_manager
        
        # Crear manejador de eventos con callbacks apropiados
        self.event_handler = CalendarEventHandler(
            calendar_logic=calendar_logic,
            update_cell_callback=calendar_renderer.update_cell,
            show_details_callback=form_manager.show_reservation_details,
            open_form_callback=form_manager.open_reservation_form
        )
    
    def get_event_handler(self):
        """
        Obtener la instancia del manejador de eventos de calendario.
        
        Returns:
            CalendarEventHandler: Manejador de eventos para interacciones del calendario
        """
        return self.event_handler
    
    def handle_month_navigation(self, direction):
        """
        Manejar eventos de navegación de mes.
        
        Args:
            direction (str): 'prev' o 'next'
        """
        if direction == 'prev':
            self.calendar_logic.prev_month()
        elif direction == 'next':
            self.calendar_logic.next_month()
        
        # Redibujar calendario con nuevo mes
        self.calendar_renderer.draw_calendar()
    
    def handle_day_selection(self, day):
        """
        Manejar evento de selección de día.
        
        Args:
            day (datetime.date): Día seleccionado
        """
        self.event_handler.on_day_click(day)
    
    def handle_availability_toggle(self, day):
        """
        Manejar evento de alternancia de disponibilidad.
        
        Args:
            day (datetime.date): Día a alternar
        """
        self.event_handler.toggle_availability(day)