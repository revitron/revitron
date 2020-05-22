import revitron
from pyrevit import script


class Transaction:
    
    def __init__(self):
        bundle = script.get_bundle_name().replace('.pushbutton', '')
        self.transaction = revitron.DB.Transaction(revitron.DOC, bundle)
        self.transaction.Start()
        
    def commit(self):
        self.transaction.Commit()
    