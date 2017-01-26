import cx_Oracle


class DbDataProvider(object):
    def __init__(self, db_address="ora3.elka.pw.edu.pl", username="kmagryta", passw="kmagryta"):
        dsn_str = cx_Oracle.makedsn(db_address, "1521", "ora3inf")
        self.con = cx_Oracle.connect(user=username, password=passw, dsn=dsn_str)
        self.cur = self.con.cursor()

    def get_type_eqs_by_time(self, time):
        query = """ select t.nazwa_typu, count(*)
                    from typurzadzenia t join
                    urzadzenia u on t.TypUrzadzenia_idTUr = u.idTUr join
                    Z_U zu on zu.Urzadzenie_TypUrzadzenia_idTUr = u.idTUr  join
                    Zabieg z on zu.Zabieg_idZ = z.idZ
                    where day(z.date_) >= """ + str(time) + "group by t.nazwa_typu"
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_eq_providers_with_eq(self, eq):
        query = """	select t.nazwa_typu, d.nazwa_firmy, d.nip
                    from typurzadzenia t join typurzdos du on du.TypUrzadzenia_idTUr = t.idTUr
                    join DostawcaSprzetu d on du.DostawcaSprzetu_idD = d.idD
                    where t.nazwa_typu = """ + "'" + eq + "'"
        self.cur.execute(query)
        return self.cur.fetchall()

    def add_eqs(self, eq_type_list):
        for type in eq_type_list:
            query = "insert into Urzadzenia values(sysdate," + type + ")"
            self.cur.execute(query)

    def get_doctors_with_type(self):
        query = """select p.pesel, p.nazwisko, t.specjalizacja from
                   pracownik p left join typpracownika t on
                   p.typpracownika_idtpr = t.idtpr"""
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_pref_hours_doctor(self, doctor_pesel):
        query = """select dzien, TO_CHAR(\"start\", 'HH24:MI:SS'), TO_CHAR(koniec, 'HH24:MI:SS') from PrefGodzP
                   where Pracownik_pesel = """ + str(doctor_pesel)

        self.cur.execute(query)
        return self.cur.fetchall()

    def check_collision(self, employer_id, room_id):
        query_employer = """select t.dzientygodnia, t.poczatek, t.koniec from
                            pracownik p where pesel=""" + employer_id + """left join
                            terminprzyjec t on p.idprac = t.pracownik_idprac"""
        empl_col = self.cur.execute(query_employer)
        query_room = """select t.dzientygodnia, t.poczatek, t.koniec from
                        gabinet g where idGab = """ + room_id + """ left join
                        terminprzyjec t on p.idgab = t.gabinet_idgab"""
        room_col = self.cur.fetchall()
        # TODO - Alghorithm.
        return True

    def get_rooms_with_type(self):
        query = """select g.nr_pietra, g.nr_pokoju, t.nazwa_rodzaju_gabinetu from gabinet g
                   left join typgabinetu t on g.TypGabinetu_idTGab = t.idtgab"""
        self.cur.execute(query)
        return self.cur.fetchall()

    def add_term_visit(self, employer_id, weekday, next_, start_h, end_h):
        query = "insert into terminprzyjec values (" + employer_id + ","  + weekday + "," + next_+ "," + \
        "," + start_h + "," + end_h + ")"
        self.cur.execute(query)

if __name__ == "__main__":
    provider = DbDataProvider()
    print(provider.get_doctors_with_type())
    print(provider.get_pref_hours_doctor(1))
    print(provider.get_eq_providers_with_eq("stroboskop"))
    print(provider.get_eq_providers_with_eq("kardiogram"))
    print(provider.get_rooms_with_type())