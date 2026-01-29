"""
Componentes de formulario para Kumbayah Calendar App.

Extraído de main.py líneas 371-447 y 208-369 para crear componentes de formulario modulares.
Incluye clases ReservationForm y ReservationDetailsDialog.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from config.app_config import AppConfig
from utils.validators import validate_client_data, validate_reservation_data, is_reference_required


class ReservationForm:
    """
    Formulario para crear nuevas reservas.
    
    Extraído de main.py líneas 371-447.
    Maneja entrada del usuario para crear nuevas reservas con validación.
    """
    
    def __init__(self, parent, calendar_logic, update_cell_callback):
        """
        Inicializar formulario de reserva.
        
        Args:
            parent: Widget padre (ventana principal)
            calendar_logic: Instancia de CalendarLogic para lógica de negocio
            update_cell_callback: Función para actualizar celda del calendario después del envío del formulario
        """
        self.parent = parent
        self.calendar_logic = calendar_logic
        self.update_cell_callback = update_cell_callback
    
    def open(self, day_str):
        """
        Abrir formulario de reserva para un día específico.
        
        Args:
            day_str (str): Cadena de fecha en formato AAAA-MM-DD
        """
        form = tk.Toplevel(self.parent)
        form.title(f"{AppConfig.LABELS['reservation_title_prefix']}{day_str}")
        
        # Crear campos del formulario
        self._create_form_fields(form, day_str)
    
    def _create_form_fields(self, form, day_str):
        """
        Crear todos los campos y widgets del formulario.
        
        Args:
            form: Ventana de formulario Toplevel
            day_str (str): Cadena de fecha para la reserva
        """
        labels = [AppConfig.LABELS['name'], AppConfig.LABELS['last_name'], 
                  AppConfig.LABELS['phone'], AppConfig.LABELS['amount']]
        entries = {}
        
        # Crear campos de entrada
        for i, label in enumerate(labels):
            ttk.Label(form, text=label).grid(
                row=i, column=0, 
                padx=AppConfig.PADDING['form_field'][0], 
                pady=AppConfig.PADDING['form_field'][1],
                sticky='e'
            )
            entry = ttk.Entry(form)
            entry.grid(
                row=i, column=1, 
                padx=AppConfig.PADDING['form_field'][0], 
                pady=AppConfig.PADDING['form_field'][1]
            )
            entries[label] = entry
        
        # Crear dropdown de estado de pago
        self._create_payment_status_dropdown(form, entries)
        
        # Crear dropdown de método de pago
        self._create_payment_method_dropdown(form, entries)
        
        # Crear botón de envío
        ttk.Button(
            form, 
            text=AppConfig.LABELS['save'], 
            command=lambda: self._submit_form(entries, day_str, form)
        ).grid(row=7, column=0, columnspan=2, pady=8)
    
    def _create_payment_status_dropdown(self, form, entries):
        """Crear dropdown de estado de pago."""
        ttk.Label(form, text=AppConfig.LABELS['payment_status']).grid(
            row=4, column=0, 
            padx=AppConfig.PADDING['form_field'][0], 
            pady=AppConfig.PADDING['form_field'][1],
            sticky='e'
        )
        
        pay_status = ttk.Combobox(form, values=AppConfig.PAYMENT_STATUSES, state='readonly')
        pay_status.current(0)
        pay_status.grid(
            row=4, column=1, 
            padx=AppConfig.PADDING['form_field'][0], 
            pady=AppConfig.PADDING['form_field'][1]
        )
        entries['payment_status'] = pay_status
    
    def _create_payment_method_dropdown(self, form, entries):
        """Crear dropdown de método de pago con campo de referencia condicional."""
        ttk.Label(form, text=AppConfig.LABELS['payment_method']).grid(
            row=5, column=0, 
            padx=AppConfig.PADDING['form_field'][0], 
            pady=AppConfig.PADDING['form_field'][1],
            sticky='e'
        )
        
        pay_method = ttk.Combobox(form, values=AppConfig.PAYMENT_METHODS, state='readonly')
        pay_method.current(0)
        pay_method.grid(
            row=5, column=1, 
            padx=AppConfig.PADDING['form_field'][0], 
            pady=AppConfig.PADDING['form_field'][1]
        )
        
        # Campo de referencia (mostrado condicionalmente)
        ref_label = ttk.Label(form, text=AppConfig.LABELS['reference'])
        ref_entry = ttk.Entry(form)
        
        def on_method_change(event=None):
            if is_reference_required(pay_method.get()):
                ref_label.grid(
                    row=6, column=0, 
                    padx=AppConfig.PADDING['form_field'][0], 
                    pady=AppConfig.PADDING['form_field'][1],
                    sticky='e'
                )
                ref_entry.grid(
                    row=6, column=1, 
                    padx=AppConfig.PADDING['form_field'][0], 
                    pady=AppConfig.PADDING['form_field'][1]
                )
            else:
                ref_label.grid_remove()
                ref_entry.grid_remove()
        
        pay_method.bind('<<ComboboxSelected>>', on_method_change)
        on_method_change()  # Estado inicial
        
        entries['payment_method'] = pay_method
        entries['reference'] = ref_entry
    
    def _submit_form(self, entries, day_str, form):
        """
        Validar y enviar datos del formulario.
        
        Args:
            entries (dict): Diccionario con todos los widgets del formulario
            day_str (str): Cadena de fecha para la reserva
            form: Ventana de formulario Toplevel
        """
        # Obtener datos del formulario
        fn = entries[AppConfig.LABELS['name']].get().strip()
        ln = entries[AppConfig.LABELS['last_name']].get().strip()
        phone = entries[AppConfig.LABELS['phone']].get().strip()
        amount = entries[AppConfig.LABELS['amount']].get().strip()
        ps = entries['payment_status'].get()
        pm = entries['payment_method'].get()
        ref = entries['reference'].get().strip()
        
        # Validar datos del cliente
        client_valid, client_error = validate_client_data(fn, ln, phone)
        if not client_valid:
            messagebox.showerror('Error', client_error)
            return
        
        # Validar datos de reserva
        reservation_valid, reservation_error = validate_reservation_data(amount, pm, ref)
        if not reservation_valid:
            messagebox.showerror('Error', reservation_error)
            return
        
        # Guardar reserva
        self.calendar_logic.add_or_update_reservation(
            day_str,
            {'first_name': fn, 'last_name': ln, 'phone': phone},
            {'amount': float(amount), 'payment_status': ps, 'payment_method': pm, 'reference': ref}
        )
        
        # Cerrar formulario y actualizar calendario
        form.destroy()
        try:
            d = datetime.fromisoformat(day_str).date()
            self.update_cell_callback(d)
        except Exception:
            # Si la actualización de celda individual falla, el calendario se redibujará externamente
            pass


class ReservationDetailsDialog:
    """
    Diálogo para ver, editar y eliminar reservas existentes.
    
    Extraído de main.py líneas 208-369.
    Soporta modos de solo lectura y edición con funcionalidad CRUD completa.
    """
    
    def __init__(self, parent, font_day, font_client, calendar_logic, update_cell_callback, redraw_calendar_callback):
        """
        Inicializar diálogo de detalles de reserva.
        
        Args:
            parent: Widget padre (ventana principal)
            font_day: Fuente para etiquetas
            font_client: Fuente para visualización de datos
            calendar_logic: Instancia de CalendarLogic para lógica de negocio
            update_cell_callback: Función para actualizar celda individual
            redraw_calendar_callback: Función para redibujar calendario completo
        """
        self.parent = parent
        self.font_day = font_day
        self.font_client = font_client
        self.calendar_logic = calendar_logic
        self.update_cell_callback = update_cell_callback
        self.redraw_calendar_callback = redraw_calendar_callback
    
    def show(self, reservation):
        """
        Mostrar diálogo de detalles de reserva.
        
        Args:
            reservation (dict): Diccionario de datos de reserva
        """
        form = tk.Toplevel(self.parent)
        form.title(f"{AppConfig.LABELS['details_title_prefix']}{reservation['date']}")
        form.geometry(AppConfig.FORM_DIMENSIONS['details'])
        
        # Crear componentes del diálogo
        info_frame = ttk.Frame(form)
        info_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        form.grid_rowconfigure(0, weight=1)
        form.grid_columnconfigure(0, weight=1)
        
        # Crear frame de botones
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=1, column=0, pady=8)
        
        # Estado inicial: solo lectura
        self._show_readonly_view(info_frame, btn_frame, reservation, form)
    
    def _show_readonly_view(self, info_frame, btn_frame, reservation, form):
        """Mostrar detalles de reserva en modo de solo lectura."""
        # Limpiar frame de información
        for widget in info_frame.winfo_children():
            widget.destroy()
        
        # Mostrar información de solo lectura
        readonly_data = [
            (AppConfig.LABELS['name'] + ':', f"{reservation.get('first_name','')} {reservation.get('last_name','')}"),
            (AppConfig.LABELS['phone'] + ':', reservation.get('phone','')),
            (AppConfig.LABELS['amount'] + ':', reservation.get('amount','')),
            (AppConfig.LABELS['payment_status'] + ':', reservation.get('payment_status','')),
            (AppConfig.LABELS['payment_method'] + ':', reservation.get('payment_method',''))
        ]
        
        for i, (label, value) in enumerate(readonly_data):
            ttk.Label(info_frame, text=label, font=self.font_day).grid(row=i, column=0, sticky='w')
            ttk.Label(info_frame, text=value, font=self.font_client).grid(row=i, column=1, sticky='w')
        
        # Agregar referencia si existe
        if reservation.get('reference'):
            ttk.Label(info_frame, text=AppConfig.LABELS['reference'] + ':', font=self.font_day).grid(
                row=5, column=0, sticky='w'
            )
            ttk.Label(info_frame, text=reservation.get('reference'), font=self.font_client).grid(
                row=5, column=1, sticky='w'
            )
        
        # Crear botones de acción
        self._create_readonly_buttons(btn_frame, info_frame, reservation, form)
    
    def _create_readonly_buttons(self, btn_frame, info_frame, reservation, form):
        """Create buttons for read-only view."""
        ttk.Button(
            btn_frame, 
            text=AppConfig.LABELS['edit'], 
            command=lambda: self._enter_edit_mode(info_frame, btn_frame, reservation, form)
        ).grid(row=0, column=0, padx=AppConfig.PADDING['button'])
        
        ttk.Button(
            btn_frame, 
            text=AppConfig.LABELS['delete'], 
            command=lambda: self._delete_reservation(reservation, form)
        ).grid(row=0, column=1, padx=AppConfig.PADDING['button'])
        
        ttk.Button(
            btn_frame, 
            text=AppConfig.LABELS['close'], 
            command=form.destroy
        ).grid(row=0, column=2, padx=AppConfig.PADDING['button'])
    
    def _enter_edit_mode(self, info_frame, btn_frame, reservation, form):
        """Switch to edit mode with input fields."""
        # Clear info frame
        for widget in info_frame.winfo_children():
            widget.destroy()
        
        # Create edit widgets
        edit_widgets = {}
        
        labels = [AppConfig.LABELS['name'], AppConfig.LABELS['last_name'], 
                  AppConfig.LABELS['phone'], AppConfig.LABELS['amount']]
        values = {
            AppConfig.LABELS['name']: reservation['first_name'],
            AppConfig.LABELS['last_name']: reservation['last_name'],
            AppConfig.LABELS['phone']: reservation['phone'],
            AppConfig.LABELS['amount']: str(reservation['amount']),
        }
        
        # Create input fields
        for i, label in enumerate(labels):
            ttk.Label(info_frame, text=label).grid(
                row=i, column=0, 
                padx=AppConfig.PADDING['form_field'][0], 
                pady=AppConfig.PADDING['form_field'][1],
                sticky='e'
            )
            entry = ttk.Entry(info_frame)
            entry.grid(
                row=i, column=1, 
                padx=AppConfig.PADDING['form_field'][0], 
                pady=AppConfig.PADDING['form_field'][1]
            )
            entry.insert(0, values[label])
            edit_widgets[label] = entry
        
        # Create payment status dropdown
        self._create_edit_payment_status(info_frame, edit_widgets, reservation)
        
        # Create payment method dropdown
        self._create_edit_payment_method(info_frame, edit_widgets, reservation)
        
        # Create edit mode buttons
        self._create_edit_buttons(btn_frame, edit_widgets, reservation, form)
    
    def _create_edit_payment_status(self, info_frame, edit_widgets, reservation):
        """Create payment status dropdown for edit mode."""
        ttk.Label(info_frame, text=AppConfig.LABELS['payment_status']).grid(
            row=4, column=0, 
            padx=AppConfig.PADDING['form_field'][0], 
            pady=AppConfig.PADDING['form_field'][1],
            sticky='e'
        )
        
        pay_status = ttk.Combobox(info_frame, values=AppConfig.PAYMENT_STATUSES, state='readonly')
        try:
            pay_status.current(AppConfig.PAYMENT_STATUSES.index(reservation['payment_status']))
        except Exception:
            pay_status.current(0)
        pay_status.grid(
            row=4, column=1, 
            padx=AppConfig.PADDING['form_field'][0], 
            pady=AppConfig.PADDING['form_field'][1]
        )
        edit_widgets['pay_status'] = pay_status
    
    def _create_edit_payment_method(self, info_frame, edit_widgets, reservation):
        """Create payment method dropdown for edit mode."""
        ttk.Label(info_frame, text=AppConfig.LABELS['payment_method']).grid(
            row=5, column=0, 
            padx=AppConfig.PADDING['form_field'][0], 
            pady=AppConfig.PADDING['form_field'][1],
            sticky='e'
        )
        
        pay_method = ttk.Combobox(info_frame, values=AppConfig.PAYMENT_METHODS, state='readonly')
        try:
            pay_method.current(AppConfig.PAYMENT_METHODS.index(reservation['payment_method']))
        except Exception:
            pay_method.current(0)
        pay_method.grid(
            row=5, column=1, 
            padx=AppConfig.PADDING['form_field'][0], 
            pady=AppConfig.PADDING['form_field'][1]
        )
        edit_widgets['pay_method'] = pay_method
        
        # Reference field
        ref_label = ttk.Label(info_frame, text=AppConfig.LABELS['reference'])
        ref_entry = ttk.Entry(info_frame)
        ref_entry.insert(0, reservation.get('reference', ''))
        
        def on_method_change(event=None):
            if is_reference_required(pay_method.get()):
                ref_label.grid(
                    row=6, column=0, 
                    padx=AppConfig.PADDING['form_field'][0], 
                    pady=AppConfig.PADDING['form_field'][1],
                    sticky='e'
                )
                ref_entry.grid(
                    row=6, column=1, 
                    padx=AppConfig.PADDING['form_field'][0], 
                    pady=AppConfig.PADDING['form_field'][1]
                )
            else:
                ref_label.grid_remove()
                ref_entry.grid_remove()
        
        pay_method.bind('<<ComboboxSelected>>', on_method_change)
        on_method_change()
        edit_widgets['ref_entry'] = ref_entry
    
    def _create_edit_buttons(self, btn_frame, edit_widgets, reservation, form):
        """Create buttons for edit mode."""
        ttk.Button(
            btn_frame, 
            text=AppConfig.LABELS['save'], 
            command=lambda: self._save_from_edit(edit_widgets, reservation, btn_frame, form)
        ).grid(row=0, column=0, padx=AppConfig.PADDING['button'])
        
        ttk.Button(
            btn_frame, 
            text=AppConfig.LABELS['cancel'], 
            command=lambda: self._cancel_edit(btn_frame, reservation, form)
        ).grid(row=0, column=1, padx=AppConfig.PADDING['button'])
    
    def _save_from_edit(self, edit_widgets, reservation, btn_frame, form):
        """Save changes from edit mode."""
        # Get form data
        fn = edit_widgets[AppConfig.LABELS['name']].get().strip()
        ln = edit_widgets[AppConfig.LABELS['last_name']].get().strip()
        phone = edit_widgets[AppConfig.LABELS['phone']].get().strip()
        amount = edit_widgets[AppConfig.LABELS['amount']].get().strip()
        ps = edit_widgets['pay_status'].get()
        pm = edit_widgets['pay_method'].get()
        ref = edit_widgets['ref_entry'].get().strip()
        
        # Validate
        client_valid, client_error = validate_client_data(fn, ln, phone)
        if not client_valid:
            messagebox.showerror('Error', client_error)
            return
        
        reservation_valid, reservation_error = validate_reservation_data(amount, pm, ref)
        if not reservation_valid:
            messagebox.showerror('Error', reservation_error)
            return
        
        # Update reservation
        self.calendar_logic.add_or_update_reservation(
            reservation['date'],
            {'first_name': fn, 'last_name': ln, 'phone': phone},
            {'amount': float(amount), 'payment_status': ps, 'payment_method': pm, 'reference': ref}
        )
        
        # Update local reservation object
        reservation['first_name'] = fn
        reservation['last_name'] = ln
        reservation['phone'] = phone
        reservation['amount'] = float(amount)
        reservation['payment_status'] = ps
        reservation['payment_method'] = pm
        reservation['reference'] = ref
        
        # Return to readonly view
        self._show_readonly_view(btn_frame.master.winfo_children()[0], btn_frame, reservation, form)
        self.redraw_calendar_callback()
    
    def _cancel_edit(self, btn_frame, reservation, form):
        """Cancel edit mode and return to readonly view."""
        info_frame = btn_frame.master.winfo_children()[0]
        self._show_readonly_view(info_frame, btn_frame, reservation, form)
    
    def _delete_reservation(self, reservation, form):
        """Delete the reservation after confirmation."""
        if messagebox.askyesno('Confirmar', AppConfig.LABELS['confirm_delete']):
            self.calendar_logic.delete_reservation(reservation['date'])
            form.destroy()
            
            # Update calendar
            try:
                d = datetime.fromisoformat(reservation['date']).date()
                self.update_cell_callback(d)
            except Exception:
                self.redraw_calendar_callback()


class FormManager:
    """
    Gestiona todas las interacciones de formulario para la aplicación.
    
    Centraliza la creación de formularios y proporciona una interfaz limpia
    para que la aplicación principal interactúe con los formularios.
    """
    
    def __init__(self, parent, style_manager, calendar_logic, calendar_renderer):
        """
        Inicializar gestor de formularios.
        
        Args:
            parent: Ventana principal de la aplicación
            style_manager: Instancia de StyleManager
            calendar_logic: Instancia de CalendarLogic
            calendar_renderer: Instancia de CalendarRenderer
        """
        self.parent = parent
        self.style_manager = style_manager
        self.calendar_logic = calendar_logic
        self.calendar_renderer = calendar_renderer
        
        # Inicializar componentes de formulario
        self.reservation_form = ReservationForm(
            parent, calendar_logic, calendar_renderer.update_cell
        )
        
        self.details_dialog = ReservationDetailsDialog(
            parent, 
            style_manager.get_font('day'),
            style_manager.get_font('client'),
            calendar_logic,
            calendar_renderer.update_cell,
            calendar_renderer.draw_calendar
        )
    
    def open_reservation_form(self, day_str):
        """
        Abrir un nuevo formulario de reserva para el día dado.
        
        Args:
            day_str (str): Cadena de fecha en formato AAAA-MM-DD
        """
        self.reservation_form.open(day_str)
    
    def show_reservation_details(self, reservation):
        """
        Mostrar diálogo de detalles de reserva.
        
        Args:
            reservation (dict): Datos de reserva
        """
        self.details_dialog.show(reservation)