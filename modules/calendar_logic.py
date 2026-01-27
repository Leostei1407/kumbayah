import calendar
from datetime import datetime, date

class CalendarLogic:
    def __init__(self, db_manager, clients_manager, reservations_manager):
        self.db_manager = db_manager
        self.clients_manager = clients_manager
        self.reservations_manager = reservations_manager

        self.now = datetime.now()
        self.current_year = self.now.year
        self.current_month = self.now.month

    def get_current_month_year(self):
        return self.current_month, self.current_year

    def set_month_year(self, month, year):
        self.current_month = month
        self.current_year = year

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        return self.current_month, self.current_year

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        return self.current_month, self.current_year

    def get_month_calendar_data(self):
        cal = calendar.Calendar(firstweekday=0)
        month_cal = cal.monthdatescalendar(self.current_year, self.current_month)

        calendar_data = []
        for week in month_cal:
            week_data = []
            for day in week:
                day_str = day.isoformat()
                reservation = None
                is_available = True

                if day.month == self.current_month:
                    reservation = self.reservations_manager.get_reservation(day_str)
                    is_available = self.reservations_manager.is_available(day_str)

                week_data.append({
                    'date': day,
                    'date_str': day_str,
                    'is_current_month': day.month == self.current_month,
                    'reservation': reservation,
                    'is_available': is_available
                })
            calendar_data.append(week_data)
        return calendar_data

    def toggle_day_availability(self, day):
        day_str = day.isoformat()
        is_currently_available = self.reservations_manager.is_available(day_str)
        self.reservations_manager.set_availability(day_str, 0 if is_currently_available else 1)
        # Return updated status for the day
        return self.reservations_manager.is_available(day_str)

    def get_day_status(self, day):
        day_str = day.isoformat()
        reservation = self.reservations_manager.get_reservation(day_str)
        is_available = self.reservations_manager.is_available(day_str)
        return {
            'date': day,
            'date_str': day_str,
            'is_current_month': day.month == self.current_month,
            'reservation': reservation,
            'is_available': is_available
        }

    def add_or_update_reservation(self, day_str, client_data, reservation_data):
        first_name = client_data['first_name']
        last_name = client_data['last_name']
        phone = client_data['phone']

        client_id = self.clients_manager.add_or_get_client(first_name, last_name, phone)

        self.reservations_manager.add_reservation({
            'date': day_str,
            'amount': reservation_data['amount'],
            'payment_status': reservation_data['payment_status'],
            'payment_method': reservation_data['payment_method'],
            'reference': reservation_data.get('reference', ''),
        }, client_id)

    def delete_reservation(self, day_str):
        self.reservations_manager.delete_reservation(day_str)
