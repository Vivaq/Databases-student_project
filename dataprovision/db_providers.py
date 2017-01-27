import cx_Oracle
from datetime import datetime

class DbDataProvider(object):
    def __init__(self, db_address="ora3.elka.pw.edu.pl", username="kmagryta", passw="kmagryta"):
        dsn_str = cx_Oracle.makedsn(db_address, "1521", "ora3inf")
        self.con = cx_Oracle.connect(user=username, password=passw, dsn=dsn_str)
        self.cur = self.con.cursor()

    def get_type_eqs_by_time(self, time):
        query = """select tu.idtur, tu.nazwa_typu, count(*)
                   from typurzadzenia tu join
                   urzadzenie u on tu.idTUr = u.TypUrzadzenia_idTUr join
                   zaburz zu on zu.urzadzenie_idUr = u.idUr  join
                   Zabieg z on zu.Zabieg_idZ = z.idZ
                   where (select trunc(sysdate - z.koniec) as days from dual) <=
                   """ + str(time) + "group by tu.nazwa_typu, tu.idtur"

        self.cur.execute(query)
        return self.cur.fetchall()

    def get_eq_providers_with_eq(self, eq):
        query = """	select t.nazwa_typu, d.nazwa_firmy, d.nip, du.cena
                    from typurzadzenia t join typurzdos du on du.TypUrzadzenia_idTUr = t.idTUr
                    join DostawcaSprzetu d on du.DostawcaSprzetu_nip = d.nip
                    where t.nazwa_typu = """ + "'" + eq + "'"
        self.cur.execute(query)
        return self.cur.fetchall()

    def add_eq(self, eq_type_id):
        query = """insert into urzadzenie (data_zakupu, typurzadzenia_idtur)
                   values (sysdate, """ + str(eq_type_id) + ")"
        self.cur.execute(query)
        self.con.commit()

    def get_doctors_with_type(self):
        query = """select p.pesel, p.nazwisko, t.specjalizacja from
                   pracownik p left join typpracownika t on
                   p.typpracownika_idtpr = t.idtpr"""
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_pref_hours_doctor(self, doctor_pesel):
        query = """select dzien, TO_CHAR(poczatek, 'HH24:MI:SS'), TO_CHAR(koniec, 'HH24:MI:SS') from PrefGodzP
                   where Pracownik_pesel = """ + str(doctor_pesel)

        self.cur.execute(query)
        return self.cur.fetchall()

    def check_collision(self, employer_id, room_id, begin_h, end_h, day):
        begin_h_t = datetime.strptime("2000-10-10 " + begin_h, "%Y-%m-%d %H:%M:%S")
        end_h_t = datetime.strptime("2000-10-10 " + end_h, "%Y-%m-%d %H:%M:%S")
        query_employer = """select t.dzien_tygodnia, t.poczatek, t.koniec from
                            pracownik p left join
                            terminprzyjec t on p.pesel = t.pracownik_pesel
                            where p.pesel= """ + str(employer_id)
        self.cur.execute(query_employer)
        empl_col = self.cur.fetchall()
        query_room = """select t.dzien_tygodnia, t.poczatek, t.koniec from
                        gabinet g left join
                        terminprzyjec t on g.idgab = t.gabinet_idgab
                        where idGab = """ + str(room_id)
        self.cur.execute(query_room)
        room_col = self.cur.fetchall()
        for dates in empl_col + room_col:
            if dates[1] is None and dates[2] is None:
                self._add_term_visit(employer_id, day, begin_h, end_h, room_id)
                return True
            if ((dates[1] < begin_h_t < dates[2]) or (dates[1] < end_h_t < dates[2])) and day == dates[0]:
                return False
            if ((begin_h_t < dates[1] < end_h_t) or (begin_h_t < dates[2] < end_h_t)) and day == dates[0]:
                return False
        self._add_term_visit(employer_id, day, begin_h, end_h, room_id)
        return True

    def get_rooms_with_type(self):
        query = """select g.idGab, g.nr_pietra, g.nr_pokoju, t.nazwa_rodzaju_gabinetu from gabinet g
                   left join typgabinetu t on g.TypGabinetu_idTGab = t.idtgab"""
        self.cur.execute(query)
        return self.cur.fetchall()

    def _add_term_visit(self, employer_pesel, weekday, start_h, end_h, room_id):
        query = "insert into terminprzyjec (pracownik_pesel, dzien_tygodnia, " + \
                "poczatek, koniec, gabinet_idgab) values (" + \
                str(employer_pesel) + ",'" + weekday + "'," + \
                "TO_DATE('2000-10-10 " + start_h + "', 'YYYY-MM-DD HH24:MI:SS'), " + \
                "TO_DATE('2000-10-10 " + end_h + "', 'YYYY-MM-DD HH24:MI:SS'), " + str(room_id) + ")"
        print(query)
        self.cur.execute(query)
        self.con.commit()

if __name__ == "__main__":
    provider = DbDataProvider()
    print(provider.get_doctors_with_type())
    print(provider.get_pref_hours_doctor(95102812345))
    print(provider.get_eq_providers_with_eq("stroboskop"))
    print(provider.get_eq_providers_with_eq("Kardiogram"))
    print(provider.get_rooms_with_type())

    print(provider.get_type_eqs_by_time(3))
    # provider.add_eq(1)
    # provider.add_term_visit(95102812345, "pon", "11:00:00", "12:00:00", 1)
    print(provider.check_collision(95102812345, 1, "11:30:00", "11:45:00", "pon"))
