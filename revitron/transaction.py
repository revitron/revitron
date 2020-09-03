
from pyrevit import script


class Transaction:
    
    
    def __init__(self):
        """
        Inits a new transaction.
        """  
        import revitron
              
        bundle = script.get_bundle_name().replace('.pushbutton', '')
        self.transaction = revitron.DB.Transaction(revitron.DOC, bundle)
        self.transaction.Start()
        
        
    def commit(self):
        """
        Commits the open transaction.
        """        
        self.transaction.Commit()
        
    
    def rollback(self):
        """
        Rolls back the open transaction.
        """
        self.transaction.RollBack()
    