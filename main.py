import cv2
import hashlib
import os

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def image_forgery_detection(original_path, manipulated_path):
    # Read images
    original_image = cv2.imread(original_path)
    manipulated_image = cv2.imread(manipulated_path)

    # Resize images to the same dimensions
    original_image = cv2.resize(original_image, (256, 256))
    manipulated_image = cv2.resize(manipulated_image, (256, 256))

    # Calculate MD5 hash for each image
    original_hash = calculate_md5(original_path)
    manipulated_hash = calculate_md5(manipulated_path)

    # Compare hashes
    if original_hash == manipulated_hash:
        print("Images are identical. No forgery detected.")
    else:
        print("Images are different. Forgery detected.")

if __name__ == "__main__":
    original_image_path = "E:\ISHA PRGM\Image forgery detection\image 1.jpg"
    manipulated_image_path = "E:\ISHA PRGM\Image forgery detection\image 2.jpg"

    if os.path.exists(original_image_path) and os.path.exists(manipulated_image_path):
        image_forgery_detection(original_image_path, manipulated_image_path)
    else:
        print("File not found.")

