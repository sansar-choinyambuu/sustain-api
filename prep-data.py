import json
import glob
import os
import pickle
from tqdm import tqdm
import time

DATA_DIR = "../data"

products = {}

def prep_data():
    for file in tqdm(glob.glob(f"{DATA_DIR}/products/en/*.json")):
        with open(file, encoding='UTF-8') as f:
            product_id = os.path.splitext(os.path.basename(file))[0]
            products[product_id] = json.load(f).get("m_check2", None)
            time.sleep(1)
    pickle.dump(products, open("products.pickle", "wb" ) )

if __name__ == "__main__":
    prep_data()