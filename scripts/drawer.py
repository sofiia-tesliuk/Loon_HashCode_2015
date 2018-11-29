import chartify
from pandas import DataFrame


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
        if satelite.r < 0 or satelite.r >= self.size_r:
            return None
        satelite.c %= size.c
        self.datafr.ix[satelite.r * self.size_c + satelite.c, 'satelite'] += 1
        for r1 in range(satelite.r - self.radius, satelite.r + self.radius + 1):
            if r1 < 0 or r1 >= self.size_r:
                continue
            for c1 in range(satelite.c - self.radius, satelite.c + self.radius + 1):
                if c1 < 0 or c1 >= self.size_c:
                    c1 = c1 % self.size_c
                if (satelite.r - r1)**2 + self.columndist(satelite.c, c1)**2 <= self.radius**2:
                    self.datafr.ix[r1 * self.size_c + c1, 'covered'] = True

    def count_targets(self):
        return sum(self.datafr['target'] & self.datafr['covered'])

    def draw(self):
        for index, row in self.datafr.iterrows():
            self.datafr.ix[index, 'value'] = row['target'] + row['covered']*2 + row["satelite"]*2
        (chartify.Chart(blank_labels=True, x_axis_type='categorical', y_axis_type='categorical')
            .plot.heatmap(
            data_frame=self.datafr,
            x_column='latitude',
            y_column='longitude',
            color_column='value',
            text_color='white')
            .axes.set_xaxis_label('latitude')
            .axes.set_yaxis_label('longitude')
            .set_title('Earth')
            .set_subtitle('Score: ' + str(self.count_targets()))
            .show('html'))

    def redraw(self, satelites):
        del self.datafr
        self.datafr = self.dforig.copy()
        for satelite in satelites:
            self.place_sputnkik(satelite)
        self.draw()
