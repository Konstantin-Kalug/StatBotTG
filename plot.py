import matplotlib.pyplot as plt
import numpy as np
from random import choice


class Plot:
    def __init__(self, title, xlabel, ylabel, color, type, legend, info):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.color = color
        self.type = type
        self.info = info.split('\n')
        self.legend = legend
        self.COLORS = {'Синий': 'b', 'Зеленый': 'g', 'Красный': 'r', 'Голубой': 'c',
                       'Фиолетовый': 'm', 'Желтый': 'y', 'Черный': 'k', 'Белый': 'w'}
        self.change_color_type()

    def change_color_type(self):
        if self.color == 'Любые':
            self.color = list(self.COLORS.values())
        else:
            self.color = self.COLORS[self.color]

    def get_elements(self):
        elems = {}
        for i in range(len(self.info)):
            if self.info[i].split()[0][:-1].isdigit():
                elems[self.info[i].split()[0] + self.info[i].split()[1]] =\
                    float(self.info[i].split()[-1])
        return elems

    def create_figure(self, address):
        try:
            elems = self.get_elements()
            if type(self.color) == list:
                self.color = [choice(self.color) for _ in range(len(self.color))]
            plt.figure(figsize=(5 * len(elems.keys()), 5 * len(elems.keys())))
            plt.title(self.title)
            plt.xlabel(self.xlabel)
            plt.ylabel(self.ylabel)
            if self.type == 'Столбчатая':
                plt.bar(list(elems.keys()), list(elems.values()), color=self.color)
            else:
                plt.pie(list(elems.values()), labels=list(elems.keys()))
            if self.legend:
                plt.legend()
            plt.savefig(address)
        except Exception:
            return -1
