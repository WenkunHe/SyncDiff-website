import os
import cv2
from tqdm import tqdm
import numpy as np

video_paths = os.listdir('./')

for video_path in video_paths:
    print(video_path)
    if 'CORE4D_baseline.mp4' in video_path:
        cap = cv2.VideoCapture(video_path)

        fps = cap.get(cv2.CAP_PROP_FPS)

        frame_count = 0
        #frames = []

        output_video_path = video_path.replace('.mp4', '_.mp4')
        #fps = 15
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        size = (1024, 374*2)
        video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, size)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            print(frame_count)

            new_frame = np.zeros_like(frame)
            
            if frame.shape == (374, 1024, 3):
                new_frame[:, :512, :] = frame[:, 512:, :]
                new_frame[:, 512:, :] = frame[:, :512, :]
            elif frame.shape == (374, 1536, 3):
                new_frame[:, :512, :] = frame[:, 1024:, :]
                new_frame[:, 512:, :] = frame[:, :1024, :]
            elif frame.shape == (374, 2048, 3):
                new_frame = np.zeros((374*2, 1024, 3), dtype=np.uint8)
                new_frame[:374, :512, :] = frame[:374, 1536:, :]
                new_frame[:374, 512:, :] = frame[:, 1024:1536, :]
                new_frame[374:, :, :] = frame[:, :1024, :]
            elif frame.shape == (750, 3072, 3):
                new_frame[:, :1024, :] = frame[:, 2048:, :]
                new_frame[:, 1024:, :] = frame[:, :2048, :]
            else:
                new_frame[:, :, :] = frame[:, :, :]
            
            mask = (new_frame.astype(np.int32).sum(axis=2)) >= 720
            #print(np.sum(mask))
            #print(new_frame[5, 5])
            new_frame[mask, 0] = new_frame[mask, 1] = new_frame[mask, 2] = 255
            #print(new_frame[5, 5])

            #frames.append(new_frame)
            #print(len(frames))
            #if len(frames) >= 300:
            #    break
            video_writer.write(new_frame)
            #if frame_count == 100:
            #    break

        

        #print('Here!')
        #import sys
        #sys.exit(1)
        
            #cv2.imwrite('./frame.png', frame)
        
        video_writer.release()