import gtk


class TestWindow(gtk.Window):

    def __init__(self, *args, **kwargs):
        gtk.Window.__init__(self, *args, **kwargs)
        self.connect("destroy", gtk.main_quit)
        self.is_allowed = True
        self.create_widgets()
        self.show_all()

    def create_widgets(self):
        box = gtk.HBox()
        self.entry = gtk.Entry()
        self.handler_id = self.entry.connect("changed", self.on_entry_changed)
        box.pack_start(self.entry, True, True, 0)
        button = gtk.Button("Toggle")
        button.connect("clicked", self.on_button_clicked)
        box.pack_start(button, True, True, 0)
        self.add(box)

    def on_entry_changed(self, *args):
        print "entry has changed"

    def on_button_clicked(self, *args):
        if self.is_allowed:
            self.entry.handler_block(self.handler_id)
            print "now blocking"
        else:
            self.entry.handler_unblock(self.handler_id)
            print "now unblocking"
        self.is_allowed = not self.is_allowed

TestWindow()
gtk.main()