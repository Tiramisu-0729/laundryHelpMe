import torch
path_hubconfig = "yolo"
path_weightfile = "yolo/729x300_yolov5m_best.pt" 
MODEL = torch.hub.load(path_hubconfig, 'custom',path=path_weightfile, source='local')
