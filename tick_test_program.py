

from kivy.uix.boxlayout import BoxLayout
from kivy.base import runTouchApp
from kivy.graphics import Mesh, InstructionGroup
from kivy.graphics.context_instructions import Color
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.garden.tickline import Tickline, Tick, LabellessTick, DataListTick
from kivy.properties import ListProperty
from bisect import bisect_left
from kivy.metrics import sp


test_data = [
    (1, 3),
    (6, 6.5),
    (7, 8),
    (9.5, 11),
    (11, 12),
    (14, 15)
]


class TestTickLine(Tickline):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.min_index = -1
        self.max_index = 20

    def redraw_(self, *args):
        super().redraw_(*args)
        print(self.index_0, self.index_1, self.scale)


class TestRangeDisplayTick(Tick):

    data_ranges = ListProperty([])
    #tick_size = ListProperty([])

    def __init__(self, *args, **kw):
        self._mesh = Mesh(mode='triangle_strip')
        self._color = Color(*self.tick_color)
        self.instr = instr = InstructionGroup()
        instr.add(self._color)
        instr.add(self._mesh)
        super(Tick, self).__init__(*args, **kw)

        self.data_ranges_idx = list()
        for item in self.data_ranges:
            self.data_ranges_idx.append(item[0])

    def display(self, tickline):
        super().display(tickline)

    def draw(self, tickline, tick_info):
        tick_pos, tick_index, tick_data = tick_info

        x = tick_pos
        y = tickline.line_pos

        t_start = tickline.index2pos(self.globalize(tick_data[0]))
        t_end = tickline.index2pos(self.globalize(tick_data[1]))

        width = float(t_end - t_start)
        print("T-start: ", t_start, "T_end: ", t_end, "Width: ", width)
        height = sp(20)

        self._vertices.extend([x, y, 0, 0,
                               x + width, y, 0, 0,
                               x + width, y + height, 0, 0,
                               x, y + height, 0, 0,
                               x, y, 0, 0,
                               x + width, y, 0, 0, ])

        tick_rect = (x, y, width, height)
        tickline.labeller.register(self, tick_index, tick_rect)

    def tick_pos_index_iter(self, tl):
        index_0 = self.localize(self.extended_index_0(tl))
        index_1 = self.localize(self.extended_index_1(tl))
        tick_sc = self.scale(tl.scale)

        if tick_sc < self.min_space:
            raise StopIteration

        try:
            data_index = bisect_left(self.data_ranges_idx, index_1 if tl.backward
            else index_0)
            tick_index = self.data_ranges[data_index][0]  # Pull only the first element of the range for starting x
            condition = self._index_condition(tl, True)
            while condition(tick_index):
                yield (tl.index2pos(self.globalize(tick_index)),
                       tick_index, self.data_ranges[data_index])
                data_index += 1
                tick_index = self.data_ranges[data_index][0]
        except IndexError:
            raise StopIteration


if __name__ == '__main__':
    tl = TestTickLine(ticks=[TestRangeDisplayTick(valign='line_bottom', data_ranges=test_data)],  # 7, 8, 9.5, 11, 12, 14, 15
                     orientation='horizontal',
                     backward=False,
                     min_index=0,
                     max_index=10,
                     draw_line=False)

    b = BoxLayout(padding=[10, 10, 10, 10], orientation='vertical')

    


    b.add_widget(tl)
    runTouchApp(b)

    # TODO: Figure out how we can overwrite the custom data tick and draw ticks that have longer distances.