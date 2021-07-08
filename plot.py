class Plot:
    def __init__(self, title, xlabel, ylabel, color, type, legend, info):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.color = color
        self.type = type
        self.info = info
        self.COLORS = {'Синий': 'b', 'Зеленый': 'g', 'Красный': 'r', 'Голубой': 'c',
                       'Фиолетовый': 'm', 'Желтый': 'y', 'Черный': 'k', 'Белый': 'w'}
        self.change_color_type()
        self.create_figure()

    def change_color_type(self):
        if self.color == 'Любые':
            self.color = list(self.COLORS.values())
        else:
            self.color = self.COLORS[self.color]

    def create_figure(self):
        pass
