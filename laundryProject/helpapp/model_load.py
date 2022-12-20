import csv
import torch
from laundryProject.settings import *
# Yoloの重みファイルをロード ＞ 呼び出し毎にロードされないようにすることでメモリがパンクしない
path_hubconfig = "yolo"
path_weightfile = "yolo/729x300_yolov5m_best.pt" 
MODEL = torch.hub.load(path_hubconfig, 'custom',path=path_weightfile, source='local')

washingProcesses, bleachingProcesses, tumbleDrys, naturalDrys, ironFinishs, tightens, dryCleanings, wetCleanings, info = [],[],[],[],[],[],[],[],[]
# CSV読み込み
with open(STATIC_ROOT + '/csv/washingProcesses.csv',encoding="utf-8") as f:
    for row in csv.reader(f):
        washingProcesses.append(row)
with open(STATIC_ROOT + '/csv/bleachingProcesses.csv',encoding="utf-8") as f:
    for row in csv.reader(f):
        bleachingProcesses.append(row)
with open(STATIC_ROOT + '/csv/tumbleDrys.csv',encoding="utf-8") as f:
    for row in csv.reader(f):
        tumbleDrys.append(row)
with open(STATIC_ROOT + '/csv/naturalDrys.csv',encoding="utf-8") as f:
    for row in csv.reader(f):
        naturalDrys.append(row)
with open(STATIC_ROOT + '/csv/ironFinishs.csv',encoding="utf-8") as f:
    for row in csv.reader(f):
        ironFinishs.append(row)
with open(STATIC_ROOT + '/csv/tighten.csv',encoding="utf-8") as f:
    for row in csv.reader(f):
        tightens.append(row)
with open(STATIC_ROOT + '/csv/dryCleanings.csv',encoding="utf-8") as f:
    for row in csv.reader(f):
        dryCleanings.append(row)
with open(STATIC_ROOT + '/csv/wetCleanings.csv',encoding="utf-8") as f:
    for row in csv.reader(f):
        wetCleanings.append(row)
f = open(STATIC_ROOT + '/csv/info.txt', 'r', encoding='UTF-8')
info = f.read()
f.close
tables = [
    ['washingProcesses', '洗濯処理', washingProcesses], 
    ['bleachingProcesses', '漂白処理', bleachingProcesses], 
    ['tumbleDrys', 'タンブル乾燥', tumbleDrys], 
    ['naturalDrys', '自然乾燥', naturalDrys], 
    ['ironFinishs', 'アイロン仕上げ', ironFinishs],
    ['tightens', '絞り方', tightens],
    ['dryCleanings', 'ドライクリーニング', dryCleanings], 
    ['wetCleanings', 'ウエットクリーニング', wetCleanings], 
    ['info', '注意事項', info]
]