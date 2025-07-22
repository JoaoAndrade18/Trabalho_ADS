import cv2
import time
import os
import torch
import csv
import gc
import subprocess
from pathlib import Path
from ultralytics import YOLO
from configs import configs

def set_jetson_power_mode(mode_id):
    try:
        print(f"[INFO] Alterando para modo {mode_id}...")
        subprocess.run(['sudo', 'nvpmodel', '-m', str(mode_id)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] Falha ao ajustar modo de desempenho: {e}")

def start_model(resolution):

    model_name = "yolov8m.pt"

    print("[INFO] Carregando modelo...")
    try:
        model = YOLO(model_name)
        model.to('cuda')

    except Exception:
        raise ValueError(f"[ERROR] Error loading model engine {model_name}")
    return model

def process_video_inference(video_path, model, frame_rate, resolution, conf_thres, exec_id, preset_level):
    width, height = {
        "480p": (640, 480),
        "720p": (1280, 736),
        "1080p": (1920, 1088)
    }[resolution]

    print("[INFO] Iniciando inferência direta no vídeo...")
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = max(fps // frame_rate, 1)

    results = []
    frame_id = 0
    processed = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_id % frame_interval == 0:
            resized = cv2.resize(frame, (width, height))
            start = time.time()
            result = model(resized, device=0, half=True, imgsz=(height, width), classes=[0])[0]
            elapsed_time = time.time() - start

            n_peoples = 0
            if result.boxes is not None:
                cls_ids = result.boxes.cls.cpu().numpy()
                n_peoples = int((cls_ids == 0).sum())

            results.append({
                "frame_id": processed,
                "detected": n_peoples,
                "tempo_ms": round(elapsed_time * 1000, 2)
            })

            processed += 1
        frame_id += 1

    cap.release()
    torch.cuda.empty_cache()
    gc.collect()

    save_csv_detalhado(video_path, results, configs["output"]["summary_csv"], resolution, preset_level, exec_id, resolution)

def save_csv_detalhado(video_path, results, detailed_csv_path, execution_name, preset_level, exec_id, resolution):
    output_dir = Path(detailed_csv_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    file_exists = os.path.isfile(detailed_csv_path)

    with open(detailed_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            'run_id', 'video_name', 'resolution', 'power_mode',
            'frame_id', 'tempo_ms', 'detected'
        ])
        if not file_exists:
            writer.writeheader()

        for r in results:
            writer.writerow({
                'run_id': exec_id,
                'video_name': Path(video_path).stem,
                'resolution': resolution,
                'power_mode': preset_level,
                'frame_id': r['frame_id'],
                'tempo_ms': r['tempo_ms'],
                'detected': r['detected']
            })

# --- MAIN LOOP ---
videos = [
    os.path.join(configs["video_settings"]["input_folder"], f)
    for f in os.listdir(configs["video_settings"]["input_folder"])
    if f.endswith(".mp4")
]

count = 2

for video in videos:
    video_name = Path(video).stem

    for level_name in [n['name'] for n in configs['processing_levels']]:
        level_id = 3 if level_name == "low" else 8

        print(f"[INFO] Level seted {level_id}")
        set_jetson_power_mode(level_id)

        for resolution in configs['video_settings']['resolutions']:
            print(f"[INFO] Resolução atual: {resolution}")
            model = start_model(resolution)

            if count > 0:
                count -= 1
                continue

            for i in range(1, configs['executions']['per_combination'] + 1):
                print(f"[INFO] Execução: {video} - {resolution} - {level_name} - {i}")
                process_video_inference(
                    video_path=video,
                    model=model,
                    frame_rate=configs['video_settings']['frame_rate'],
                    resolution=resolution,
                    conf_thres=configs['model']['confidence_threshold'],
                    exec_id=i,
                    preset_level=level_name
                )

                gc.collect()
                torch.cuda.empty_cache()