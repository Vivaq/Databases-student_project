class DbDataProvider(object):
    def __init__(self, db_address="", username="", passw=""):
        pass

    def get_type_eqs_by_time(self, time):
        pass

    def get_eq_providers_with_eq(self, eq_list):
        pass

    def add_eqs(self, eq_list):
        pass

    def get_doctors_with_type(self):
        pass

    def get_pref_hours_doctor(self, doctor):
        pass

    def check_collision(self, employer, room):
        pass

    def get_rooms(self):
        pass

    def add_term_visit(self, employer, weekday, next, start_t, end_h):
        pass
