import gtk


class GuiApp(gtk.Window):

    def __init__(self):
        super(GuiApp, self).__init__()
        self.set_title("Klinika")
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_default_size(250, 200)
        self.button_w = 100
        self.button_h = 50
        self.margin = 20
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_resizable(False)
        self.vbox = None

        mb = gtk.MenuBar()
        menu = gtk.Menu()
        opcje = gtk.MenuItem("menu")
        opcje.set_submenu(menu)
        wroc = gtk.ImageMenuItem("Powrot")
        wroc.connect("activate", self.go_back)

        menu.append(wroc)

        shutdown = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        menu.append(shutdown)

        mb.append(opcje)

        self.vb = gtk.VBox(False, 2)
        self.vb.pack_start(mb, False, False, 0)

        self.initial_buttons = ['Zaplanuj operacje', 'Kup urzadzenie']
        self.add_buttons(self.initial_buttons)

    def add_buttons(self, blist):
        self.vbox = gtk.VButtonBox()
        for label in blist:
            button = gtk.Button(stock=label)
            button.set_size_request(self.button_w, self.button_h)
            button.connect("clicked", self.go_next)
            self.vbox.pack_start(button, True, True, 0)
        self.vb.add(self.vbox)
        self.add(self.vb)
        self.set_size_request(200, len(blist) * (self.button_h + self.margin) - self.margin + 30)
        self.show_all()

    def go_next(self, widget, data=None):
        self.vb.remove(self.vbox)
        self.remove(self.vb)
        self.add_buttons(['a', 'b', 'c', 'd', 'e'])

    def go_back(self, widet, data=None):
        self.remove(self.vb)
        self.__init__()

GuiApp()
gtk.main()

