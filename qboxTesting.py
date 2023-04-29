from PyQt6.QtWidgets import QApplication, QSpinBox
from PyQt6.QtGui import QFont

app = QApplication([])

spinBox = QSpinBox()
spinBox.setStyleSheet('''
    QSpinBox {
        border: none;
        background-color: #FFFFFF;
        color: #303030;
        font-size: 14px;
        padding: 8px;
    }

    QSpinBox::up-button, QSpinBox::down-button {
        border: none;
        background-color: #FFABAB;
        width: 16px;
        height: 16px;
        subcontrol-origin: padding;
        subcontrol-position: right;
        margin-right: 8px;
        margin-top: 8px;
    }

    QSpinBox::up-button:hover, QSpinBox::down-button:hover {
        background-color: #ED2B2A;
    }

    QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {
        background-color: #ED2B2A;
    }
''')
spinBox.setFont(QFont('Open Sans', 14))

spinBox.show()

app.exec()
