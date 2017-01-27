import gtk
from dataprovision.db_providers import DbDataProvider

buy_list = {}
plan_list = {}
tv = gtk.TextView()
days = gtk.Entry(max=0)
day = gtk.Entry(max=0)
start_h = gtk.Entry(max=0)
end_h = gtk.Entry(max=0)
db_conn = DbDataProvider()


class GuiApp(gtk.Window):

    def __init__(self):
        super(GuiApp, self).__init__()
        self.set_title("Klinika")
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_default_size(250, 200)
        self.button_w = 500
        self.button_h = 100
        self.margin = 100
        self.set_position(gtk.WIN_POS_CENTER)
        self.vbox = None
        self.parameter = ''

        mb = gtk.MenuBar()
        menu = gtk.Menu()
        opcje = gtk.MenuItem("menu")
        opcje.set_submenu(menu)
        wroc = gtk.ImageMenuItem("Powrot")
        wroc.connect("activate", self.go_back)

        menu.append(wroc)

        shutdown = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        shutdown.connect("activate", exit)
        menu.append(shutdown)

        mb.append(opcje)

        self.vb = gtk.VBox(False, 2)
        self.vb.pack_start(mb, False, False, 0)

        self.initial_buttons = {'Zaplanuj operacje': self.list_docs, 'Kup urzadzenie': self.enter_days}
        self.vbox = gtk.VButtonBox()
        self.add_buttons(self.initial_buttons)
        self.set_size_request(500, 200)

    def add_buttons(self, blist):
        #self.vbox = gtk.VButtonBox()
        for bf_tuple in blist.items():
            button = gtk.Button(stock=bf_tuple[0])
            button.set_size_request(self.button_w, self.button_h)
            button.connect("clicked", bf_tuple[1])
            self.vbox.pack_start(button, True, True, 0)
        self.vb.add(self.vbox)
        self.add(self.vb)
        #self.set_size_request(200, len(blist) * (self.button_h + self.margin) - self.margin + 30)
        self.show_all()

    def enter_days(self, widget, data=None):
        self.vb.remove(self.vbox)
        self.remove(self.vb)
        self.vbox = gtk.VButtonBox()
        label = gtk.Label()
        txt = 'Liczba uwzglednianych dni:'
        label.set_markup(txt)
        self.vbox.add(label)
        self.vbox.add(days)
        self.add_buttons({'dalej': self.buy})

    def buy(self, widget, data=None):
        days_num = int(self.vbox.children()[1].get_text())
        self.vb.remove(self.vbox)
        self.remove(self.vb)
        self.vbox = gtk.VButtonBox()
        d = {}
        for x in db_conn.get_type_eqs_by_time(days_num):
            x = x[0] + ' ' + str(x[1])
            d[x] = self.suppliers
        self.add_buttons(d)

    def suppliers(self, widget, data=None):
        buy_list['type'] = widget.get_label()
        self.vb.remove(self.vbox)
        self.remove(self.vb)
        self.vbox = gtk.VButtonBox()
        d = {}
        for x in db_conn.get_eq_providers_with_eq(buy_list['type'].split(' ')[0]):
            x = x[1] + ' ' + str(x[2])
            d[x] = self.finalize
        self.add_buttons(d)

    def finalize(self, widget):
        buy_list['supplier'] = widget.get_label()
        self.vb.remove(self.vbox)
        self.remove(self.vb)
        self.vbox = gtk.VButtonBox()
        self.add_buttons({'Powodzenie!': self.go_back})

    def list_docs(self, widget):
        self.vb.remove(self.vbox)
        self.remove(self.vb)
        self.vbox = gtk.VButtonBox()
        d = {}
        for x in db_conn.get_doctors_with_type():
            x = x[1] + ' ' + x[2] + ' ' + str(x[0])
            d[x] = self.list_rooms
        self.add_buttons(d)

    def list_rooms(self, widget):
        plan_list['doc'] = widget.get_label()
        self.vb.remove(self.vbox)
        self.remove(self.vb)
        self.vbox = gtk.VButtonBox()
        d = {}
        for x in db_conn.get_rooms_with_type():
            x = str(x[0]) + ' ' + str(x[1]) + ' ' + x[2]
            d[x] = self.show_days
        self.add_buttons(d)

    def show_days(self, widget):
        self.vb.remove(self.vbox)
        self.remove(self.vb)
        self.vbox = gtk.VButtonBox()
        label = gtk.Label()
        # label.set_use_markup(True)
        txt = 'Preferowane godziny przyjec:\n\n'
        label.set_markup(txt)
        label = gtk.Label()
        for i in db_conn.get_pref_hours_doctor(plan_list['doc'].split(' ')[2]):
            txt += '\t' + i[0] + ' ' + i[1] + ' ' + i[2] + '\n'
        label.set_markup(txt)
        self.vbox.add(label)
        self.add_buttons({'dalej': self.plan})

    def plan(self, widget, data=None):
        plan_list['room'] = widget.get_label()
        self.vb.remove(self.vbox)
        self.remove(self.vb)
        self.vbox = gtk.VButtonBox()
        label = gtk.Label()
        # label.set_use_markup(True)
        txt = 'Dzien tygodnia:'
        label.set_markup(txt)
        self.vbox.add(label)
        self.vbox.add(day)
        label = gtk.Label()
        # label.set_use_markup(True)
        txt = 'Data rozpoczecia:'
        label.set_markup(txt)
        self.vbox.add(label)
        self.vbox.add(start_h)
        label = gtk.Label()
        # label.set_use_markup(True)
        txt = 'Data zakonczenia:'
        label.set_markup(txt)
        self.vbox.add(label)
        self.vbox.add(end_h)

        self.add_buttons({'dalej': self.check_collisions})

    def check_collisions(self, texts):
        childs = []
        for child in enumerate(self.vbox.children()):
            if child[0] % 2 == 1:
                childs.append(child[1])
        for child in zip(['day', 'start_h', 'end_h'], child):
            plan_list[child[0]] = child[1].get_text()
        print plan_list
        self.vb.remove(self.vbox)
        self.remove(self.vb)
        self.vbox = gtk.VButtonBox()
        if db_conn.check_collision(plan_list[''], plan_list['room']):
            self.add_buttons({'Powodzenie!': self.go_back})
        else:

            self.add_buttons({'Niepowodzenie, wykryto kolizje': self.go_back})

    def go_back(self, widet, data=None):
        self.remove(self.vb)
        self.__init__()

GuiApp()
gtk.main()
