import os
import subprocess
import shutil

print("\033[92mInit...\033[0m")

# Paramètres
input_directory = os.getcwd()
gif_fps = 10
watermark = 'your watermark'
fontsize = 14
target_dimension = 512
quality = 50

def convert_video_to_gif(input_file_path, output_file_path, gif_fps=gif_fps, fontsize=fontsize, target_dimension=target_dimension, quality=quality):
    # Créer un répertoire temporaire pour stocker les images
    temp_image_dir = "temp_images"
    os.makedirs(temp_image_dir, exist_ok=True)

    print(f"\033[92mExtraction des frames...\033[0m")
    # Charger la vidéo et extraire les images dans le répertoire temporaire
    subprocess.run(["ffmpeg", "-i", input_file_path, "-vf", f"fps={gif_fps}", f"{temp_image_dir}/frame_%05d.png"])

    print(f"\033[92mResize des images...\033[0m")
    # Déterminer les dimensions maximales tout en préservant le rapport d'aspect
    subprocess.run(["ffmpeg", "-i", f"{temp_image_dir}/frame_%05d.png", "-vf", f"scale=iw*min({target_dimension}/iw\\,{target_dimension}/ih):ih*min({target_dimension}/iw\\,{target_dimension}/ih)", f"{temp_image_dir}/resized_frame_%05d.png"])

    print(f"\033[92mAjout du watermark...\033[0m")
    # Ajouter le watermark à chaque image
    subprocess.run(["mogrify", "-gravity", "SouthEast", "-geometry", "+10+0", "-pointsize", str(fontsize), "-fill", "white", "-annotate", "+10+0", watermark, f"{temp_image_dir}/*.png"], shell=True)

    print(f"\033[92mCréation du gif...\033[0m")
    # Utiliser ImageMagick pour créer le GIF à partir des images avec une durée totale spécifique
    subprocess.run(["ffmpeg", "-framerate", str(gif_fps), "-i", f"{temp_image_dir}/resized_frame_%05d.png",
                    "-c:v", "gif", "-b:v", "2M", "-loop", "0", output_file_path])

    # Supprimer le répertoire temporaire des images
    shutil.rmtree(temp_image_dir)


for filename in os.listdir(input_directory):
    if filename.endswith(".mp4"):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(input_directory, f"{os.path.splitext(filename)[0]}.gif")
        print(f"\033[92mDébut de conversion de {filename}\033[0m")
        convert_video_to_gif(input_file_path, output_file_path, gif_fps, fontsize, target_dimension, quality)
        print(f"\033[92mConversion terminée pour {filename}\033[0m")


print("\033[92mToutes les conversions sont terminées.\033[0m")
