configs = {
    "video_settings": {
        "input_folder": "videos/",
        "frame_rate": 1,
        "resolutions": ["480p", "720p", "1080p"]
    },
    "processing_levels": [
        {
        "name": "low",
        "description": "Modo 10W com 2 núcleos e GPU reduzida",
        "id": 3
        },
        {
        "name": "Alto",
        "description": "Modo 20W com 8 núcleos e GPU plena",
        "id": 8
        }
    ],
    "model": {
        "path": "modelos/yolov8n.engine",
        "confidence_threshold": 0.3,
        "iou_threshold": 0.5
    },
    "metrics": [
        {
        "nome": "acuracia",
        "descricao": "Pessoas detectadas / pessoas esperadas"
        },
        {
        "nome": "tempo_medio",
        "descricao": "Tempo médio por frame em milissegundos"
        }
    ],
    "executions": {
        "per_combination": 10,
        "videos_level": 2,
        "presets": 2,
        "total_executions": 120
    },
    "output": {
        "summary_csv": "results/inferences.csv"
    },
    "version": "1.0",
    "date": "2025-06-29"
}