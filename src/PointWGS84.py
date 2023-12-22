from PyQt5.QtCore import QPointF


class PointWGS84(QPointF):
    def __init__(self, lat=0.0, lon=0.0):
        super(PointWGS84, self).__init__(lat, lon)
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return 'PointWGS84(lat: %f, lon: %f)' % (self.lat, self.lon)

    def lat(self):
        return self.lat

    def lon(self):
        return self.lon

    def x(self):
        return self.lon

    def y(self):
        return self.lat

    def setX(self, x):
        self.lon = x

    def setY(self, y):
        self.lat = y

    def setLat(self, lat):
        self.lat = lat

    def setLon(self, lon):
        self.lon = lon

    def copy(self):
        return self
