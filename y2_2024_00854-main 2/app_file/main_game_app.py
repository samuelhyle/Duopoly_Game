import sys
from PySide6.QtCore import Qt, Slot, QPointF
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (QApplication, QFormLayout, QHeaderView,
                               QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QTableWidget, QTableWidgetItem,
                               QVBoxLayout, QWidget, QListWidget, QGridLayout, QTextEdit, QLabel, QTabWidget, QSpinBox)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QLineSeries
from stats_analyze import load_states
from move_action import get_moves
from random import randint


class ReactionFunction(QWidget):
    def __init__(self):
        super().__init__()
        self.chart = QChart()

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view_v = QHBoxLayout()
        self.chart_view_v.addWidget(self.chart_view)

        self.chart_label = QLabel("REACTION GRAPH")
        self.label_v = QHBoxLayout()
        self.label_v.addWidget(self.chart_label)
        self.chart_view_vv = QVBoxLayout()
        self.chart_view_vv.addLayout(self.label_v)
        self.chart_view_vv.addLayout(self.chart_view_v)
        self.setLayout(self.chart_view_vv)


class ProfitFunction(QWidget):
    def __init__(self):
        super().__init__()

        self.chart = QChart()

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view_v = QHBoxLayout()
        self.chart_view_v.addWidget(self.chart_view)

        self.chart_label = QLabel("REACTION GRAPH")
        self.label_v = QHBoxLayout()
        self.label_v.addWidget(self.chart_label)
        self.chart_view_vv = QVBoxLayout()
        self.chart_view_vv.addLayout(self.label_v)
        self.chart_view_vv.addLayout(self.chart_view_v)

        self.setLayout(self.chart_view_vv)


