from PyQt5.QtCore import QModelIndex, Qt, QSortFilterProxyModel
from PyQt5.QtGui import QFont, QColor

class FileFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        self.open_files = set()
        super().__init__(parent)


    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex):
        index0 = self.sourceModel().index(source_row, 0, source_parent)
<<<<<<<+HEAD
        return self.sourceModel().fileName(index0) != "URHProject.xml"
=======
        return self.sourceModel().fileName(index0) not in ("URHProject.xml")
>>>>>>>-b1ae517

    def data(self, index: QModelIndex, role=None):
        if role == Qt.FontRole or role == Qt.TextColorRole:
            file_name = self.sourceModel().filePath(self.mapToSource(index))
            if file_name in self.open_files:
                if role == Qt.FontRole:
                    font = QFont()
                    font.setBold(True)
                    return font
                elif role == Qt.TextColorRole:
                    return QColor("orange")

        return super().data(index, role)
