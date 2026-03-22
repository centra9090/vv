# VV: Decision Intelligence System (Data-Driven)

Repository: `centra9090/vv` (branch `main`)

## 🎯 Tujuan
Platform ini didesain untuk:
- Validasi insight data via analisis statistik (tanpa AI wajib)
- Identifikasi akar penyebab perubahan metrik secara otomatis
- Rekomendasi keputusan bisnis terukur dengan confidence
- Arsitektur modular dan scalable

## 🗂️ Struktur Proyek
```
vv/
├── LICENSE
├── README.md
├── requirements.txt
├── notebooks/  # placeholder
├── src/
│   ├── __init__.py
│   ├── example.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── analyzer.py
│   │   ├── data_loader.py
│   │   ├── decision_intelligence_system.py
│   │   ├── engines/
│   │   │   ├── audit_trail.py
│   │   │   ├── confidence_engine.py
│   │   │   ├── consistency_engine.py
│   │   │   ├── decision_engine.py
│   │   │   ├── limitation_engine.py
│   │   │   ├── root_cause.py
│   │   │   └── validator.py
│   │   ├── models/
│   │   │   └── models.py
│   │   └── utils/
│   │       └── helpers.py
├── tests/
│   ├── conftest.py
│   ├── test_analyzer.py
│   ├── test_data_loader.py
│   ├── test_engines.py
│   ├── test_system.py
│   └── test_validator.py
```

## 🧩 Komponen Utama
- `core/data_loader.py`: load CSV/Excel, schema validation, clean, quality metrics
- `core/analyzer.py`: statistik, trend, persentase perubahan, root cause candidates, hypothesis test
- `core/engines/validator.py`: parse insight teks, hitung perubahan aktual, status valid/invalid, confidence
- `core/engines/root_cause.py`: kontribusi kelompok per dimensi, root cause utama
- `core/engines/decision_engine.py`: rekomendasi action prioritas
- `core/engines/confidence_engine.py`: scoring confidence integrasi hasil
- `core/engines/limitation_engine.py`: deteksi batasan data
- `core/engines/consistency_engine.py`: validasi konsistensi silang
- `core/engines/audit_trail.py`: logging operasi dan jejak audit
- `core/decision_intelligence_system.py`: orchestrator end-to-end

## 🚀 Instalasi
1. Clone:
```bash
git clone https://github.com/centra9090/vv.git
cd vv
```
2. Setup environment (disarankan virtual env):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Jalankan Demo
```bash
cd src
python example.py
```

## 🧪 Jalankan Test
```bash
pytest -q /workspaces/vv/tests
```

## 📌 Catatan
- `requirements.txt` sudah punya dependency utama: pandas, numpy, scipy, sklearn, matplotlib, seaborn
- Semua test lulus: `9 passed`

## 📄 Lisensi
MIT
