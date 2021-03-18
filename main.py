import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QLineEdit

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from datetime import datetime
import requests


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.init_main()
    
    # инициализация GUI 
    def init_main(self):
        # экземпляр фигуры для построения графика
        self.figure = plt.figure()

        # Canvas Widget отображающий `figure`
        # он принимает экземпляр `figure` в качестве параметра __init__
        self.canvas = FigureCanvas(self.figure)

        # Поле ввода периода цен
        self.timespan = QLineEdit()
        self.timespan.setPlaceholderText('Введите период в годах:')

        # кнопка вызова функции построения графика
        self.button = QPushButton('Построить график')
        self.button.clicked.connect(self.plot)

        # создаем вертикальный контейнер и помещаем виджеты
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.timespan)
        layout.addWidget(self.button)
        self.setLayout(layout)

    # функция получения данных через API и периода получаемых цен
    def get_data_plot(self):     
        # получаем значение в годах из поля ввода timespan 
        time = self.timespan.text()        
        # запрос и получение данных через API blockchain.com
        url = 'https://api.blockchain.info/charts/market-price'
        params = {'timespan': '10year', 'rollingAverage': '8hours', 'format': 'json'}
        params['timespan'] = time + 'year'
        response = requests.get(url, params=params)
        data = response.json()
        return data

        # чтение данных из JSON файла
        #with open('market_price.json') as file:
            #data = json.load(file)
    
    # обработка полученных JSON данных
    def data_plot(self):
        data = self.get_data_plot()
        x_list = []
        y_list = []
        for item in data["values"]:
            x_list.append(datetime.utcfromtimestamp(item['x']))
            y_list.append(item['y'])
        return x_list, y_list
    
    # функция построения графика
    def plot(self):
        # очистка экземпляра фигуры перед построением графика
        self.figure.clear()
        # создание координатной плоскости
        ax = self.figure.add_subplot(111)
        # заголовок графика
        plt.title('График рыночной стоимости Bitcoin', fontsize=14, fontweight='bold', color='blue')
        # наименование осей координат
        plt.xlabel('Период, год', fontsize=12, color='black')
        plt.ylabel('Рыночная стоимость, $', fontsize=12, color='black')
        # сетка графика
        ax.grid()
        # построение линейного графика
        ax.plot(*self.data_plot(), label="Рыночная цена")
        # легенда графика
        ax.legend()
        # обновляем canvas
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.resize(1280, 720)
    main.show()
    sys.exit(app.exec_())
