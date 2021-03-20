import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from datetime import datetime
import requests


class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.init_main()
        self.data = None
    
    # инициализация GUI 
    def init_main(self):
        # экземпляр фигуры для построения графика
        self.figure = plt.figure()

        # Canvas Widget отображающий `figure`
        # он принимает экземпляр `figure` в качестве параметра __init__
        self.canvas = FigureCanvas(self.figure)

        # кнопка для построения графика за 7 дней
        self.btn_timespan_7_days = QPushButton('7 дней')
        self.btn_timespan_7_days.clicked.connect(lambda: self.get_data_plot('7days'))

        # кнопка для построения графика за 30 дней
        self.btn_timespan_30_days = QPushButton('30 дней')
        self.btn_timespan_30_days.clicked.connect(lambda: self.get_data_plot('30days'))

        # кнопка для построения графика за 90 дней
        self.btn_timespan_90_days = QPushButton('90 дней')
        self.btn_timespan_90_days.clicked.connect(lambda: self.get_data_plot('90days'))

        # кнопка для построения графика за 1 год
        self.btn_timespan_1_year = QPushButton('1 год')
        self.btn_timespan_1_year.clicked.connect(lambda: self.get_data_plot('1year'))

        # кнопка для построения графика за 3 год
        self.btn_timespan_3_years = QPushButton('3 года')
        self.btn_timespan_3_years.clicked.connect(lambda: self.get_data_plot('3year'))

        # кнопка для построения графика c 2013 года
        self.btn_timespan_all_time = QPushButton('За все время')
        self.btn_timespan_all_time.clicked.connect(lambda: self.get_data_plot('8year'))

        # кнопка вызова функции построения графика
        self.btn_plot = QPushButton('Построить график')
        self.btn_plot.clicked.connect(self.plot)

        # создаем вертикальный контейнер и помещаем виджеты
        vertical_layout = QVBoxLayout()

        # создаем горизонтальный контейнер и помещаем виджеты       
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.btn_timespan_7_days)
        horizontal_layout.addWidget(self.btn_timespan_30_days)
        horizontal_layout.addWidget(self.btn_timespan_90_days)
        horizontal_layout.addWidget(self.btn_timespan_1_year)
        horizontal_layout.addWidget(self.btn_timespan_3_years)
        horizontal_layout.addWidget(self.btn_timespan_all_time)
        horizontal_layout.addWidget(self.btn_plot)

        vertical_layout.addLayout(horizontal_layout)
        vertical_layout.addWidget(self.canvas)

        self.setLayout(vertical_layout)

    # функция получения данных через API и периода получаемых цен
    def get_data_plot(self, timespan):  
        # получаем значение в годах из поля ввода timespan
        # запрос и получение данных через API blockchain.com
        url = 'https://api.blockchain.info/charts/market-price'
        params = {'timespan': timespan, 'rollingAverage': '8hours', 'format': 'json'}
        response = requests.get(url, params=params)
        self.data = response.json()
    
    # обработка полученных JSON данных
    def data_plot(self):
        x_list = []
        y_list = []
        for item in self.data["values"]:
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
        #plt.title('График рыночной стоимости Bitcoin', fontsize=14, fontweight='bold', color='blue')
        # наименование осей координат
        #plt.xlabel('Период', fontsize=12, color='black')
        #plt.ylabel('Рыночная стоимость, $', fontsize=12, color='black')
        # построение линейного графика
        ax.plot(*self.data_plot(), label="Рыночная цена")
        ax.fill_between(*self.data_plot(), alpha=.1)
        ax.yaxis.set_major_formatter('${x:1.0f}')
        # легенда графика
        ax.legend()
        # сетка графика
        ax.grid()
        # обновляем canvas
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.setWindowTitle('BTC market price')
    main.resize(1280, 720)
    main.show()
    sys.exit(app.exec_())
