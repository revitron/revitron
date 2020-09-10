import clr
clr.AddReference("Microsoft.Office.Interop.Excel")
import Microsoft.Office.Interop.Excel as Excel



class ExcelWorkbook:
    
    
    def __init__(self, file):
        """
        Inits a new ExcelWorkbook instance.

        Args:
            file (string): The path to the xls file
        """
        excel = Excel.ApplicationClass()
        self.workbook = excel.Workbooks.Open(file)
        
    
    def close(self, save = True):
        """
        Closes and optionally saves a workbook file.

        Args:
            save (bool, optional): If True, the file is saved before closing. Defaults to True.
        """
        if save:
            self.workbook.Save()
        self.workbook.Close(SaveChanges=save)
        
        
    def newWorksheetFromTemplate(self, template, name):
        """
        Creates a new worksheet as a copy from a given template.

        Example::
        
            workbook = revitron.ExcelWorkbook(xlsx)
            worksheet = workbook.newWorksheetFromTemplate('Template', 'Name')

        Args:
            template (string): The template name
            name (string): The name of the new copy

        Returns:
            object: An ExcelWorksheet instance
        """
        self.workbook.Worksheets(template).Copy(Before = self.workbook.Worksheets(1))
        worksheet = self.workbook.Worksheets(1)
        worksheet.Name = name
        return ExcelWorksheet(worksheet)
    
    
class ExcelWorksheet:
    
    
    def __init__(self, worksheet):
        """
        Inits a new ExcelWorksheet instance.

        Args:
            file (object): An Excel worksheet object
        """
        self.worksheet = worksheet
        
        
    def cell(self, row, column, value):
        """
        Writes data to a cell of the current worksheet. 
        
        Example::
        
            book = revitron.ExcelWorkbook(xlsx)
            sheet = book.newWorksheetFromTemplate('Template', 'Name')
            sheet.cell(5, 1, 'Value')

        Args:
            row (integer): The row
            column (integer): The column
            value (mixed): The value

        Returns:
            object: The ExcelWorkbook instance
        """
        cell = self.worksheet.Cells(row, column)
        cell.Value = value
        return self
        