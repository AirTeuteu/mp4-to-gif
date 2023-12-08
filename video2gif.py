import os
import subprocess
import shutil

print("\033[92mInit...\033[0m")

# Paramètres
input_directory = os.getcwd()
gif_fps = 10
watermark = 'www.st-network.com'
fontsize = 14
target_dimension = 512
quality = 50
temp_image_dir = "temp_images_mp4"

try:

    def convert_video_to_gif(input_file_path, output_file_path, gif_fps=gif_fps, fontsize=fontsize, target_dimension=target_dimension, quality=quality):
        
        print(f"  Création du repertoire temporaire...")
        os.makedirs(temp_image_dir, exist_ok=True)

        print(f"  Extraction des frames...")
        subprocess.run(["ffmpeg", "-i", input_file_path, "-vf", f"fps={gif_fps}", "-loglevel", "error", f"{temp_image_dir}/frame_%05d.png"])

        print(f"  Resize des images...")
        subprocess.run(["ffmpeg", "-i", f"{temp_image_dir}/frame_%05d.png", "-vf", f"scale=iw*min({target_dimension}/iw\\,{target_dimension}/ih):ih*min({target_dimension}/iw\\,{target_dimension}/ih)", "-loglevel", "error", f"{temp_image_dir}/resized_frame_%05d.png"])

        print(f"  Ajout du watermark...")
        subprocess.run(["mogrify", "-gravity", "SouthEast", "-geometry", "+10+0", "-pointsize", str(fontsize), "-fill", "white", "-annotate", "+10+0", watermark, f"{temp_image_dir}/*.png"], shell=True)

        print(f"  Génération du gif...")
        subprocess.run(["ffmpeg", "-framerate", str(gif_fps), "-i", f"{temp_image_dir}/resized_frame_%05d.png",
                        "-c:v", "gif", "-b:v", "2M", "-loop", "0", "-loglevel", "error", output_file_path])

        print(f"  Suppression du repertoire temporaire...")
        shutil.rmtree(temp_image_dir)

    mp4_files = [filename for filename in os.listdir(input_directory) if filename.endswith(".mp4")]
    for i, filename in enumerate(mp4_files, start=1):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(input_directory, f"{os.path.splitext(filename)[0]}.gif")
        print(f"\033[92m [{i}/{len(mp4_files)}] Début de conversion de {filename} \033[0m")
        convert_video_to_gif(input_file_path, output_file_path, gif_fps, fontsize, target_dimension, quality)
        print(f"\033[92m [{i}/{len(mp4_files)}] Conversion terminée pour {filename} \033[0m")
        print()
    print("\033[92mToutes les conversions sont terminées.\033[0m")
    print()
    input("\033[92m => Appuyez sur Entrée pour fermer la fenêtre...\033[0m")
except Exception as e:
    # Afficher l'erreur
    print(f"\033[91m Une erreur s'est produite: {e} \033[0m")
    # Ajouter une pause pour voir l'erreur avant de fermer
    input("Appuyez sur Entrée pour fermer la fenêtre...")