class Widget(QWidget):

    def __init__(self):
        super().__init__()
        self.rounds = 0
        self.player_moves = []
        self.co_moves = []
        self.firm_one_profit = 0
        self.firm_two_profit = 0
        self.profit_points_one = []
        self.profit_points_two = []
        self.states = None
        self.round = 1
        self.firm1_best = []
        self.firm2_best = []

        self.table_one = QTableWidget()
        self.table_one.setColumnCount(4)
        self.table_one.setHorizontalHeaderLabels(["W / L / T", "MOVE", "PROFIT", "OUTPUT"])
        self.table_one.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table_one_v = QHBoxLayout()
        self.table_one_v.addWidget(self.table_one)

        self.table_one_label = QLabel("FIRM 1 STATS")
        self.table_one_label_v = QHBoxLayout()
        self.table_one_label_v.addWidget(self.table_one_label)

        self.table_one_f = QVBoxLayout()
        self.table_one_f.addLayout(self.table_one_label_v)
        self.table_one_f.addLayout(self.table_one_v)

        self.table_two = QTableWidget()
        self.table_two.setColumnCount(4)
        self.table_two.setHorizontalHeaderLabels(["W / L / T", "MOVE", "PROFIT", "OUTPUT"])
        self.table_two.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table_two_v = QHBoxLayout()
        self.table_two_v.addWidget(self.table_two)

        self.table_two_label = QLabel("FIRM 2 STATS")
        self.table_two_label_v = QHBoxLayout()
        self.table_two_label_v.addWidget(self.table_two_label)

        self.table_two_f = QVBoxLayout()
        self.table_two_f.addLayout(self.table_two_label_v)
        self.table_two_f.addLayout(self.table_two_v)

        self.rec_f = ReactionFunction()
        self.pro_f = ProfitFunction()

        self.tab = QTabWidget()
        self.tab.addTab(self.rec_f, "REACTION GRAPH")
        self.tab.addTab(self.pro_f, "PROFIT GRAPH")
        self.tabs = QHBoxLayout()
        self.tabs.addWidget(self.tab)
        self.tab.setFixedSize(750, 500)

        self.text_box = QTextEdit()
        self.text_box_v = QHBoxLayout()
        self.text_box_v.addWidget(self.text_box)

        self.text_label = QLabel("GAME DATA")
        self.text_label_v = QHBoxLayout()
        self.text_label_v.addWidget(self.text_label)

        self.text_box_vv = QVBoxLayout()
        self.text_box_vv.addLayout(self.text_label_v)
        self.text_box_vv.addLayout(self.text_box_v)

        self.text_box.setText("Welcome to the Duopoly Game Gym.\n"
                              "To begin please enter the market values down below, and choose the quantity that firm one will produce\n"
                              "Then you can start the game by entering PLAY.")

        self.total_in = QSpinBox()
        self.total_in_v = QHBoxLayout()
        self.total_in_v.addWidget(self.total_in)
        self.total_in.setRange(10, 1000000)

        self.total_in_label = QLabel("INPUT TOTAL INDUSTRY QUANTITY")
        self.total_in_label_v = QHBoxLayout()
        self.total_in_label_v.addWidget(self.total_in_label)

        self.total_f = QVBoxLayout()
        self.total_f.addLayout(self.total_in_label_v)
        self.total_f.addLayout(self.total_in_v)

        self.b_in = QSpinBox()
        self.b_in_v = QHBoxLayout()
        self.b_in_v.addWidget(self.b_in)
        self.b_in.setRange(1, 1000000)

        self.b_in_label = QLabel("INPUT ELASTICITY FACTOR")
        self.b_in_label_v = QHBoxLayout()
        self.b_in_label_v.addWidget(self.b_in_label)

        self.b_f = QVBoxLayout()
        self.b_f.addLayout(self.b_in_label_v)
        self.b_f.addLayout(self.b_in_v)

        self.c1_in = QSpinBox()
        self.c1_in_v = QHBoxLayout()
        self.c1_in_v.addWidget(self.c1_in)
        self.c1_in.setRange(10, 1000000)

        self.c1_in_label = QLabel("INPUT FIRM 1 COST")
        self.c1_in_label_v = QHBoxLayout()
        self.c1_in_label_v.addWidget(self.c1_in_label)

        self.c1_f = QVBoxLayout()
        self.c1_f.addLayout(self.c1_in_label_v)
        self.c1_f.addLayout(self.c1_in_v)

        self.c2_in = QSpinBox()
        self.c2_in_v = QHBoxLayout()
        self.c2_in_v.addWidget(self.c2_in)
        self.c2_in.setRange(10, 1000000)

        self.c2_in_label = QLabel("INPUT FIRM 2 COST")
        self.c2_in_label_v = QHBoxLayout()
        self.c2_in_label_v.addWidget(self.c2_in_label)

        self.c2_f = QVBoxLayout()
        self.c2_f.addLayout(self.c2_in_label_v)
        self.c2_f.addLayout(self.c2_in_v)

        self.c_1 = QHBoxLayout()
        self.c_1.addLayout(self.total_f)
        self.c_1.addLayout(self.b_f)

        self.c_2 = QHBoxLayout()
        self.c_2.addLayout(self.c1_f)
        self.c_2.addLayout(self.c2_f)

        self.inputs = QVBoxLayout()
        self.inputs.addLayout(self.c_1)
        self.inputs.addLayout(self.c_2)

        self.q_input = QSpinBox()
        self.q_input_v = QHBoxLayout()
        self.q_input_v.addWidget(self.q_input)
        self.q_input.setRange(1, 2)

        self.add_q = QPushButton("PLAY")
        self.add_q_v = QHBoxLayout()
        self.add_q_v.addWidget(self.add_q)

        self.input_f = QHBoxLayout()
        self.input_f.addLayout(self.q_input_v)
        self.input_f.addLayout(self.add_q_v)

        self.q_input_label = QLabel(f"ENTER THE PRODUCTION QUANTITY FOR ROUND {self.round}")
        self.q_input_label_v = QHBoxLayout()
        self.q_input_label_v.addWidget(self.q_input_label)

        self.q_f = QVBoxLayout()
        self.q_f.addLayout(self.q_input_label_v)
        self.q_f.addLayout(self.input_f)

        self.table_profits = QTableWidget()
        self.table_profits.setColumnCount(2)
        self.table_profits.setHorizontalHeaderLabels(["1", "2"])
        self.table_profits.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_profits_v = QHBoxLayout()
        self.table_profits_v.addWidget(self.table_profits)

        self.profits_label = QLabel("PROFIT MATRIX ( FIRM 1 / FIRM 2 )")
        self.profits_label_v = QHBoxLayout()
        self.profits_label_v.addWidget(self.profits_label)

        self.table_profits_vv = QVBoxLayout()
        self.table_profits_vv.addLayout(self.profits_label_v)
        self.table_profits_vv.addLayout(self.table_profits_v)

        self.table_output = QTableWidget()
        self.table_output.setColumnCount(2)
        self.table_output.setHorizontalHeaderLabels(["1", "2"])
        self.table_output.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_output_v = QHBoxLayout()
        self.table_output_v.addWidget(self.table_output)

        self.out_label = QLabel("OUTPUT MATRIX ( FIRM 1 / FIRM 2 )")
        self.out_label_v = QHBoxLayout()
        self.out_label_v.addWidget(self.out_label)

        self.table_output_vv = QVBoxLayout()
        self.table_output_vv.addLayout(self.out_label_v)
        self.table_output_vv.addLayout(self.table_output_v)

        self.table_price = QTableWidget()
        self.table_price.setColumnCount(2)
        self.table_price.setHorizontalHeaderLabels(["1", "2"])
        self.table_price.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_price_v = QHBoxLayout()
        self.table_price_v.addWidget(self.table_price)

        self.price_label = QLabel("PRICE MATRIX ( FIRM 1 / FIRM 2 )")
        self.price_label_v = QHBoxLayout()
        self.price_label_v.addWidget(self.price_label)

        self.table_price_vv = QVBoxLayout()
        self.table_price_vv.addLayout(self.price_label_v)
        self.table_price_vv.addLayout(self.table_price_v)

        self.t_b = QVBoxLayout()
        self.t_b.addLayout(self.table_profits_vv)
        self.t_b.addLayout(self.table_output_vv)
        self.t_b.addLayout(self.table_price_vv)

        self.v1 = QVBoxLayout()
        self.v2 = QVBoxLayout()

        self.v1.addLayout(self.table_one_f)
        self.v1.addLayout(self.table_two_f)
        self.v1.addLayout(self.tabs)

        self.v2.addLayout(self.text_box_vv)
        self.v2.addLayout(self.inputs)
        self.v2.addLayout(self.q_f)
        self.v2.addLayout(self.t_b)

        self.main_layout = QHBoxLayout(self)

        self.main_layout.addLayout(self.v1)
        self.main_layout.addLayout(self.v2)

        self.total_in.valueChanged.connect(self.update_set)
        self.b_in.valueChanged.connect(self.update_set)
        self.c1_in.valueChanged.connect(self.update_set)
        self.c2_in.valueChanged.connect(self.update_set)
        self.add_q.clicked.connect(self.play)

    def get_states(self):
        return self.states

    def play(self):

        self.total_in.setEnabled(False)
        self.b_in.setEnabled(False)
        self.c1_in.setEnabled(False)
        self.c2_in.setEnabled(False)

        all_moves = [self.player_moves, self.co_moves]

        total = float(self.total_in.value())
        b = float(self.b_in.value())
        c1 = float(self.c1_in.value())
        c2 = float(self.c2_in.value())
        data = [total, b, c1, c2]
        states = self.get_states()
        move = self.q_input.value()
        possible_moves = get_moves(all_moves)

        self.set_round_data(states, move, possible_moves[1])

    def set_round_data(self, states, move, co_move):

        profit_matrix = states[1]
        output_matrix = states[0]
        price_matrix = states[2]

        if move == 1 and co_move == 1:

            p = price_matrix[0]

            self.firm1_best.append(2)
            self.firm2_best.append(2)

            profits_one = round(profit_matrix[0][0])
            profits_two = round(profit_matrix[0][1])

            output_one = round(output_matrix[0][0])
            output_two = round(output_matrix[0][1])

            f1_wl = "T"
            f2_wl = "T"

            f1_o = str(output_one)
            f2_o = str(output_two)

            f1_p = str(profits_one)
            f2_p = str(profits_two)

            f1_m = str(move)
            f2_m = str(co_move)

            firm_one_wl = QTableWidgetItem(f"{f1_wl}")
            firm_one_wl.setTextAlignment(Qt.AlignCenter)
            firm_two_wl = QTableWidgetItem(f"{f2_wl}")
            firm_two_wl.setTextAlignment(Qt.AlignCenter)

            firm_one_o = QTableWidgetItem(f"{f1_o}")
            firm_one_o.setTextAlignment(Qt.AlignCenter)
            firm_two_o = QTableWidgetItem(f"{f2_o}")
            firm_two_o.setTextAlignment(Qt.AlignCenter)

            firm_one_p = QTableWidgetItem(f"{f1_p}")
            firm_one_p.setTextAlignment(Qt.AlignCenter)
            firm_two_p = QTableWidgetItem(f"{f2_p}")
            firm_two_p.setTextAlignment(Qt.AlignCenter)

            firm_one_m = QTableWidgetItem(f"{f1_m}")
            firm_one_m.setTextAlignment(Qt.AlignCenter)
            firm_two_m = QTableWidgetItem(f"{f2_m}")
            firm_two_m.setTextAlignment(Qt.AlignCenter)

            self.table_one.insertRow(self.rounds)
            self.table_one.setItem(self.rounds, 0, firm_one_wl)
            self.table_one.setItem(self.rounds, 1, firm_one_m)
            self.table_one.setItem(self.rounds, 2, firm_one_p)
            self.table_one.setItem(self.rounds, 3, firm_one_o)

            self.table_two.insertRow(self.rounds)
            self.table_two.setItem(self.rounds, 0, firm_two_wl)
            self.table_two.setItem(self.rounds, 1, firm_two_m)
            self.table_two.setItem(self.rounds, 2, firm_two_p)
            self.table_two.setItem(self.rounds, 3, firm_two_o)

            self.text_box.setText(f"ROUND {self.round} : "
                                  f"TIE\n"
                                  f"Firm One Profit: {profits_one}, Firm Two Profit: {profits_two}\n"
                                  f"Firm One Output: {output_one}, Firm Two Output: {output_two}\n"
                                  f"Market Price: {p}\n")

            self.firm_one_profit += profits_one
            self.firm_two_profit += profits_two

            new_point_one = QPointF(self.rounds + 1, self.firm_one_profit)
            new_point_two = QPointF(self.rounds + 1, self.firm_two_profit)
            self.profit_points_one.append(new_point_one)
            self.profit_points_two.append(new_point_two)

            series_one = QLineSeries()
            series_one.append(self.profit_points_one)

            series_two = QLineSeries()
            series_two.append(self.profit_points_two)

            self.pro_f.chart.addSeries(series_one)
            self.pro_f.chart.addSeries(series_two)
            self.pro_f.chart.setTitle("REACTION FUNCTIONS")
            self.pro_f.chart.legend().hide()
            self.pro_f.chart.createDefaultAxes()

            self.rounds += 1
            self.round += 1

        elif move == 2 and co_move == 2:

            p = price_matrix[1]

            self.firm1_best.append(1)
            self.firm2_best.append(1)

            profits_one = round(profit_matrix[1][0])
            profits_two = round(profit_matrix[1][1])

            output_one = round(output_matrix[1][0])
            output_two = round(output_matrix[1][1])

            f1_wl = "T"
            f2_wl = "T"

            f1_o = str(output_one)
            f2_o = str(output_two)

            f1_p = str(profits_one)
            f2_p = str(profits_two)

            f1_m = str(move)
            f2_m = str(co_move)

            firm_one_wl = QTableWidgetItem(f"{f1_wl}")
            firm_one_wl.setTextAlignment(Qt.AlignCenter)
            firm_two_wl = QTableWidgetItem(f"{f2_wl}")
            firm_two_wl.setTextAlignment(Qt.AlignCenter)

            firm_one_o = QTableWidgetItem(f"{f1_o}")
            firm_one_o.setTextAlignment(Qt.AlignCenter)
            firm_two_o = QTableWidgetItem(f"{f2_o}")
            firm_two_o.setTextAlignment(Qt.AlignCenter)

            firm_one_p = QTableWidgetItem(f"{f1_p}")
            firm_one_p.setTextAlignment(Qt.AlignCenter)
            firm_two_p = QTableWidgetItem(f"{f2_p}")
            firm_two_p.setTextAlignment(Qt.AlignCenter)

            firm_one_m = QTableWidgetItem(f"{f1_m}")
            firm_one_m.setTextAlignment(Qt.AlignCenter)
            firm_two_m = QTableWidgetItem(f"{f2_m}")
            firm_two_m.setTextAlignment(Qt.AlignCenter)

            self.table_one.insertRow(self.rounds)
            self.table_one.setItem(self.rounds, 0, firm_one_wl)
            self.table_one.setItem(self.rounds, 1, firm_one_m)
            self.table_one.setItem(self.rounds, 2, firm_one_p)
            self.table_one.setItem(self.rounds, 3, firm_one_o)

            self.table_two.insertRow(self.rounds)
            self.table_two.setItem(self.rounds, 0, firm_two_wl)
            self.table_two.setItem(self.rounds, 1, firm_two_m)
            self.table_two.setItem(self.rounds, 2, firm_two_p)
            self.table_two.setItem(self.rounds, 3, firm_two_o)

            self.text_box.setText(f"ROUND {self.round} : "
                                  f"TIE\n"
                                  f"Firm One Profit: {profits_one}, Firm Two Profit: {profits_two}\n"
                                  f"Firm One Output: {output_one}, Firm Two Output: {output_two}\n"
                                  f"Market Price: {p}\n")

            self.firm_one_profit += profits_one
            self.firm_two_profit += profits_two

            new_point_one = QPointF(self.rounds + 1, self.firm_one_profit)
            new_point_two = QPointF(self.rounds + 1, self.firm_two_profit)
            self.profit_points_one.append(new_point_one)
            self.profit_points_two.append(new_point_two)

            series_one = QLineSeries()
            series_one.append(self.profit_points_one)

            series_two = QLineSeries()
            series_two.append(self.profit_points_two)

            self.pro_f.chart.addSeries(series_one)
            self.pro_f.chart.addSeries(series_two)
            self.pro_f.chart.setTitle("PROFIT FUNCTIONS")
            self.pro_f.chart.legend().hide()
            self.pro_f.chart.createDefaultAxes()

            self.rounds += 1
            self.round += 1

        elif move == 1 and co_move == 2:

            p = price_matrix[2]

            self.firm1_best.append(1)
            self.firm2_best.append(1)

            profits_one = round(profit_matrix[2][0])
            profits_two = round(profit_matrix[2][1])

            output_one = round(output_matrix[2][0])
            output_two = round(output_matrix[2][1])

            f1_wl = "W"
            f2_wl = "L"

            f1_o = str(output_one)
            f2_o = str(output_two)

            f1_p = str(profits_one)
            f2_p = str(profits_two)

            f1_m = str(move)
            f2_m = str(co_move)

            firm_one_wl = QTableWidgetItem(f"{f1_wl}")
            firm_one_wl.setTextAlignment(Qt.AlignCenter)
            firm_two_wl = QTableWidgetItem(f"{f2_wl}")
            firm_two_wl.setTextAlignment(Qt.AlignCenter)

            firm_one_o = QTableWidgetItem(f"{f1_o}")
            firm_one_o.setTextAlignment(Qt.AlignCenter)
            firm_two_o = QTableWidgetItem(f"{f2_o}")
            firm_two_o.setTextAlignment(Qt.AlignCenter)

            firm_one_p = QTableWidgetItem(f"{f1_p}")
            firm_one_p.setTextAlignment(Qt.AlignCenter)
            firm_two_p = QTableWidgetItem(f"{f2_p}")
            firm_two_p.setTextAlignment(Qt.AlignCenter)

            firm_one_m = QTableWidgetItem(f"{f1_m}")
            firm_one_m.setTextAlignment(Qt.AlignCenter)
            firm_two_m = QTableWidgetItem(f"{f2_m}")
            firm_two_m.setTextAlignment(Qt.AlignCenter)

            self.table_one.insertRow(self.rounds)
            self.table_one.setItem(self.rounds, 0, firm_one_wl)
            self.table_one.setItem(self.rounds, 1, firm_one_m)
            self.table_one.setItem(self.rounds, 2, firm_one_p)
            self.table_one.setItem(self.rounds, 3, firm_one_o)

            self.table_two.insertRow(self.rounds)
            self.table_two.setItem(self.rounds, 0, firm_two_wl)
            self.table_two.setItem(self.rounds, 1, firm_two_m)
            self.table_two.setItem(self.rounds, 2, firm_two_p)
            self.table_two.setItem(self.rounds, 3, firm_two_o)

            self.text_box.setText(f"ROUND {self.round} : "
                                  f"FIRM 1 WON\n"
                                  f"Firm One Profit: {profits_one}, Firm Two Profit: {profits_two}\n"
                                  f"Firm One Output: {output_one}, Firm Two Output: {output_two}\n"
                                  f"Market Price: {p}\n")

            self.firm_one_profit += profits_one
            self.firm_two_profit += profits_two

            new_point_one = QPointF(self.rounds + 1, self.firm_one_profit)
            new_point_two = QPointF(self.rounds + 1, self.firm_two_profit)
            self.profit_points_one.append(new_point_one)
            self.profit_points_two.append(new_point_two)

            series_one = QLineSeries()
            series_one.append(self.profit_points_one)

            series_two = QLineSeries()
            series_two.append(self.profit_points_two)

            self.pro_f.chart.addSeries(series_one)
            self.pro_f.chart.addSeries(series_two)
            self.pro_f.chart.setTitle("PROFIT FUNCTIONS")
            self.pro_f.chart.legend().hide()
            self.pro_f.chart.createDefaultAxes()

            self.rounds += 1
            self.round += 1

        elif move == 2 and co_move == 1:

            p = price_matrix[3]

            self.firm1_best.append(1)
            self.firm2_best.append(1)
            profits_one = round(profit_matrix[3][0])
            profits_two = round(profit_matrix[3][1])

            output_one = round(output_matrix[3][0])
            output_two = round(output_matrix[3][1])

            f1_wl = "L"
            f2_wl = "W"

            f1_o = str(output_one)
            f2_o = str(output_two)

            f1_p = str(profits_one)
            f2_p = str(profits_two)

            f1_m = str(move)
            f2_m = str(co_move)

            firm_one_wl = QTableWidgetItem(f"{f1_wl}")
            firm_one_wl.setTextAlignment(Qt.AlignCenter)
            firm_two_wl = QTableWidgetItem(f"{f2_wl}")
            firm_two_wl.setTextAlignment(Qt.AlignCenter)

            firm_one_o = QTableWidgetItem(f"{f1_o}")
            firm_one_o.setTextAlignment(Qt.AlignCenter)
            firm_two_o = QTableWidgetItem(f"{f2_o}")
            firm_two_o.setTextAlignment(Qt.AlignCenter)

            firm_one_p = QTableWidgetItem(f"{f1_p}")
            firm_one_p.setTextAlignment(Qt.AlignCenter)
            firm_two_p = QTableWidgetItem(f"{f2_p}")
            firm_two_p.setTextAlignment(Qt.AlignCenter)

            firm_one_m = QTableWidgetItem(f"{f1_m}")
            firm_one_m.setTextAlignment(Qt.AlignCenter)
            firm_two_m = QTableWidgetItem(f"{f2_m}")
            firm_two_m.setTextAlignment(Qt.AlignCenter)

            self.table_one.insertRow(self.rounds)
            self.table_one.setItem(self.rounds, 0, firm_one_wl)
            self.table_one.setItem(self.rounds, 1, firm_one_m)
            self.table_one.setItem(self.rounds, 2, firm_one_p)
            self.table_one.setItem(self.rounds, 3, firm_one_o)

            self.table_two.insertRow(self.rounds)
            self.table_two.setItem(self.rounds, 0, firm_two_wl)
            self.table_two.setItem(self.rounds, 1, firm_two_m)
            self.table_two.setItem(self.rounds, 2, firm_two_p)
            self.table_two.setItem(self.rounds, 3, firm_two_o)

            self.text_box.setText(f"ROUND {self.round} : "
                                  f"FIRM 2 WON THE ROUND\n"
                                  f"Firm One Profit: {profits_one}, Firm Two Profit: {profits_two}\n"
                                  f"Firm One Output: {output_one}, Firm Two Output: {output_two}\n"
                                  f"Market Price: {p}\n")

            self.firm_one_profit += profits_one
            self.firm_two_profit += profits_two

            new_point_one = QPointF(self.rounds + 1, self.firm_one_profit)
            new_point_two = QPointF(self.rounds + 1, self.firm_two_profit)
            self.profit_points_one.append(new_point_one)
            self.profit_points_two.append(new_point_two)

            series_one = QLineSeries()
            series_one.append(self.profit_points_one)

            series_two = QLineSeries()
            series_two.append(self.profit_points_two)

            self.pro_f.chart.addSeries(series_one)
            self.pro_f.chart.addSeries(series_two)
            self.pro_f.chart.setTitle("PROFIT FUNCTIONS")
            self.pro_f.chart.legend().hide()
            self.pro_f.chart.createDefaultAxes()

            self.rounds += 1
            self.round += 1

    def set_state(self, state):
        self.states = state

    def update_set(self):
        self.table_profits.setRowCount(0)
        self.table_output.setRowCount(0)
        self.table_price.setRowCount(0)
        self.rec_f.chart.removeAllSeries()
        total = float(self.total_in.value())
        b = float(self.b_in.value())
        c1 = float(self.c1_in.value())
        c2 = float(self.c2_in.value())
        data = [total, b, c1, c2]
        states = load_states(data)
        self.set_state(states)
        self.load_s(states)
        self.load_c(data)

    def load_c(self, data):

        eka = float(data[0])
        toka = float(data[1])

        uno = (eka * 2)

        series_one = QLineSeries()
        series_one.append(0, eka)
        series_one.append(uno, 0)

        series_two = QLineSeries()
        series_two.append(0, uno)
        series_two.append(eka, 0)

        self.rec_f.chart.addSeries(series_one)
        self.rec_f.chart.addSeries(series_two)
        self.rec_f.chart.setTitle("REACTION FUNCTIONS")
        self.rec_f.chart.legend().hide()
        self.rec_f.chart.createDefaultAxes()

    def load_s(self, op):

        output = op[0]
        profit = op[1]
        price = op[2]

        o1 = output[0]
        o2 = output[2]
        o3 = output[3]
        o4 = output[1]

        o1_1 = str(round(o1[0]))
        o1_2 = str(round(o1[1]))

        o2_1 = str(round(o2[0]))
        o2_2 = str(round(o2[1]))

        o3_1 = str(round(o3[0]))
        o3_2 = str(round(o3[1]))

        o4_1 = str(round(o4[0]))
        o4_2 = str(round(o4[1]))

        out_1 = QTableWidgetItem(f"{o1_1} / {o1_2}")
        out_1.setTextAlignment(Qt.AlignCenter)
        out_2 = QTableWidgetItem(f"{o2_1} / {o2_2}")
        out_2.setTextAlignment(Qt.AlignCenter)
        out_3 = QTableWidgetItem(f"{o3_1} / {o3_2}")
        out_3.setTextAlignment(Qt.AlignCenter)
        out_4 = QTableWidgetItem(f"{o4_1} / {o4_2}")
        out_4.setTextAlignment(Qt.AlignCenter)

        p1 = profit[0]
        p2 = profit[2]
        p3 = profit[3]
        p4 = profit[1]

        p1_1 = str(round(p1[0]))
        p1_2 = str(round(p1[1]))

        p2_1 = str(round(p2[0]))
        p2_2 = str(round(p2[1]))

        p3_1 = str(round(p3[0]))
        p3_2 = str(round(p3[1]))

        p4_1 = str(round(p4[0]))
        p4_2 = str(round(p4[1]))

        pro_1 = QTableWidgetItem(f"{p1_1} / {p1_2}")
        pro_1.setTextAlignment(Qt.AlignCenter)
        pro_2 = QTableWidgetItem(f"{p2_1} / {p2_2}")
        pro_2.setTextAlignment(Qt.AlignCenter)
        pro_3 = QTableWidgetItem(f"{p3_1} / {p3_2}")
        pro_3.setTextAlignment(Qt.AlignCenter)
        pro_4 = QTableWidgetItem(f"{p4_1} / {p4_2}")
        pro_4.setTextAlignment(Qt.AlignCenter)

        price_1 = QTableWidgetItem(str(round(price[0])))
        price_1.setTextAlignment(Qt.AlignCenter)
        price_2 = QTableWidgetItem(str(round(price[2])))
        price_2.setTextAlignment(Qt.AlignCenter)
        price_3 = QTableWidgetItem(str(round(price[3])))
        price_3.setTextAlignment(Qt.AlignCenter)
        price_4 = QTableWidgetItem(str(round(price[1])))
        price_4.setTextAlignment(Qt.AlignCenter)

        self.table_output.insertRow(0)
        self.table_output.setItem(0, 0, out_1)
        self.table_output.setItem(0,1, out_2)
        self.table_output.insertRow(1)
        self.table_output.setItem(1, 0, out_3)
        self.table_output.setItem(1, 1, out_4)

        self.table_profits.insertRow(0)
        self.table_profits.setItem(0, 0, pro_1)
        self.table_profits.setItem(0, 1, pro_2)
        self.table_profits.insertRow(1)
        self.table_profits.setItem(1, 0, pro_3)
        self.table_profits.setItem(1, 1, pro_4)

        self.table_price.insertRow(0)
        self.table_price.setItem(0, 0, price_1)
        self.table_price.setItem(0, 1, price_2)
        self.table_price.insertRow(1)
        self.table_price.setItem(1, 0, price_3)
        self.table_price.setItem(1, 1, price_4)


class MainWindow(QMainWindow):

    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("Duopoly")

        self.setCentralWidget(widget)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    widget = Widget()
    window = MainWindow(widget)
    window.resize(1900, 1200)
    window.show()

    sys.exit(app.exec())