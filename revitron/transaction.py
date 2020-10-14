"""
The ``transaction`` submodule contains a wrapper class to simplify the usage of transactions:: 

    t = revitron.Transaction() 
    ... 
    t.close()
    
"""
from pyrevit import script


class Transaction:
    """
    A transaction helper class. 
    """
    
    def __init__(self):
        """
        Inits a new transaction.
        """  
        import revitron
        self.transaction = revitron.DB.Transaction(revitron.DOC, script.get_button().get_title())
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
    