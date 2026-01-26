import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import calendar
from modules.database import Database
from modules.clients import Clients
from modules.reservations import Reservations
import tkinter.font as tkfont
from modules.calendar_logic import CalendarLogic


class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Kumbayah - Calendario de Reservas (offline)')
        
        # Configuración de la base de datos
        self.db_manager = Database('kumbayah.db')
        self.db_manager.create_tables()
        db_conn = self.db_manager.connect()

        self.clients_manager = Clients(db_conn)
        self.reservations_manager = Reservations(db_conn)
        self.calendar_logic = CalendarLogic(self.db_manager, self.clients_manager, self.reservations_manager)

        # Estilos y fuentes
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except Exception:
            pass
        self.font_title = tkfont.Font(family='Segoe UI', size=16, weight='bold')
        self.font_day = tkfont.Font(family='Segoe UI', size=14, weight='bold')
        self.font_client = tkfont.Font(family='Segoe UI', size=10)

        top_frame = ttk.Frame(root)
        top_frame.pack(fill='x', padx=12, pady=10)

        prev_btn = ttk.Button(top_frame, text='<', width=3, command=self.prev_month)
        prev_btn.grid(row=0, column=0)
        self.title_label = ttk.Label(top_frame, text='', font=self.font_title)
        self.title_label.grid(row=0, column=1, padx=12)
        next_btn = ttk.Button(top_frame, text='>', width=3, command=self.next_month)
        next_btn.grid(row=0, column=2)

        controls = ttk.Frame(root)
        controls.pack(fill='x', padx=12, pady=(0,6))
        ttk.Button(controls, text='Marcar disponibilidad (click derecho)', command=lambda: None).grid(row=0, column=0)

        # Leyenda
        legend = ttk.Frame(controls)
        legend.grid(row=0, column=1, padx=10)
        ttk.Label(legend, text='Disponible', background='#dcedc8').grid(row=0, column=0, padx=4)
        ttk.Label(legend, text='Reservado', background='#ffcdd2').grid(row=0, column=1, padx=4)
        ttk.Label(legend, text='Parcial/Nada', background='#ffe0b2').grid(row=0, column=2, padx=4)
        ttk.Label(legend, text='Bloqueado', background='#e0e0e0').grid(row=0, column=3, padx=4)

        self.calendar_frame = ttk.Frame(root)
        self.calendar_frame.pack(padx=12, pady=6)

        self.day_buttons = []
        self.draw_calendar()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.db_manager.close()
        self.root.destroy()

    def prev_month(self):
        self.calendar_logic.prev_month()
        self.draw_calendar()

    def next_month(self):
        self.calendar_logic.next_month()
        self.draw_calendar()

    def draw_calendar(self):
        for w in self.calendar_frame.winfo_children():
            w.destroy()

        current_month, current_year = self.calendar_logic.get_current_month_year()
        self.title_label.config(text=f'{calendar.month_name[current_month]} {current_year}')

        # Encabezados de días de la semana
        days = ['Lun','Mar','Mié','Jue','Vie','Sáb','Dom']
        for i, d in enumerate(days):
            ttk.Label(self.calendar_frame, text=d).grid(row=0, column=i, padx=4, pady=2)

        month_calendar_data = self.calendar_logic.get_month_calendar_data()
        self.day_buttons = []
        for r, week_data in enumerate(month_calendar_data, start=1):
            for c, day_info in enumerate(week_data):
                day = day_info['date']
                day_str = day_info['date_str']
                is_current_month = day_info['is_current_month']
                booking = day_info['booking']
                avail = day_info['is_available']

                canvas = tk.Canvas(self.calendar_frame, width=140, height=110, highlightthickness=0)
                canvas.grid(row=r, column=c, padx=6, pady=6, sticky='nsew')
                canvas.config(bg='#ffffff')
                self.calendar_frame.grid_rowconfigure(r, weight=1, minsize=110)
                self.calendar_frame.grid_columnconfigure(c, weight=1, minsize=140)

                rect = canvas.create_rectangle(0, 0, 140, 110, fill='#ffffff', width=0)
                day_txt = canvas.create_text(8, 8, anchor='nw', text=str(day.day), font=self.font_day, fill='#000000')
                name_txt = canvas.create_text(8, 36, anchor='nw', text='', font=self.font_client, width=120)

                def _on_click(ev, d=day):
                    self.on_day_click(d)
                def _on_right_click(ev, d=day):
                    self.toggle_availability(d)

                canvas.bind('<Button-1>', _on_click)
                canvas.bind('<Button-3>', _on_right_click)

                if not is_current_month:
                    canvas.itemconfig(day_txt, fill='#9e9e9e')
                    canvas.itemconfig(rect, fill='#f5f5f5')
                    canvas.itemconfig(name_txt, text='')
                else:
                    if booking:
                        status = booking.get('payment_status','')
                        color = '#ffc0cb' if status == 'Completo' else '#ffcc80'
                        canvas.itemconfig(rect, fill=color)
                        display_name = f"{booking.get('first_name','')} {booking.get('last_name','')}".strip()
                        canvas.itemconfig(name_txt, text=display_name)
                    elif not avail:
                        canvas.itemconfig(rect, fill='#eeeeee')
                        canvas.itemconfig(name_txt, text='No disponible')
                    else:
                        canvas.itemconfig(rect, fill='#c8e6c9')
                        canvas.itemconfig(name_txt, text='')

                self.day_buttons.append((day, canvas, {'rect': rect, 'day_txt': day_txt, 'name_txt': name_txt}))

    def update_cell(self, day):
        for entry in self.day_buttons:
            if len(entry) < 3:
                continue
            d, canvas, ids = entry
            if d == day:
                day_info = self.calendar_logic.get_day_status(d)
                is_current_month = day_info['is_current_month']
                booking = day_info['booking']
                avail = day_info['is_available']

                rect = ids.get('rect')
                name_txt = ids.get('name_txt')
                day_txt = ids.get('day_txt')

                if not is_current_month:
                    try:
                        canvas.itemconfig(day_txt, fill='#9e9e9e')
                        canvas.itemconfig(rect, fill='#f5f5f5')
                        canvas.itemconfig(name_txt, text='')
                    except Exception:
                        pass
                    return

                if booking:
                    status = booking.get('payment_status','')
                    color = '#ffc0cb' if status == 'Completo' else '#ffcc80'
                    try:
                        canvas.itemconfig(rect, fill=color)
                        display_name = f"{booking.get('first_name','')} {booking.get('last_name','')}".strip()
                        canvas.itemconfig(name_txt, text=display_name)
                    except Exception:
                        pass
                elif not avail:
                    try:
                        canvas.itemconfig(rect, fill='#eeeeee')
                        canvas.itemconfig(name_txt, text='No disponible')
                    except Exception:
                        pass
                else:
                    try:
                        canvas.itemconfig(rect, fill='#c8e6c9')
                        canvas.itemconfig(name_txt, text='')
                    except Exception:
                        pass
                return

    def toggle_availability(self, day):
        current_month, _ = self.calendar_logic.get_current_month_year()
        if day.month != current_month:
            return
        self.calendar_logic.toggle_day_availability(day)
        self.update_cell(day)

    def on_day_click(self, day):
        current_month, _ = self.calendar_logic.get_current_month_year()
        if day.month != current_month:
            return
        
        day_info = self.calendar_logic.get_day_status(day)
        booking = day_info['booking']
        avail = day_info['is_available']

        if booking:
            self.show_booking_details(booking)
        elif not avail:
            messagebox.showinfo('No disponible', 'Este día no está disponible para reservas.')
        else:
            self.open_booking_form(day_info['date_str'])

    def show_booking_details(self, booking):
        # Abrir un diálogo de solo lectura con un botón Editar para cambiar a modo edición
        form = tk.Toplevel(self.root)
        form.title(f"Reserva {booking['date']}")
        form.geometry('420x340')

        info_frame = ttk.Frame(form)
        info_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        form.grid_rowconfigure(0, weight=1)
        form.grid_columnconfigure(0, weight=1)

        def show_readonly():
            for w in info_frame.winfo_children():
                w.destroy()
            ttk.Label(info_frame, text=f"Cliente:", font=self.font_day).grid(row=0, column=0, sticky='w')
            ttk.Label(info_frame, text=f"{booking.get('first_name','')} {booking.get('last_name','')}", font=self.font_client).grid(row=0, column=1, sticky='w')
            ttk.Label(info_frame, text=f"Teléfono:", font=self.font_day).grid(row=1, column=0, sticky='w')
            ttk.Label(info_frame, text=f"{booking.get('phone','')}", font=self.font_client).grid(row=1, column=1, sticky='w')
            ttk.Label(info_frame, text=f"Monto:", font=self.font_day).grid(row=2, column=0, sticky='w')
            ttk.Label(info_frame, text=f"{booking.get('amount','')}", font=self.font_client).grid(row=2, column=1, sticky='w')
            ttk.Label(info_frame, text=f"Estado de pago:", font=self.font_day).grid(row=3, column=0, sticky='w')
            ttk.Label(info_frame, text=f"{booking.get('payment_status','')}", font=self.font_client).grid(row=3, column=1, sticky='w')
            ttk.Label(info_frame, text=f"Método:", font=self.font_day).grid(row=4, column=0, sticky='w')
            ttk.Label(info_frame, text=f"{booking.get('payment_method','')}", font=self.font_client).grid(row=4, column=1, sticky='w')
            if booking.get('reference'):
                ttk.Label(info_frame, text=f"Referencia:", font=self.font_day).grid(row=5, column=0, sticky='w')
                ttk.Label(info_frame, text=f"{booking.get('reference')}", font=self.font_client).grid(row=5, column=1, sticky='w')

        # contenedor de widgets para edición
        edit_widgets = {}

        def enter_edit_mode():
            for w in info_frame.winfo_children():
                w.destroy()
            labels = ['Nombre','Apellido','Teléfono','Monto a pagar']
            values = {
                'Nombre': booking['first_name'],
                'Apellido': booking['last_name'],
                'Teléfono': booking['phone'],
                'Monto a pagar': str(booking['amount']),
            }
            for i, lab in enumerate(labels):
                ttk.Label(info_frame, text=lab).grid(row=i, column=0, sticky='e', padx=6, pady=4)
                ent = ttk.Entry(info_frame)
                ent.grid(row=i, column=1, padx=6, pady=4)
                ent.insert(0, values[lab])
                edit_widgets[lab] = ent

            ttk.Label(info_frame, text='Estado de pago').grid(row=4, column=0, sticky='e', padx=6, pady=4)
            pay_status = ttk.Combobox(info_frame, values=['Completo','Mitad','Nada'], state='readonly')
            try:
                pay_status.current(['Completo','Mitad','Nada'].index(booking['payment_status']))
            except Exception:
                pay_status.current(0)
            pay_status.grid(row=4, column=1, padx=6, pady=4)
            edit_widgets['pay_status'] = pay_status

            ttk.Label(info_frame, text='Método de pago').grid(row=5, column=0, sticky='e', padx=6, pady=4)
            pay_method = ttk.Combobox(info_frame, values=['PagoMovil','Efectivo','Transferencia'], state='readonly')
            try:
                pay_method.current(['PagoMovil','Efectivo','Transferencia'].index(booking['payment_method']))
            except Exception:
                pay_method.current(0)
            pay_method.grid(row=5, column=1, padx=6, pady=4)
            edit_widgets['pay_method'] = pay_method

            ref_label = ttk.Label(info_frame, text='Referencia (>=6 dígitos)')
            ref_entry = ttk.Entry(info_frame)
            ref_entry.insert(0, booking.get('reference',''))

            def on_method_change(event=None):
                m = pay_method.get()
                if m in ('PagoMovil','Transferencia'):
                    ref_label.grid(row=6, column=0, sticky='e', padx=6, pady=4)
                    ref_entry.grid(row=6, column=1, padx=6, pady=4)
                else:
                    ref_label.grid_remove()
                    ref_entry.grid_remove()

            pay_method.bind('<<ComboboxSelected>>', on_method_change)
            on_method_change()
            edit_widgets['ref_entry'] = ref_entry

            # reemplazar botones inferiores
            for w in btn_frame.winfo_children():
                w.destroy()
            ttk.Button(btn_frame, text='Guardar', command=save_from_edit).grid(row=0, column=0, padx=6)
            ttk.Button(btn_frame, text='Cancelar', command=cancel_edit).grid(row=0, column=1, padx=6)

        def save_from_edit():
            fn = edit_widgets['Nombre'].get().strip()
            ln = edit_widgets['Apellido'].get().strip()
            phone = edit_widgets['Teléfono'].get().strip()
            amount = edit_widgets['Monto a pagar'].get().strip()
            ps = edit_widgets['pay_status'].get()
            pm = edit_widgets['pay_method'].get()
            ref = edit_widgets['ref_entry'].get().strip()

            if not fn or not ln:
                messagebox.showerror('Error', 'Nombre y apellido son obligatorios.')
                return
            if not phone.isdigit():
                messagebox.showerror('Error', 'Teléfono debe contener sólo dígitos.')
                return
            try:
                amount_val = float(amount)
            except Exception:
                messagebox.showerror('Error', 'Monto inválido.')
                return
            if pm in ('PagoMovil','Transferencia'):
                if not (ref.isdigit() and len(ref) >= 6):
                    messagebox.showerror('Error', 'Referencia debe tener al menos 6 dígitos.')
                    return

            self.calendar_logic.add_or_update_booking(
                booking['date'],
                {'first_name': fn, 'last_name': ln, 'phone': phone},
                {'amount': amount_val, 'payment_status': ps, 'payment_method': pm, 'reference': ref}
            )
            # actualizar el objeto booking local y volver a solo lectura
            booking['first_name'] = fn
            booking['last_name'] = ln
            booking['phone'] = phone
            booking['amount'] = amount_val
            booking['payment_status'] = ps
            booking['payment_method'] = pm
            booking['reference'] = ref
            for w in btn_frame.winfo_children():
                w.destroy()
            ttk.Button(btn_frame, text='Editar', command=enter_edit_mode).grid(row=0, column=0, padx=6)
            ttk.Button(btn_frame, text='Eliminar reserva', command=delete).grid(row=0, column=1, padx=6)
            ttk.Button(btn_frame, text='Cerrar', command=form.destroy).grid(row=0, column=2, padx=6)
            show_readonly()
            self.draw_calendar()

        def cancel_edit():
            for w in btn_frame.winfo_children():
                w.destroy()
            ttk.Button(btn_frame, text='Editar', command=enter_edit_mode).grid(row=0, column=0, padx=6)
            ttk.Button(btn_frame, text='Eliminar reserva', command=delete).grid(row=0, column=1, padx=6)
            ttk.Button(btn_frame, text='Cerrar', command=form.destroy).grid(row=0, column=2, padx=6)
            show_readonly()

        def delete():
            if messagebox.askyesno('Confirmar', '¿Eliminar esta reserva?'):
                self.calendar_logic.delete_booking(booking['date'])
                form.destroy()
                # actualizar solo la celda de ese día
                try:
                    d = datetime.fromisoformat(booking['date']).date()
                    self.update_cell(d)
                except Exception:
                    self.draw_calendar()

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=1, column=0, pady=8)

        ttk.Button(btn_frame, text='Editar', command=enter_edit_mode).grid(row=0, column=0, padx=6)
        ttk.Button(btn_frame, text='Eliminar reserva', command=delete).grid(row=0, column=1, padx=6)
        ttk.Button(btn_frame, text='Cerrar', command=form.destroy).grid(row=0, column=2, padx=6)

        show_readonly()

    def open_booking_form(self, day_str):
        form = tk.Toplevel(self.root)
        form.title(f'Reservar {day_str}')

        labels = ['Nombre','Apellido','Teléfono','Monto a pagar']
        entries = {}
        for i, lab in enumerate(labels):
            ttk.Label(form, text=lab).grid(row=i, column=0, sticky='e', padx=6, pady=4)
            ent = ttk.Entry(form)
            ent.grid(row=i, column=1, padx=6, pady=4)
            entries[lab] = ent

        ttk.Label(form, text='Estado de pago').grid(row=4, column=0, sticky='e', padx=6, pady=4)
        pay_status = ttk.Combobox(form, values=['Completo','Mitad','Nada'], state='readonly')
        pay_status.current(0)
        pay_status.grid(row=4, column=1, padx=6, pady=4)

        ttk.Label(form, text='Método de pago').grid(row=5, column=0, sticky='e', padx=6, pady=4)
        pay_method = ttk.Combobox(form, values=['PagoMovil','Efectivo','Transferencia'], state='readonly')
        pay_method.current(0)
        pay_method.grid(row=5, column=1, padx=6, pady=4)

        ref_label = ttk.Label(form, text='Referencia (>=6 dígitos)')
        ref_entry = ttk.Entry(form)

        def on_method_change(event=None):
            m = pay_method.get()
            if m in ('PagoMovil','Transferencia'):
                ref_label.grid(row=6, column=0, sticky='e', padx=6, pady=4)
                ref_entry.grid(row=6, column=1, padx=6, pady=4)
            else:
                ref_label.grid_remove()
                ref_entry.grid_remove()

        pay_method.bind('<<ComboboxSelected>>', on_method_change)
        on_method_change()

        def submit():
            fn = entries['Nombre'].get().strip()
            ln = entries['Apellido'].get().strip()
            phone = entries['Teléfono'].get().strip()
            amount = entries['Monto a pagar'].get().strip()
            ps = pay_status.get()
            pm = pay_method.get()
            ref = ref_entry.get().strip()

            if not fn or not ln:
                messagebox.showerror('Error', 'Nombre y apellido son obligatorios.')
                return
            if not phone.isdigit():
                messagebox.showerror('Error', 'Teléfono debe contener sólo dígitos.')
                return
            try:
                amount_val = float(amount)
            except Exception:
                messagebox.showerror('Error', 'Monto inválido.')
                return
            if pm in ('PagoMovil','Transferencia'):
                if not (ref.isdigit() and len(ref) >= 6):
                    messagebox.showerror('Error', 'Referencia debe tener al menos 6 dígitos.')
                    return

            self.calendar_logic.add_or_update_booking(
                day_str,
                {'first_name': fn, 'last_name': ln, 'phone': phone},
                {'amount': amount_val, 'payment_status': ps, 'payment_method': pm, 'reference': ref}
            )
            form.destroy()
            # actualizar solo la celda de ese día
            try:
                d = datetime.fromisoformat(day_str).date()
                self.update_cell(d)
            except Exception:
                self.draw_calendar()

        ttk.Button(form, text='Guardar', command=submit).grid(row=7, column=0, columnspan=2, pady=8)


if __name__ == '__main__':
    try:
        from ttkbootstrap import Style
        style = Style('flatly')
        root = style.master
    except Exception:
        root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
