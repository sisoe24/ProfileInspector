
class __PageSelector(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        _layout = QHBoxLayout()

        widget_color(self, 'green')

        self._left = QToolButton()
        self._left.setArrowType(Qt.LeftArrow)

        self._right = QToolButton()
        self._right.setArrowType(Qt.RightArrow)

        self._widget_label = QLabel()
        self._widget_label.setAlignment(Qt.AlignHCenter)

        _layout.addWidget(self._left)
        _layout.addWidget(self._widget_label)
        _layout.addWidget(self._right)

        self.setLayout(_layout)

    @property
    def left_button(self):
        return self._left

    @property
    def right_button(self):
        return self._right

    def set_label(self, value):
        return self._widget_label.setText(value)


class __PageController(QVBoxLayout):
    def __init__(self):
        QVBoxLayout.__init__(self)

        self.table_stack = QStackedWidget()

        self.dag_page = DagInspector()
        self.table_stack.addWidget(self.dag_page)
        self.table_stack.addWidget(FileInspectorWidget())
        self.table_stack.addWidget(XmlReportWidget())

        self.table_stack.setCurrentIndex(2)

        self._stack_selector = PageSelector()
        self._stack_selector.left_button.clicked.connect(
            lambda: self.change_stack(0)
        )

        self._stack_selector.right_button.clicked.connect(
            lambda: self.change_stack(1)
        )

        self._stack_selector.set_label(
            self.table_stack.currentWidget().objectName()
        )

        self.addWidget(self._stack_selector)
        self.addWidget(self.table_stack)

    def change_stack(self, index):
        self.table_stack.setCurrentIndex(index)
        self._stack_selector.set_label(
            self.table_stack.currentWidget().objectName()
        )
