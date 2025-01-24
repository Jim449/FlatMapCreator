from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt


class NewMapMenu(QtWidgets.QFrame):
    def __init__(self, main):
        super().__init__()
        self.setWindowTitle("New map")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.layout)

        self.algorithm_label = QtWidgets.QLabel("Area generation algorithm")
        self.layout.addWidget(self.algorithm_label)

        self.algorithm = QtWidgets.QComboBox()
        self.algorithm.addItem("Relative growth")
        self.algorithm.addItem("Fixed growth")
        self.layout.addWidget(self.algorithm)

        self.regions_label = QtWidgets.QLabel("Total amount of areas")
        self.layout.addWidget(self.regions_label)

        self.regions_total = QtWidgets.QSpinBox()
        self.regions_total.setMinimum(2)
        self.regions_total.setMaximum(15)
        self.regions_total.setValue(10)
        self.layout.addWidget(self.regions_total)

        self.land_label = QtWidgets.QLabel("Amount of land-only areas")
        self.layout.addWidget(self.land_label)

        self.land_regions = QtWidgets.QSpinBox()
        self.land_regions.setMinimum(0)
        self.land_regions.setMaximum(15)
        self.land_regions.setValue(0)
        self.layout.addWidget(self.land_regions)

        self.sea_label = QtWidgets.QLabel("Amount of sea-only areas")
        self.layout.addWidget(self.sea_label)

        self.sea_regions = QtWidgets.QSpinBox()
        self.sea_regions.setMinimum(0)
        self.sea_regions.setMaximum(14)
        self.sea_regions.setValue(0)
        self.layout.addWidget(self.sea_regions)

        self.margin_label = QtWidgets.QLabel("Sea margin of mixed areas")
        self.layout.addWidget(self.margin_label)

        self.sea_margin = QtWidgets.QDoubleSpinBox()
        self.sea_margin.setMinimum(0.0)
        self.sea_margin.setMaximum(0.4)
        self.sea_margin.setSingleStep(0.05)
        self.sea_margin.setValue(0.15)
        self.layout.addWidget(self.sea_margin)

        self.visualize_check = QtWidgets.QCheckBox("Visualize area expansion")
        self.visualize_check.setChecked(False)
        self.layout.addWidget(self.visualize_check)

        self.generate_button = QtWidgets.QPushButton("Generate map")
        self.generate_button.clicked.connect(main.generate_map)
        self.layout.addWidget(self.generate_button)

        self.abort_button = QtWidgets.QPushButton("Cancel")
        self.abort_button.clicked.connect(self.close)
        self.layout.addWidget(self.abort_button)
