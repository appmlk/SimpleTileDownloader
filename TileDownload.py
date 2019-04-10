import multiprocessing
import os
import math
import requests
import configparser
# from PIL import Image,ImageFont,ImageDraw
# im=Image.open('car.jpg')
# im=im.rotate(20)
# im1=Image.open('steve.jpg')
# im1.thumbnail((700,400))
# im.paste(im1,(100,70))
# im.show()

URL = {
    "google":"http://mt2.google.cn/vt/lyrs=m@167000000&hl=zh-CN&gl=cn&x={x}&y={y}&z={z}&s=Galil",
    "mapquest": "https://b.tiles.mapbox.com/v4/mapquest.osm-vivid-v7/{z}/{x}/{y}@2x.png?access_token=pk.eyJ1IjoibWFwcXVlc3QiLCJhIjoiY2Q2N2RlMmNhY2NiZTRkMzlmZjJmZDk0NWU0ZGJlNTMifQ.mPRiEubbajc6a5y9ISgydg",
    "gaode": "http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}",
    "default":"http://mt2.google.cn/vt/lyrs=m@167000000&hl=zh-CN&gl=cn&x={x}&y={y}&z={z}&s=Galil",
}

def process_tilenum(minzoom,maxzoom, filename="default", maptype="default",rootpath=".", poolnum=4):
    minzoom=int(minzoom)
    maxzoom=int(maxzoom)+1
    if minzoom>maxzoom:
        print("最大级别比最小级别小")
        return
    if minzoom<0 or maxzoom<0:
        print("级别不能为负数")
    poolnum=int(poolnum)
    download(minzoom,maxzoom, filename, maptype,rootpath,poolnum)


def download(minzoom,maxzoom, filename="default", maptype="default",rootpath=".",poolnum=4):
    pool = multiprocessing.Pool(processes=poolnum)
    for zoom in range(minzoom,maxzoom):
        max=int(math.pow(2,zoom))
        for x in range(max):
            for y in range(max):
                path = rootpath+'/%s/%i/%i/%i.png' % (filename, zoom, x, y)
                if not os.path.exists(path):
                    #_download(x, y, zoom,filename,maptype,rootpath)
                    pool.apply_async(_download,(x, y, zoom,filename,maptype,rootpath))
    pool.close()
    pool.join()


def _download(x, y, z, filename, maptype,rootpath):
    print("正在下载 缩放等级:"+str(z)+" x轴:"+str(x)+" y轴:"+str(y))
    url = URL.get(maptype)
    path = rootpath+'/%s/%i/%i' % (filename, z, x)
    map_url = url.format(x=x, y=y, z=z)
    r = requests.get(map_url)
    if r.status_code!=200:
        return

    if not os.path.isdir(path):
        os.makedirs(path)
    with open('%s/%i.png' % (path, y), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()


def config():
    cf = configparser.ConfigParser()
    cf.read("config.conf", encoding="utf-8-sig")
    minzoom = cf.get("config","最小级别")
    maxzoom = cf.get("config", "最大级别")
    rootpath = cf.get("config","根路径")
    filename = cf.get("config","项目名")
    maptype = cf.get("config","地图地址")
    poolnum = cf.get("config", "线程数")

    process_tilenum(minzoom,maxzoom,filename,maptype,rootpath,poolnum)


if __name__ == '__main__':
    config()