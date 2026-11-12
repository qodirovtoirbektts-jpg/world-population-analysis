"""
Kaggle Kernel & Dataset Downloader / Connector
Dunyo aholisi o'sishi va demografik tahlil (World Population Analysis)

Ushbu skript Hasib Al Muzdadidning 'world-population-analysis' Kaggle kernelini
va 'iamsouravbanerjee/world-population-dataset' ma'lumotlar to'plamini yuklab olish va 
loyihaga ulash uchun xizmat qiladi.
"""

import os
import sys
import json
import urllib.request
import shutil
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
DATASET_FILE = DATA_DIR / "world_population.csv"
KERNEL_SLUG = "hasibalmuzdadid/world-population-analysis"

def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def pull_kaggle_kernel_direct(kernel_ref=KERNEL_SLUG):
    """
    Kaggle API orqali kernel faylini (notebook) to'g'ridan-to'g'ri yuklab oladi.
    CLI komandasi ekvivalenti:
    kaggle kernels pull hasibalmuzdadid/world-population-analysis
    """
    print(f"[*] Kaggle kernelini tortib olinmoqda: {kernel_ref}...")
    parts = kernel_ref.split("/")
    if len(parts) != 2:
        raise ValueError("Kernel formati 'username/kernel-slug' ko'rinishida bo'lishi kerak!")
    
    username, slug = parts
    url = f"https://www.kaggle.com/api/v1/kernels/pull?userName={username}&kernelSlug={slug}"
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        
        blob_source = data.get("blob", {}).get("source")
        if blob_source:
            notebook_path = Path(__file__).resolve().parent / "world_population_analysis.ipynb"
            with open(notebook_path, "w", encoding="utf-8") as f:
                f.write(blob_source)
            print(f"[+] Kaggle daftari muvaffaqiyatli saqlandi: {notebook_path.name}")
            return notebook_path
        else:
            print("[!] Blob topilmadi, metadata:", data.get("metadata", {}))
    except Exception as e:
        print(f"[-] Kernel yuklab olishda xatolik: {e}")
        print("    Muqobil: CLI orqali quyidagi komandani bering:")
        print(f"    kaggle kernels pull {kernel_ref}")
    return None

def download_dataset():
    """
    World Population datasetini tekshiradi va kerak bo'lsa kagglehub orqali yuklab oladi.
    """
    ensure_data_dir()
    if DATASET_FILE.exists() and DATASET_FILE.stat().st_size > 1000:
        print(f"[+] Dataset mavjud: {DATASET_FILE} ({DATASET_FILE.stat().st_size} bayt)")
        return DATASET_FILE
    
    print("[*] Dataset internetdan yuklab olinmoqda (kagglehub)...")
    try:
        import kagglehub
        path = kagglehub.dataset_download("iamsouravbanerjee/world-population-dataset")
        src_file = Path(path) / "world_population.csv"
        if src_file.exists():
            shutil.copy(src_file, DATASET_FILE)
            print(f"[+] Dataset muvaffaqiyatli yuklandi: {DATASET_FILE}")
            return DATASET_FILE
    except Exception as e:
        print(f"[-] kagglehub orqali yuklab bo'lmadi: {e}")
    
    return DATASET_FILE if DATASET_FILE.exists() else None

if __name__ == "__main__":
    print("=" * 60)
    print("Dunyo Aholisi Tahlili - Kaggle Ulanishi va Dataset Tayyorlash")
    print("=" * 60)
    pull_kaggle_kernel_direct()
    download_dataset()
    print("Tayyor!")
