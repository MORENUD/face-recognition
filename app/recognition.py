import os
import numpy as np
from PIL import Image

IMAGE_SIZE = (224, 224)

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
DATABASE_FOLDER = os.path.join(project_root, "database_img")

MOCK_PATIENT_DB = {
    "Sarah": {
        "disease": "Diabetes",
        "appointment_day": 53
    },
    "Peter": {
        "disease": "Typhoid",
        "appointment_day": 21
    }
}

def process_image_to_vector(image: Image.Image):
    img_processed = image.convert("RGB").convert("L").resize(IMAGE_SIZE)
    vec = np.array(img_processed).flatten().astype(float)
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm

def load_database_from_folder(folder_path=DATABASE_FOLDER):
    db = {}
    
    if not os.path.exists(folder_path):
        print(f"Warning: Database folder not found at {folder_path}")
        return db

    print(f"Loading images from: {folder_path}")
    
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    for filename in files:
        filepath = os.path.join(folder_path, filename)
        try:
            with Image.open(filepath) as img:
                vector = process_image_to_vector(img)
                db[filename] = vector
                print(f"Loaded: {filename}")
        except Exception as e:
            print(f"Failed to load {filename}: {e}")
            pass
            
    return db

def find_match(target_vector, database, threshold=0.8):
    best_name = "No match"
    highest_score = -1.0
    
    for name, db_vector in database.items():
        score = np.dot(target_vector, db_vector)
        
        if score > highest_score:
            highest_score = score
            best_name = name
            
    if highest_score >= threshold:
        return best_name, float(highest_score)
    else:
        return "No match", float(highest_score)

def get_patient_info(filename):
    if filename == "No match":
        return None
    
    name_key = os.path.splitext(filename)[0]
    return MOCK_PATIENT_DB.get(name_key)