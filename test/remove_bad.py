import os
from ultralytics import YOLO
import cv2

class DetectYellow:

    def __init__(self) -> None:
        # ALL TAGS: #  ['Asshole - Exposed', 'Buttocks - Exposed', 'Buttocks - Panties', 'Female Breast - Bra', 'Female Breast - Exposed', 'Female Genitalia - Exposed', 'Fingers', 'Foot', 'Navel - Exposed', 'Nipple - Exposed', 'Pelvic - Exposed', 'Pelvic - Panties', 'Toy']
        self.model = YOLO('/media/zw/370a04c9-d73f-4abb-93db-ceed43e46020/hugging-face-park/yolov8/runs/detect/train15/weights/best.pt')  # Load a custom trained model
        self.yellow_tags = ['Asshole - Exposed', 'Buttocks - Exposed', 'Buttocks - Panties', 'Female Breast - Exposed', 'Female Genitalia - Exposed', 'Nipple - Exposed', 'Pelvic - Exposed', 'Pelvic - Panties']

    def _is_yellow(self, result):
        import json
        result_list = json.loads(result.tojson())
        result_tags = [item["name"] for item in result_list]
        name_confidence_map = {}
        for item in result_list:
            name_confidence_map[item['name']] = item['confidence']
        # [{'name': 'Female Breast - Bra', 'class': 3, 'confidence': 0.15345139801502228, 'box': {'x1': 152.09429931640625, 'y1': 519.6268920898438, 'x2': 203.56405639648438, 'y2': 599.6094970703125}}
        for tag in result_tags:
            if tag in self.yellow_tags and item['confidence'] > 0.5:
                print(f'【{tag}】')
                return True
        return False

    def detect_yellow(self, image_path: str):
        image = cv2.imread(image_path)
        results = self.model.track(image, persist=True)
        assert len(results) > 0
        return self._is_yellow(results[0])

    
detect_yellow = DetectYellow()
basepath = '/media/zw/370a04c9-d73f-4abb-93db-ceed43e46020/solo-sass/fullstack/upscaler-roop-server/images'
for dir in os.listdir(basepath):
    for image in os.listdir(f'{basepath}/{dir}/'):
        try:
            image_path = f'{basepath}/{dir}/{image}'
            result = detect_yellow.detect_yellow(image_path)
            import subprocess
            if result:
                subprocess.run(f"cp {image_path} ./yellow/", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as e:
            print(e)