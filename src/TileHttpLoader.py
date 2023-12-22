from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QByteArray, QUrl, QStandardPaths
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkDiskCache, QNetworkRequest, QNetworkReply

from config import Config


class TileHTTPLoader(QObject):
    tileLoaded = pyqtSignal(int, int, int, QByteArray)

    def __init__(self, parent=None):
        super(TileHTTPLoader, self).__init__(parent)

        self._cacheDir = QStandardPaths.writableLocation(QStandardPaths.CacheLocation)
        self._userAgent = Config.userAgent.encode()
        self._cacheSize = Config.cacheSize
        self._tileInDownload = dict()
        self._manager = None
        self._cache = None

    @pyqtSlot(int, int, int, str)
    def loadTile(self, x, y, zoom, url):
        if self._manager is None:
            self._manager = QNetworkAccessManager(parent=self)
            self._manager.finished.connect(self.handleNetworkData)
            cache = QNetworkDiskCache()
            cache.setCacheDirectory(self._cacheDir)
            cache.setMaximumCacheSize(self._cacheSize)
            self._manager.setCache(cache)

        key = (x, y, zoom)
        url = QUrl(url)

        if key not in self._tileInDownload:
            # Request the image to the map service
            request = QNetworkRequest(url)
            request.setRawHeader(b'User-Agent', self._userAgent)
            request.setAttribute(QNetworkRequest.User, key)
            request.setAttribute(QNetworkRequest.CacheLoadControlAttribute, QNetworkRequest.PreferCache)

            self._tileInDownload[key] = self._manager.get(request)

    @pyqtSlot(QNetworkReply)
    def handleNetworkData(self, reply):
        tp = reply.request().attribute(QNetworkRequest.User)
        if tp in self._tileInDownload:
            del self._tileInDownload[tp]

        if not reply.error():
            data = reply.readAll()
            self.tileLoaded.emit(*tp, data)

        reply.close()
        reply.deleteLater()

    @pyqtSlot()
    def abortRequest(self, x: int, y: int, zoom: int):
        p = (x, y, zoom)

        if p in self._tileInDownload:
            reply = self._tileInDownload[p]
            del self._tileInDownload[p]
            reply.close()
            reply.deleteLater()

    @pyqtSlot()
    def abortAllRequests(self):
        for x, y, zoom in list(self._tileInDownload.keys()):
            self.abortRequest(x, y, zoom)
