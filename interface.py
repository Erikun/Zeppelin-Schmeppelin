from pgu import gui

class OrderControl(gui.Table):
    def __init__(self,**params):
        gui.Table.__init__(self,background=(255,255,255),**params)

        def orders_finished(doh):
            self.done = True

        #orders = []
        fg = (0,0,0)

        self.done = False

        self.tr()
        self.td(gui.Label("Your orders, sir?",color=fg),colspan=2)

        self.tr()
        self.td(gui.Label("AIRSHIP 1",color=(255,0,0)), colspan=2)

        self.tr()
        self.td(gui.Label("Speed: ",color=fg),align=1)
        e = gui.HSlider(0,-10000,30000, step=1000,
                        size=20,width=100,height=16,name='speed1')
        self.td(e)

        self.tr()
        self.td(gui.Label("Turn: ",color=fg),align=1)
        e = gui.HSlider(0,-50,50,step=10,
                        size=20,width=100,height=16,name='turn1')
        self.td(e)

        self.tr()
        self.td(gui.Label("AIRSHIP 2",color=(0,255,0)), colspan=2)

        self.tr()
        self.td(gui.Label("Speed: ",color=fg),align=1)
        e = gui.HSlider(0,-10000,30000,step=1000,
                        size=20,width=100,height=16,name='speed2')
        self.td(e)

        self.tr()
        self.td(gui.Label("Turn: ",color=fg),align=1)
        e = gui.HSlider(0,-50,50, step=10,
                        size=20,width=100,height=16,name='turn2')
        self.td(e)

        self.tr()
        self.td(gui.Label("SIRSHIP 3",color=(0,0,255)),colspan=2)

        self.tr()
        self.td(gui.Label("Speed: ",color=fg),align=1)
        e = gui.HSlider(0,-10000,30000, step=1000,
                        size=20,width=100,height=16,name='speed3')
        self.td(e)

        self.tr()
        self.td(gui.Label("Turn: ",color=fg),align=1)
        e = gui.HSlider(0,-50, 50, step=10,
                        size=20,width=100,height=16,name='turn3')
        self.td(e)

        self.tr()
        self.btn = gui.Button("Make it so!")
        self.td(self.btn, colspan=2)
        #self.btn.connect(gui.CHANGE, fullscreen_changed, btn)
        self.btn.connect(gui.CLICK, orders_finished, None)

