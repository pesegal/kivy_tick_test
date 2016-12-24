from kivy.uix.boxlayout import BoxLayout
from kivy.base import runTouchApp
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.garden.tickline import Tickline, Tick, LabellessTick, DataListTick


class TestTickLine(Tickline):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min_index = -1
        self.max_index = 20

    def redraw_(self, *args):
        super().redraw_(*args)
        print(self.pos2index(40, True))


class TestTick(Tick):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



if __name__ == '__main__':
    tl = TestTickLine(ticks=[TestTick()],
                             orientation='horizontal',
                             backward=False,
                             min_index=0,
                             max_index=10,
                             draw_line=False)

    b = BoxLayout(padding=[10, 10, 10, 10], orientation='vertical')

    


    b.add_widget(tl)
    runTouchApp(b)

    # TODO: Figure out how we can overwrite the custom data tick and draw ticks that have longer distances.