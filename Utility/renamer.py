import os
import shutil

def rename_images(folder_path, serial_number="000111", batch_number=1):
    foto_number = 1
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            # Generate new filename
            new_filename = f"{serial_number}_{batch_number}_{foto_number}.jpg"

            # Construct full paths
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_filename)

            # Rename file
            os.rename(old_path, new_path)
            
            # Increment foto number for next image
            foto_number += 1

# Example usage
folder_path ="Fotos"
serial_number = "000111"
batch_number = int(input("Enter batch number: "))
rename_images(folder_path, serial_number, batch_number)
