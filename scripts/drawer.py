#import chartify
from pandas import DataFrame
from bokeh.io import show
from bokeh.models import LinearColorMapper, BasicTicker, PrintfTickFormatter, ColorBar
from bokeh.plotting import figure


class Drawer:
    def __init__(self, target_cells, satelites, c, r, radius):
        self.size_c = c
        self.size_r = r
        self.radius = radius
        dic = {'latitude': [], 'longitude': [], 'target': [], 'value': [], 'covered': [], 'satelite': []}
        for y in range(self.size_r):
            for x in range(self.size_c):
                dic['latitude'].append(x)
                dic['longitude'].append(y)
                dic['value'].append(0)
                dic['target'].append(False)
                dic['covered'].append(False)
                dic['satelite'].append(0)

        self.dforig = DataFrame(data=dic)
        for target in target_cells:
            self.place_target(target)
        self.datafr = self.dforig.copy()
        for satelite in satelites:
            self.place_sputnkik(satelite)

    def place_target(self, target):
        self.dforig.ix[target.r * self.size_c + target.c, 'target'] = True

    def columndist(self, y1, y2):
        return min(abs(y1 - y2), self.size_c - abs(y1 - y2))

    def place_sputnkik(self, satelite):
        if satelite.r == None:
            return None
        self.datafr.ix[satelite.r * self.size_c + satelite.c, 'satelite'] += 1
        for r1 in range(satelite.r - self.radius, satelite.r + self.radius + 1):
            if r1 < 0 or r1 >= self.size_r:
                continue
            for c1 in range(satelite.c - self.radius, satelite.c + self.radius + 1):
                if c1 < 0 or c1 >= self.size_c:
                    c1 = c1 % self.size_c
                if (satelite.r - r1)**2 + self.columndist(satelite.c, c1)**2 <= self.radius**2:
                    self.datafr.ix[r1 * self.size_c + c1, 'covered'] = True

    def draw(self, score):
        for index, row in self.datafr.iterrows():
            self.datafr.ix[index, 'value'] = row['target'] + row['covered']*2
            '''
        (chartify.Chart(blank_labels=True, x_axis_type='categorical', y_axis_type='categorical')
            .plot.heatmap(
            data_frame=self.datafr,
            x_column='latitude',
            y_column='longitude',
            color_column='value',
            text_column='satelite',
            text_color='white')
            .axes.set_xaxis_label('latitude')
            .axes.set_yaxis_label('longitude')
            .set_title('Earth')
            .set_subtitle('Score: ' + str(score))
            .show('html'))
            '''
        colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
        mapper = LinearColorMapper(palette=colors, low=0, high=self.datafr.value.max())
        TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"
        p = figure(title="Earth",
                   x_range=list(str(x) for x in set(self.datafr.latitude)),
                   y_range=list(str(y) for y in set(self.datafr.longitude)),
                   x_axis_location="above", plot_width=1200, plot_height=300,
                   tools=TOOLS, toolbar_location='below')

        p.axis.axis_line_color = None
        p.axis.major_tick_line_color = None
        p.axis.major_label_text_font_size = "5pt"
        p.axis.major_label_standoff = 0
        p.xaxis.major_label_orientation = 3.14 / 3

        p.rect(x="latitude", y="longitude", width=1, height=1,
               source=self.datafr,
               fill_color={'field': 'value', 'transform': mapper},
               line_color=None)

        color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                             ticker=BasicTicker(desired_num_ticks=len(colors)),
                             formatter=PrintfTickFormatter(format="%d%%"),
                             label_standoff=6, border_line_color=None, location=(0, 0))
        p.add_layout(color_bar, 'right')

        show(p)

    def redraw(self, satelites, score):
        del self.datafr
        self.datafr = self.dforig.copy()
        for satelite in satelites:
            self.place_sputnkik(satelite)
        self.draw(score)
