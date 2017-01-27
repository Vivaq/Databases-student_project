import cx_Oracle


class DbDataProvider(object):
    def __init__(self, db_address="ora3.elka.pw.edu.pl", username="kmagryta", passw="kmagryta"):
        dsn_str = cx_Oracle.makedsn(db_address, "1521", "ora3inf")
        self.con = cx_Oracle.connect(user=username, password=passw, dsn=dsn_str)
        self.cur = self.con.cursor()

    def get_type_eqs_by_time(self, time):
        query = """select tu.nazwa_typu, count(*)
                   from typurzadzenia tu join
                   urzadzenie u on tu.idTUr = u.TypUrzadzenia_idTUr join
                   zaburz zu on zu.urzadzenie_idUr = u.idUr  join
                   Zabieg z on zu.Zabieg_idZ = z.idZ
                   where (select trunc(sysdate - z.koniec) as days from dual) <=
                   """ + str(time) +  "group by tu.nazwa_typu";
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
        query = """INSERT INTO "KMAGRYTA"."URZADZENIE" (DATA_ZAKUPU, TYPURZADZENIA_IDTUR)
                   VALUES (sysdate, """ + str(eq_type_id) + ")"
        self.cur.execute(query)

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
    print(provider.get_pref_hours_doctor(95102812345))
    print(provider.get_eq_providers_with_eq("stroboskop"))
    print(provider.get_eq_providers_with_eq("Kardiogram"))
    print(provider.get_rooms_with_type())
    print(provider.get_type_eqs_by_time(3))
    provider.add_eq(1)