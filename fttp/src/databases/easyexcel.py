# unit six
# js 2.9.2004

# easy Excel from Python/Programming on Win32, p. 149
# js 26.11.01

from types import UnicodeType

from win32com.client import Dispatch


def fixStringAndDate(value):
    if type(value) is UnicodeType:
        return str(value)
    ##    elif type(value) is TimeType:
    ##        return int(value)
    else:
        return value


class EasyExcel:
    """A utility to make it easier to get at Excel.
       Remember to save your data is your problem, as is error handling.
       Operates on one workbook at a time."""

    def __init__(self, filename=None):
        self.xlApp = Dispatch('Excel.Application')
        if filename:
            self.filename = filename
            self.xlBook = self.xlApp.Workbooks.Open(filename)
        else:
            self.filename = ''
            self.xlBook = self.xlApp.Workbooks.Add()

    def setVisible(self, flag):
        self.xlApp.Visible = flag

    def save(self, newfilename=None):
        if newfilename:
            self.filename = newfilename
            self.xlBook.SaveAs(newfilename)
        else:
            self.xlBook.Save()

    def close(self):
        self.xlBook.Close(SaveChanges=0)
        del self.xlApp

    def getCell(self, sheetNbr, row, col):
        """ Get value of one cell; sheetNbr, row, col are ints > 0 """
        sheet = self.xlBook.Worksheets(sheetNbr)
        return fixStringAndDate(sheet.Cells(row, col).Value)

    def setCell(self, sheetNbr, row, col, value):
        """ Set value of one cell; sheetNbr, row, col are ints > 0 """
        sheet = self.xlBook.Worksheets(sheetNbr)
        sheet.Cells(row, col).Value = value

    def getRange(self, sheetNbr, row1, col1, row2, col2):
        """ Return a 2d-range of values: sheetNbr, row, col are ints > 0
            and define the 2d-range"""
        sheet = self.xlBook.Worksheets(sheetNbr)
        return sheet.Range(sheet.Cells(row1, col1), sheet.Cells(row2, col2)).Value

    def setRange(self, sheetNbr, topRow, leftCol, data):
        """ insert a 2d array starting at (topRow, leftCol).
            Works out the sheet size for itself """
        bottomRow = topRow + len(data) - 1
        rightCol = len(data[0]) + 1
        sheet = self.xlBook.Worksheets(sheetNbr)
        sheet.Range(sheet.Cells(topRow, leftCol),
                    sheet.Cells(bottomRow, rightCol)).Value = data

    def getContiguousRange(self, sheetNbr, topRow, leftCol):
        """ Tracks down and across from top left cell until it encounters
            blank cells; returns the non-blank range."""
        sheet = self.xlBook.Worksheets(sheetNbr)

        bottom = topRow
        while sheet.Cells(bottom + 1, leftCol).Value not in [None, '']:
            bottom += 1

        right = leftCol
        while sheet.Cells(topRow, right + 1).Value not in [None, '']:
            right += 1

        return sheet.Range(sheet.Cells(topRow, leftCol),
                           sheet.Cells(bottom, right)).Value
