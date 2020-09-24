""" 
This submodule contains a wrapper classes for **Revit** room elements.
"""
import Autodesk
from revitron.element import Element


class Room(Element):
    """
    A wrapper class for room elements.
    """
    
    def getBboxCenter(self, inRoomOnly = False):
        """
        Get the center point of a room's bounding box.

        Args:
            inRoomOnly (boolean): Optionally only return a point in case the bounding box center is actually in the room

        Returns:
            object: A Revit point object
        """
        import revitron
        
        room = self.element
        bbox = self.getBbox()
        
        if isinstance(bbox, revitron.BoundingBox):
            x = (bbox.Min.X + bbox.Max.X) / 2
            y = (bbox.Min.Y + bbox.Max.Y) / 2
            z = (bbox.Min.Z + bbox.Max.Z) / 2
            point = revitron.DB.XYZ(x, y, z)
            if room.IsPointInRoom(point) or not inRoomOnly:
                return point
        

    def tagCenter(self, tagTypeId = False, viewId = False):
        """
        Create a room tag in the bounding box center.

        Args:
            tagTypeId (ElementId, optional): A Revit element Id of a custom tag type. Defaults to False.
            viewId (ElementId, optional): A Revit element Id a view. Defaults to False.

        Returns:
            object: A Revit ``RoomTag`` element 
        """
        import revitron
        if not viewId:
            viewId = revitron.ACTIVEVIEW.Id
        return revitron.Create.roomTag(self.element, self.getBboxCenter(), tagTypeId, viewId)
    
    
        