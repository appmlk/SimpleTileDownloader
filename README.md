# SimpleTileDownloader
简易瓦片地图下载器  多线程下载选定的缩放范围

## 瓦片地图来源地址
修改Python源码内的URL，默认包含以下瓦片地址：谷歌、mapquest、高德。
```Python
URL = {
    "google":"http://mt2.google.cn/vt/lyrs=m@167000000&hl=zh-CN&gl=cn&x={x}&y={y}&z={z}&s=Galil",
    "mapquest": "https://b.tiles.mapbox.com/v4/mapquest.osm-vivid-v7/{z}/{x}/{y}@2x.png?access_token=pk.eyJ1IjoibWFwcXVlc3QiLCJhIjoiY2Q2N2RlMmNhY2NiZTRkMzlmZjJmZDk0NWU0ZGJlNTMifQ.mPRiEubbajc6a5y9ISgydg",
    "gaode": "http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}",
    "default":"http://mt2.google.cn/vt/lyrs=m@167000000&hl=zh-CN&gl=cn&x={x}&y={y}&z={z}&s=Galil",
}
```

## 配置程序config
其中“地图地址”须与Python源码内的URL对应，此处选择谷歌地图
“根路径”+“项目名”为地图下载至本地的保存路径
```conf
[config]
最小级别 = 10
最大级别 = 12
根路径 = D:/tile
项目名 = google
地图地址 = google
线程数 = 1
```
