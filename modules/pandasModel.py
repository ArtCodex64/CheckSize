from PyQt5.QtCore import QAbstractTableModel, Qt

class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
    
    def rowCount(self, data):
        return self._data.shape[0]

    def columnCount(self, data):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None
    
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            self._data.columns[col]
            return self._data.columns[col]
        return None