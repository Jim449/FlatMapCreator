from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QTimer
from map_locations import MapLocations
from map_label import MapLabel
from world import World
from new_map_menu import NewMapMenu
import constants as c


class Main(QtWidgets.QMainWindow):
    # 1-RED, 5-BLUE, 10-GREEN, 13-YELLOW, 3-PURPLE, 6-LIGHTBLUE, 9-SEAGREEN
    # 15-ORANGE, 17-BROWN, 18-BLUEGRAY, 2-MAGENTA, 8-TEAL, 11-GRASS
    # 14-LIGHTORANGE, 16-LIGHTRED, 12-OLIVE
    AREA_COLORS = [QColor(244, 67, 54), QColor(229, 115, 115),
                   QColor(63, 81, 181), QColor(121, 134, 203),
                   QColor(76, 175, 80), QColor(129, 199, 132),
                   QColor(255, 235, 59), QColor(255, 241, 118),
                   QColor(156, 39, 176), QColor(186, 104, 200),
                   QColor(33, 150, 243), QColor(100, 181, 246),
                   QColor(205, 220, 57), QColor(220, 231, 117),
                   QColor(121, 85, 72), QColor(161, 136, 127),
                   QColor(96, 125, 139), QColor(144, 164, 174),
                   QColor(233, 30, 99), QColor(240, 98, 146),
                   QColor(0, 188, 212), QColor(77, 208, 225),
                   QColor(139, 195, 74), QColor(174, 213, 129),
                   QColor(255, 193, 7), QColor(255, 213, 79),
                   QColor(255, 87, 34), QColor(255, 138, 101),
                   QColor(255, 152, 0), QColor(255, 183, 77)]

    MAP_LENGTH = 800
    MAP_HEIGHT = 800
    CELL_SIZE = 2
    GRID_SIZE = 20
    LENGTH_DIVISION = 40
    HEIGHT_DIVISION = 40

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map creator")

        self.world: World = World(Main.LENGTH_DIVISION)
        self.new_map_menu: NewMapMenu = None
        self.timer: self.timer = QTimer()

        self.new_action = QtWidgets.QAction("New map", self)
        self.export_action = QtWidgets.QAction("Export", self)
        self.quit_action = QtWidgets.QAction("Quit", self)
        self.grid_view_action = QtWidgets.QAction("View grid", self)
        self.line_view_action = QtWidgets.QAction("View lines", self)
        self.label_view_action = QtWidgets.QAction("View locations", self)
        self._create_actions()

        self.file_menu = QtWidgets.QMenu("File", self)
        self.view_menu = QtWidgets.QMenu("View", self)
        self._create_menu_bar()

        self.left_tool_bar = QtWidgets.QToolBar("Tools", self)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.left_tool_bar)

        self.layout = QtWidgets.QHBoxLayout()
        self.left_layout = QtWidgets.QVBoxLayout()
        self.center_layout = QtWidgets.QVBoxLayout()
        self.right_layout = QtWidgets.QVBoxLayout()

        self.map_screen = QtWidgets.QLabel()
        self.map_screen.installEventFilter(self)

        self.map = QtGui.QPixmap(Main.MAP_LENGTH, Main.MAP_HEIGHT)
        self.grid_map = QtGui.QPixmap(Main.MAP_LENGTH, Main.MAP_HEIGHT)
        self.label_map = QtGui.QPixmap(Main.MAP_LENGTH, Main.MAP_HEIGHT)

        self.map.fill(c.get_color(c.WATER))
        self.grid_map.fill(c.EMPTY_COLOR)
        self.label_map.fill(c.EMPTY_COLOR)

        self.map_screen.setPixmap(self.map)
        self.center_layout.addWidget(self.map_screen)

        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.center_layout)
        self.layout.addLayout(self.right_layout)

        self.locations = MapLocations()
        self.locations.add_location(MapLabel(50, 50, "Sometown", 3, "Town"))
        self.locations.add_location(
            MapLabel(100, 150, "Somecapital", 3, "Capital"))
        self.locations.add_location(
            MapLabel(150, 250, "Somethingelse", 3, "Geography"))
        self.locations.add_location(MapLabel(200, 350, "Smalltown", 2, "Town"))
        self.locations.add_location(
            MapLabel(400, 350, "Smallcapital", 2, "Capital"))
        self.locations.add_location(
            MapLabel(250, 450, "Smallplace", 2, "Geography"))
        self.locations.add_location(MapLabel(300, 550, "Minortown", 1, "Town"))
        self.locations.add_location(
            MapLabel(500, 550, "Minorcapital", 1, "Capital"))
        self.locations.add_location(
            MapLabel(350, 650, "Minorplace", 1, "Geography"))

        self.paint_labels(self.locations, importance=3)
        self.paint_grid()
        self.paint()

        widget = QtWidgets.QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        menu_bar.addMenu(self.file_menu)
        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.export_action)
        self.file_menu.addAction(self.quit_action)
        menu_bar.addMenu(self.view_menu)
        self.view_menu.addAction(self.grid_view_action)
        self.view_menu.addAction(self.line_view_action)
        self.view_menu.addAction(self.label_view_action)

    def _create_actions(self):
        self.new_action.triggered.connect(self.new_map)
        self.export_action.triggered.connect(self.export)
        self.quit_action.triggered.connect(self.close)

        self.grid_view_action.setCheckable(True)
        self.grid_view_action.setChecked(True)
        self.grid_view_action.triggered.connect(self.repaint_grid)

        self.line_view_action.setCheckable(True)
        self.line_view_action.setChecked(True)
        self.line_view_action.triggered.connect(self.repaint_grid)

        self.label_view_action.setCheckable(True)
        self.label_view_action.setChecked(True)
        self.label_view_action.triggered.connect(self.paint)

    def paint_expansion(self) -> None:
        """Paints areas. Unclaimed cells are painted black"""
        painter = QtGui.QPainter(self.map_screen.pixmap())
        pen = QtGui.QPen()
        painter.fillRect(0, 0, Main.MAP_LENGTH, Main.MAP_HEIGHT, Qt.black)
        pen.setWidth(2)

        for area in self.world.areas:
            pen.setColor(Main.AREA_COLORS[area.id * 2])
            painter.setPen(pen)

            for cell in area.claimed_cells:
                painter.drawPoint(cell.x * 2, cell.y * 2)

            pen.setColor(Main.AREA_COLORS[area.id * 2 + 1])
            painter.setPen(pen)

            for cell in area.queued_cells:
                painter.drawPoint(cell.x * 2, cell.y * 2)
        painter.end()
        self.update()

    def paint_grid(self, draw_grid: bool = True, draw_lines: bool = True) -> None:
        """Draws a grid"""
        painter = QtGui.QPainter(self.grid_map)
        pen = QtGui.QPen()
        pen.setColor(c.GRID_COLOR)
        painter.setPen(pen)
        painter.fillRect(0, 0, Main.MAP_LENGTH,
                         Main.MAP_HEIGHT, c.get_color(c.WATER))

        if draw_grid:
            for x in range(0, Main.MAP_LENGTH, Main.GRID_SIZE):
                painter.drawLine(x, 0, x, Main.MAP_HEIGHT)

            for y in range(0, Main.MAP_HEIGHT, Main.GRID_SIZE):
                painter.drawLine(0, y, Main.MAP_LENGTH, y)

        if draw_lines:
            pen.setColor(c.LINE_COLOR)
            painter.setPen(pen)

            for x in range(0, Main.MAP_LENGTH, Main.GRID_SIZE * 10):
                painter.drawLine(x, 0, x, Main.MAP_HEIGHT)

            for y in range(0, Main.MAP_HEIGHT, Main.GRID_SIZE * 10):
                painter.drawLine(0, y, Main.MAP_LENGTH, y)
        painter.end()

    def paint_labels(self, locations: MapLocations, importance: int) -> None:
        """Draws labels"""
        painter = QtGui.QPainter(self.label_map)

        # Remove loop. get_locations should give everything of given importance or higher
        for importance in range(1, 4):
            for location in locations.get_locations(importance):
                font = QtGui.QFont("Calibri",
                                   pointSize=location.get_font_size(),
                                   italic=location.get_italics())
                painter.setFont(font)

                if location.style == "Capital":
                    painter.fillRect(*location.get_icon_metrics(), c.BLACK)
                    painter.drawText(
                        location.x + 8, location.y + 5, location.get_text())
                elif location.style == "City" or location.style == "Town":
                    painter.drawEllipse(*location.get_icon_metrics())
                    painter.drawText(
                        location.x + 8, location.y + 5, location.get_text())
                else:
                    painter.drawText(location.x, location.y +
                                     5, location.get_text())
        painter.end()

    def join_maps(self, map_1: QtGui.QPixmap, map_2: QtGui.QPixmap) -> QtGui.QPixmap:
        result = QtGui.QPixmap(Main.MAP_LENGTH, Main.MAP_HEIGHT)
        painter = QtGui.QPainter(result)
        painter.drawPixmap(QtCore.QPoint(), map_1)
        painter.setCompositionMode(
            QtGui.QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.drawPixmap(result.rect(), map_2, map_2.rect())
        painter.end()
        return result

    def paint(self) -> None:
        result = self.map

        if self.grid_view_action.isChecked() or self.line_view_action.isChecked():
            result = self.join_maps(result, self.grid_map)

        if self.label_view_action.isChecked():
            result = self.join_maps(result, self.label_map)

        self.map_screen.setPixmap(result)
        self.update()

    def repaint_grid(self):
        if self.grid_view_action.isChecked() or self.line_view_action.isChecked():
            self.paint_grid(self.grid_view_action.isChecked(),
                            self.line_view_action.isChecked())
        self.paint()

    def export(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, caption="Save image",
                                                     filter=".png", initialFilter=".png")
        self.map_screen.pixmap().save(name[0] + name[1])

    def new_map(self):
        self.new_map_menu: NewMapMenu = NewMapMenu(self)
        self.new_map_menu.show()

    def expand_areas(self):
        """Expands area by one growth step and paints the progress.
        When finished, generates land and paints the map"""
        if self.world.expand_areas():
            self.world.create_land()
            self.paint()
        else:
            self.paint_expansion()
            self.timer.singleShot(100, self.expand_areas)

    def generate_map(self):
        self.new_map_menu.generate_button.setText("Generating...")
        self.new_map_menu.generate_button.setEnabled(False)

        if self.new_map_menu.algorithm.currentText() == "Fixed growth":
            fixed_growth = True
        else:
            fixed_growth = False

        self.world.create_areas(total_amount=self.new_map_menu.regions_total.value(),
                                land_amount=self.new_map_menu.land_regions.value(),
                                sea_amount=self.new_map_menu.sea_regions.value(),
                                sea_margin=self.new_map_menu.sea_margin.value(),
                                fixed_growth=fixed_growth)

        if self.new_map_menu.visualize_check.isChecked():
            self.timer.singleShot(100, self.expand_areas)
        else:
            # This might take a while. Add a progress bar.
            self.world.build_areas()
            self.world.create_land()
            self.new_map_menu.close()
            self.new_map_menu = None
            self.paint()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    app.exec_()
