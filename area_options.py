from PyQt5 import QtWidgets


class AreaOptions(QtWidgets.QFrame):
    def __init__(self, main):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.layout)

        self.header = QtWidgets.QLabel("Area options")
        self.layout.addWidget(self.header)

        self.type_label = QtWidgets.QLabel("Area type")
        self.layout.addWidget(self.type_label)

        self.type = QtWidgets.QComboBox()
        self.type.addItem("North")
        self.type.addItem("Northeast")
        self.type.addItem("East")
        self.type.addItem("Southeast")
        self.type.addItem("South")
        self.type.addItem("Southwest")
        self.type.addItem("West")
        self.type.addItem("Northwest")
        self.type.addItem("Center")
        self.type.addItem("Land")
        self.type.addItem("Water")
        self.layout.addWidget(self.type)

        self.sea_margin_label = QtWidgets.QLabel("Sea margin")
        self.layout.addWidget(self.sea_margin_label)

        self.sea_margin = QtWidgets.QDoubleSpinBox()
        self.sea_margin.setMinimum(0.0)
        self.sea_margin.setMaximum(0.4)
        self.sea_margin.setSingleStep(0.05)
        self.sea_margin.setValue(0.20)
        self.layout.addWidget(self.sea_margin)

        self.coastal_label = QtWidgets.QLabel("Coastal water rate")
        self.layout.addWidget(self.coastal_label)

        self.coastal_rate = QtWidgets.QDoubleSpinBox()
        self.coastal_rate.setMinimum(0.05)
        self.coastal_rate.setMaximum(0.95)
        self.coastal_rate.setSingleStep(0.05)
        self.coastal_rate.setValue(0.50)
        self.layout.addWidget(self.coastal_rate)

        self.add_button = QtWidgets.QPushButton("Add type")
        self.add_button.clicked.connect(main.add_area_type)
        self.layout.addWidget(self.add_button)

        self.set_button = QtWidgets.QPushButton("Set type")
        self.set_button.clicked.connect(main.set_area_type)
        self.layout.addWidget(self.set_button)

        self.coastal_button = QtWidgets.QPushButton("Add coastal landscape")
        self.coastal_button.clicked.connect(main.add_coastal_landscape)
        self.layout.addWidget(self.coastal_button)

        self.mountain_label = QtWidgets.QLabel("Mountain ranges")
        self.layout.addWidget(self.mountain_label)

        self.min_offset_label = QtWidgets.QLabel(
            "Minimum distance\nfrom border")
        self.layout.addWidget(self.min_offset_label)

        self.min_offset = QtWidgets.QSpinBox()
        self.min_offset.setMinimum(1)
        self.min_offset.setMaximum(30)
        self.min_offset.setSingleStep(1)
        self.min_offset.setValue(3)
        self.layout.addWidget(self.min_offset)

        self.max_offset_label = QtWidgets.QLabel(
            "Maximum distance\nfrom border")
        self.layout.addWidget(self.max_offset_label)

        self.max_offset = QtWidgets.QSpinBox()
        self.max_offset.setMinimum(1)
        self.max_offset.setMaximum(30)
        self.max_offset.setSingleStep(1)
        self.max_offset.setValue(5)
        self.layout.addWidget(self.max_offset)

        self.land_mountain = QtWidgets.QPushButton("Generate by land")
        self.land_mountain.clicked.connect(main.create_mountains_on_land)
        self.layout.addWidget(self.land_mountain)

        self.sea_mountain = QtWidgets.QPushButton("Generate by sea")
        self.sea_mountain.clicked.connect(main.create_mountains_by_sea)
        self.layout.addWidget(self.sea_mountain)

        self.erase_mountain = QtWidgets.QPushButton("Erase mountains")
        self.erase_mountain.clicked.connect(main.erase_mountains)
        self.layout.addWidget(self.erase_mountain)

        self.layout.addStretch()

    def enable_buttons(self, flag: bool) -> None:
        self.set_button.setEnabled(flag)
        self.add_button.setEnabled(flag)
        self.coastal_button.setEnabled(flag)
        self.land_mountain.setEnabled(flag)
        self.sea_mountain.setEnabled(flag)
        self.erase_mountain.setEnabled(flag)
