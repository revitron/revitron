""" 
This submodule contains a wrapper class for **Revit** room elements.
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
    
      
    def getBoundary(self):
        """
        Get the boundary of a given room. 
        
        Returns:
            list: A list of boundary segment curves
        """
        import revitron
        room = self.element
        options = revitron.DB.SpatialElementBoundaryOptions()
        boundaryLocation = revitron.DB.AreaVolumeSettings.\
                           GetAreaVolumeSettings(revitron.DOC).\
                           GetSpatialElementBoundaryLocation(revitron.DB.SpatialElementType.Room)   
        options.SpatialElementBoundaryLocation = boundaryLocation
        curveList = []
        for boundaryList in room.GetBoundarySegments(options):
            for boundary in boundaryList:
                curveList.append(boundary.GetCurve())
        return curveList


    def getBoundaryPoints(self):
        """
        Get all points along a room boundary.

        Returns:
            list: A list of points
        """
        import revitron
        room = self.element
        curveList = self.getBoundary()
        points = []
        for curve in curveList:
            # If the curve is an arc, first tessellate the curve 
            # and extend the points array with the polyline points.
            if 'Arc' in str(curve.GetType()):
                points.extend(curve.Tessellate())
            else:
                points.append(curve.GetEndPoint(0))
        return points


    def getBoundaryInsetPoints(self, inset = 0.1):
        """
        Get all points along an inset of the room boundary. 
        
        The inset is useful in cases where a point has to be used as a location for a tag 
        and therefore should be located direktly on the boundary but a little bit more inside instead 
        to avoid issues and warnings.

        Args:
            inset (float, optional): The inset. Defaults to 0.1.

        Returns:
            list: The list of points
        """
        import revitron
        room = self.element
        options = revitron.DB.SpatialElementBoundaryOptions()
        boundaryLocation = revitron.DB.AreaVolumeSettings.\
                           GetAreaVolumeSettings(revitron.DOC).\
                           GetSpatialElementBoundaryLocation(revitron.DB.SpatialElementType.Room)
        options.SpatialElementBoundaryLocation = boundaryLocation
        curves = dict()
        points = []

        try:            
            for boundaryList in room.GetBoundarySegments(options):
                cl = revitron.DB.CurveLoop()
                for x in boundaryList:
                    cl.Append(x.GetCurve())
                curves[cl.GetExactLength()] = cl

            curveLengths = curves.keys()
            longest = curves[max(curveLengths)]

            tempInset = revitron.DB.CurveLoop.CreateViaOffset(longest, inset, revitron.DB.XYZ(0,0,1))
            if tempInset.GetExactLength() > max(curveLengths):
                tempInset = revitron.DB.CurveLoop.CreateViaOffset(longest, inset, revitron.DB.XYZ(0,0,-1))

            for c in tempInset:
                points.append(c.GetEndPoint(0))

        except:
            # If CurveLoop throws exception, get points from boundary.
            points = self.getPoints()
            pass

        return points
     

    def getPointClosest(self, point, inset = 0.1):
        """
        Get the point on a room boundary that is the closest to a given point.

        Args:
            point (object): A Revit XYZ object
            inset (float, optional): An optional room boundary inset. Defaults to 0.1.

        Returns:
            object: A Revit XYZ object
        """
        closestDistance = False
        for p in self.getBoundaryInsetPoints(inset):
            d = p.DistanceTo(point)
            if not closestDistance:
                closestDistance = d
                closestPoint = p
            else:
                if d < closestDistance:
                    closestDistance = d
                    closestPoint = p
        return closestPoint
        
    
    def getPointTopLeft(self, inset = 0.1):
        """
        Get the most top left point of a room boundary.

        Args:
            inset (float, optional): An optional room boundary inset. Defaults to 0.1.

        Returns:
            object: A Revit XYZ object
        """
        import revitron
        bbox = self.getBbox()
        bboxTopLeft = revitron.DB.XYZ(bbox.Min.X, bbox.Max.Y, bbox.Min.Z)
        return self.getPointClosest(bboxTopLeft, inset)   
     
     
    def getPointTopRight(self, inset = 0.1):
        """
        Get the most top right point of a room boundary.

        Args:
            inset (float, optional): An optional room boundary inset. Defaults to 0.1.

        Returns:
            object: A Revit XYZ object
        """
        import revitron
        bbox = self.getBbox()
        bboxTopLeft = revitron.DB.XYZ(bbox.Max.X, bbox.Max.Y, bbox.Min.Z)
        return self.getPointClosest(bboxTopLeft, inset)   
    
    
    def getPointBottomLeft(self, inset = 0.1):
        """
        Get the most bottom left point of a room boundary.

        Args:
            inset (float, optional): An optional room boundary inset. Defaults to 0.1.

        Returns:
            object: A Revit XYZ object
        """
        import revitron
        bbox = self.getBbox()
        bboxTopLeft = revitron.DB.XYZ(bbox.Min.X, bbox.Min.Y, bbox.Min.Z)
        return self.getPointClosest(bboxTopLeft, inset)   
    
    
    def getPointBottomRight(self, inset = 0.1):
        """
        Get the most bottom right point of a room boundary.

        Args:
            inset (float, optional): An optional room boundary inset. Defaults to 0.1.

        Returns:
            object: A Revit XYZ object
        """
        import revitron
        bbox = self.getBbox()
        bboxTopLeft = revitron.DB.XYZ(bbox.Max.X, bbox.Min.Y, bbox.Min.Z)
        return self.getPointClosest(bboxTopLeft, inset)   
    

    def tagCenter(self, tagTypeId = False, viewId = False):
        """
        Create a room tag in the bounding box center. 
        All existing room tags will be removed before automatically.

        Args:
            tagTypeId (ElementId, optional): A Revit element Id of a custom tag type. Defaults to False.
            viewId (ElementId, optional): A Revit element Id a view. Defaults to False.

        Returns:
            object: A Revit ``RoomTag`` element 
        """
        import revitron
        from revitron import _
        
        if not viewId:
            viewId = revitron.ACTIVEVIEW.Id
            
        for tag in self.getTags():
            _(tag).delete()
            
        return revitron.Create.roomTag(self.element, self.getBboxCenter(), tagTypeId, viewId)
