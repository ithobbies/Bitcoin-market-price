import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from datetime import datetime
import requests


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # экземпляр фигуры для построения графика
        self.figure = plt.figure()

        # Canvas Widget отображающий `figure`
        # он принимает экземпляр `figure` в качестве параметра __init__
        self.canvas = FigureCanvas(self.figure)

        # кнопка вызова функции построения графика
        self.button = QPushButton('Построить график')
        self.button.clicked.connect(self.plot)

        # создаем вертикальный контейнер и помещаем виджеты
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def get_data_plot(self):        
        # запрос и получение данных через API blockchain.com
        url = 'https://api.blockchain.info/charts/market-price'
        params = {'timespan': '10year', 'rollingAverage': '8hours', 'format': 'json'}
        response = requests.get(url, params=params)
        data = response.json()

        # чтение данных из JSON файла
        #with open('market_price.json') as file:
            #data = json.load(file)

        x_list = []
        y_list = []
        for item in data["values"]:
            x_list.append(datetime.utcfromtimestamp(item['x']))
            y_list.append(item['y'])
        return x_list, y_list
    
    def plot(self, x_list, y_list): 
        # создание координатной плоскости
        ax = self.figure.add_subplot(111)
        # построение линейного графика
        ax.plot(x_list, y_list)
        # обновляем canvas
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
