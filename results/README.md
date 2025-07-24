# Conjunto de Dados: Análise de Desempenho do Jetson Xavier NX

Este arquivo `inferences.csv` contém os dados brutos, quadro a quadro, coletados durante os experimentos de análise de desempenho da plataforma NVIDIA Jetson Xavier NX. O objetivo do estudo foi avaliar o impacto de diferentes modos de energia e resoluções de vídeo na velocidade de inferência e na eficácia de detecção do modelo YOLOv8m.

## Estrutura do Arquivo

O arquivo está no formato CSV (Comma-Separated Values). Ele é composto por mais de 200.000 linhas, onde cada linha representa a inferência de um único quadro de vídeo para uma configuração experimental específica.

## Descrição das Colunas

| Nome da Coluna | Tipo de Dado | Descrição |
| :--- | :--- | :--- |
| `run_id` | Inteiro | O identificador da repetição do experimento, variando de 1 a 10 para cada configuração. |
| `video_name` | Texto | O nome do arquivo de vídeo utilizado como carga de trabalho (workload). |
| `resolution` | Texto | A resolução do vídeo de entrada processado. Valores possíveis: '480p', '720p', '1080p'. |
| `power_mode` | Texto | O modo de energia configurado no Jetson. Valores possíveis: 'low' (baixo desempenho) ou 'high' (alto desempenho). |
| `frame_id` | Inteiro | O número do quadro (frame) dentro do vídeo, variando de 0 a aproximadamente 1799. |
| `tempo_ms` | Numérico | O tempo de inferência para aquele quadro específico, medido em milissegundos (ms). |
| `detected` | Inteiro | A quantidade de pessoas detectadas pelo modelo YOLOv8m no quadro correspondente. |

## Divisão Experimental

Os dados foram gerados a partir de um design fatorial completo, cobrindo todas as combinações dos seguintes fatores e níveis:

* **Fator 1: Vídeo de Carga de Trabalho (`video_name`)** - 2 níveis
* **Fator 2: Modo de Energia (`power_mode`)** - 2 níveis (`low`, `high`)
* **Fator 3: Resolução do Vídeo (`resolution`)** - 3 níveis (`480p`, `720p`, `1080p`)

Isso resulta em 12 "presets" ou configurações únicas (ex: `video1, low, 480p`). Cada um desses presets foi executado 10 vezes (`run_id`) para garantir a robustez estatística, totalizando **120 execuções**.

Cada execução processou um vídeo inteiro, gerando aproximadamente **1800 inferências** (uma por quadro).
