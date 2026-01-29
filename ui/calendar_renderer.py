"""
Componente de renderizado de calendario para Kumbayah Calendar App.

Extraído de main.py líneas 78-183 para separar lógica de renderizado de UI.
Maneja visualización del calendario, creación de celdas y actualizaciones dinámicas.
"""
import tkinter as tk
import calendar
from ui.components import WeekdayHeader
from config.app_config import AppConfig


class CalendarRenderer:
    """
    Maneja el renderizado visual del calendario.
    
    Responsable de:
    - Dibujar la cuadrícula completa del calendario
    - Crear celdas individuales de día
    - Actualizar celdas individuales cuando cambian los datos
    - Gestionar diseño y estilo de celdas
    
    Extraído de main.py líneas 78-183.
    """
    
    def __init__(self, calendar_frame, title_label, style_manager, calendar_logic, event_handler=None):
        """
        Inicializar renderizador de calendario.
        
        Args:
            calendar_frame: Widget frame donde se renderizará el calendario
            title_label: Widget label para título de mes/año
            style_manager: Instancia de StyleManager para fuentes y colores
            calendar_logic: Instancia de CalendarLogic para datos
            event_handler: Instancia de EventHandler para interacciones del usuario (opcional)
        """
        self.calendar_frame = calendar_frame
        self.title_label = title_label
        self.style_manager = style_manager
        self.calendar_logic = calendar_logic
        self.event_handler = event_handler
        
        self.day_buttons = []  # Store references to all day cells
        
        # Get fonts from style manager
        self.font_day = style_manager.get_font('day')
        self.font_client = style_manager.get_font('client')
    
    def draw_calendar(self):
        """
        Dibujar el calendario completo para el mes actual.
        
        Limpia widgets existentes y crea nueva cuadrícula de calendario.
        
        Extraído de main.py líneas 78-136.
        """
        # Limpiar widgets existentes del calendario
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # Actualizar título
        current_month, current_year = self.calendar_logic.get_current_month_year()
        self.title_label.config(text=f'{calendar.month_name[current_month]} {current_year}')
        
        # Crear encabezado de días de la semana
        weekday_header = WeekdayHeader(self.calendar_frame)
        
        # Obtener datos del calendario y crear celdas de día
        month_calendar_data = self.calendar_logic.get_month_calendar_data()
        self.day_buttons = []
        
        for row_idx, week_data in enumerate(month_calendar_data, start=1):  # Comenzar en fila 1 (después del encabezado)
            for col_idx, day_info in enumerate(week_data):
                self._create_day_cell(day_info, row_idx, col_idx)
    
    def update_cell(self, day):
        """
        Actualizar una celda de día específica para reflejar datos actuales.
        
        Args:
            day (datetime.date): Día a actualizar
            
        Extraído de main.py líneas 138-183.
        """
        # Encontrar celda para el día dado
        for entry in self.day_buttons:
            if len(entry) < 3:
                continue
                
            cell_day, canvas, canvas_ids = entry
            if cell_day == day:
                # Obtener estado actual del día
                day_info = self.calendar_logic.get_day_status(day)
                self._update_canvas_content(canvas, canvas_ids, day_info)
                return
    
    def _create_day_cell(self, day_info, row_idx, col_idx):
        """
        Crear un canvas de celda de día único y su contenido.
        
        Args:
            day_info (dict): Información del día desde la lógica del calendario
            row_idx (int): Posición de fila en la cuadrícula
            col_idx (int): Posición de columna en la cuadrícula
        """
        day = day_info['date']
        
        # Crear canvas para la celda del día
        canvas = tk.Canvas(
            self.calendar_frame,
            width=AppConfig.CELL_SIZE['width'],
            height=AppConfig.CELL_SIZE['height'],
            highlightthickness=0
        )
        canvas.grid(
            row=row_idx, column=col_idx,
            padx=AppConfig.PADDING['cell'][0],
            pady=AppConfig.PADDING['cell'][1],
            sticky='nsew'
        )
        
        # Configurar pesos de cuadrícula para diseño responsivo
        self.calendar_frame.grid_rowconfigure(row_idx, weight=1, minsize=AppConfig.CELL_SIZE['height'])
        self.calendar_frame.grid_columnconfigure(col_idx, weight=1, minsize=AppConfig.CELL_SIZE['width'])
        
        # Crear elementos del canvas
        canvas_ids = self._create_canvas_items(canvas)
        
        # Establecer contenido inicial
        self._update_canvas_content(canvas, canvas_ids, day_info)
        
        # Enlazar eventos de clic
        if self.event_handler:
            self.event_handler.create_day_cell_bindings(canvas, day)
        
        # Almacenar referencia de celda
        self.day_buttons.append((day, canvas, canvas_ids))
    
    def _create_canvas_items(self, canvas):
        """
        Crear elementos visuales para una celda de día.
        
        Args:
            canvas: Widget canvas en el que dibujar
            
        Returns:
            dict: Diccionario con IDs de elementos del canvas
        """
        # Rectángulo de fondo
        rect = canvas.create_rectangle(
            0, 0, 
            AppConfig.CELL_SIZE['width'], 
            AppConfig.CELL_SIZE['height'],
            fill=AppConfig.COLORS['current_month'], 
            width=0
        )
        
        # Texto del número del día
        day_txt = canvas.create_text(
            8, 8,
            anchor='nw',
            text='',
            font=self.font_day,
            fill=AppConfig.COLORS['text_current']
        )
        
        # Texto del nombre del cliente
        name_txt = canvas.create_text(
            8, 36,
            anchor='nw',
            text='',
            font=self.font_client,
            width=AppConfig.CELL_SIZE['width'] - 16  # Considerar relleno
        )
        
        return {
            'rect': rect,
            'day_txt': day_txt,
            'name_txt': name_txt
        }
    
    def _update_canvas_content(self, canvas, canvas_ids, day_info):
        """
        Actualizar contenido de un canvas con información del día.
        
        Args:
            canvas: Widget canvas
            canvas_ids (dict): Diccionario con IDs de elementos del canvas
            day_info (dict): Información del día a mostrar
        """
        is_current_month = day_info['is_current_month']
        reservation = day_info['reservation']
        is_available = day_info['is_available']
        
        # Obtener IDs de elementos del canvas
        rect = canvas_ids.get('rect')
        name_txt = canvas_ids.get('name_txt')
        day_txt = canvas_ids.get('day_txt')
        
        # Actualizar basado en si es del mes actual
        if not is_current_month:
            self._update_other_month_day(canvas, rect, day_txt, name_txt)
            return
        
        # Actualizar día del mes actual
        self._update_current_month_day(canvas, rect, day_txt, name_txt, day_info)
    
    def _update_other_month_day(self, canvas, rect, day_txt, name_txt):
        """
        Actualizar visualización para días no en el mes actual.
        
        Args:
            canvas: Widget canvas
            rect: ID del rectángulo de fondo
            day_txt: ID del texto del día
            name_txt: ID del texto del nombre
        """
        try:
            canvas.itemconfig(day_txt, fill=AppConfig.COLORS['text_other'])
            canvas.itemconfig(rect, fill=AppConfig.COLORS['other_month'])
            canvas.itemconfig(name_txt, text='')
        except Exception:
            # Manejar casos donde los widgets podrían haber sido destruidos
            pass
    
    def _update_current_month_day(self, canvas, rect, day_txt, name_txt, day_info):
        """
        Actualizar visualización para días del mes actual.
        
        Args:
            canvas: Widget canvas
            rect: ID del rectángulo de fondo
            day_txt: ID del texto del día
            name_txt: ID del texto del nombre
            day_info (dict): Información del día
        """
        day = day_info['date']
        reservation = day_info['reservation']
        is_available = day_info['is_available']
        
        try:
            # Siempre establecer el número del día
            canvas.itemconfig(day_txt, text=str(day.day))
            
            if reservation:
                # El día tiene una reserva
                status = reservation.get('payment_status', '')
                color = self.style_manager.get_color_for_status(reservation_status=status)
                canvas.itemconfig(rect, fill=color)
                
                display_name = f"{reservation.get('first_name','')} {reservation.get('last_name','')}".strip()
                canvas.itemconfig(name_txt, text=display_name)
                
            elif not is_available:
                # El día está marcado como no disponible
                canvas.itemconfig(rect, fill=AppConfig.COLORS['unavailable'])
                canvas.itemconfig(name_txt, text=AppConfig.LABELS['unavailable_msg'])
                
            else:
                # El día está disponible
                canvas.itemconfig(rect, fill=AppConfig.COLORS['available'])
                canvas.itemconfig(name_txt, text='')
                
        except Exception:
            # Manejar casos donde los widgets podrían haber sido destruidos
            pass
    
    def get_day_buttons(self):
        """
        Obtener lista de todas las celdas de día.
        
        Returns:
            list: Lista de tuplas (day, canvas, canvas_ids)
        """
        return self.day_buttons