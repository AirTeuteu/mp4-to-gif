import os
import subprocess
import shutil
import time

print("\033[92mInit...\033[0m")

# Paramètres
input_directory = os.getcwd()
gif_fps = 8
watermark_text = 'www.st-network.com'
watermark_fontsize = 14
output_dimension_max = 512
output_quality = 50
temp_image_dir = "temp_images_mp4"

try:

    def convert_video_to_gif(input_file_path, output_file_path, gif_fps=gif_fps, watermark_fontsize=watermark_fontsize, output_dimension_max=output_dimension_max, output_quality=output_quality):
        
        print(f"  Création du repertoire temporaire...")
        os.makedirs(temp_image_dir, exist_ok=True)

        print(f"  Extraction des frames...")
        subprocess.run(["ffmpeg", "-i", input_file_path, "-vf", f"fps={gif_fps}", "-loglevel", "error", f"{temp_image_dir}/frame_%05d.png"])

        print(f"  Resize des images...")
        subprocess.run(["ffmpeg", "-i", f"{temp_image_dir}/frame_%05d.png", "-vf", f"scale=iw*min({output_dimension_max}/iw\\,{output_dimension_max}/ih):ih*min({output_dimension_max}/iw\\,{output_dimension_max}/ih)", "-loglevel", "error", f"{temp_image_dir}/resized_frame_%05d.png"])

        print(f"  Ajout du watermark...")
        subprocess.run(["mogrify", "-gravity", "SouthEast", "-geometry", "+10+0", "-pointsize", str(watermark_fontsize), "-fill", "white", "-annotate", "+10+0", watermark_text, f"{temp_image_dir}/*.png"], shell=True)

        print(f"  Génération du gif...")
        subprocess.run(["ffmpeg", "-framerate", str(gif_fps), "-i", f"{temp_image_dir}/resized_frame_%05d.png", "-c:v", "gif", "-b:v", "2M", "-loop", "0", "-loglevel", "error", output_file_path])

        print(f"  Suppression du repertoire temporaire...")
        shutil.rmtree(temp_image_dir)


    def convert_video_to_gif_cr(input_file_path, output_file_path, gif_fps=gif_fps, watermark_fontsize=watermark_fontsize, output_dimension_max=output_dimension_max, output_quality=output_quality):
        
        progress_bar = [
            "[X_____]",
            "[XX____]",
            "[XXX___]",
            "[XXXX__]",
            "[XXXXX_]",
            "[XXXXXX]"
        ]
        
        # .ljust(70) ajoute des espaces pour effacer la ligne précédente si elle était plus longue
        print(f"  {progress_bar[0]} Création du repertoire temporaire...".ljust(70), end='\r')
        os.makedirs(temp_image_dir, exist_ok=True)

        print(f"  {progress_bar[1]} Extraction des frames...".ljust(70), end='\r')
        subprocess.run(["ffmpeg", "-i", input_file_path, "-vf", f"fps={gif_fps}", "-loglevel", "error", f"{temp_image_dir}/frame_%05d.png"])

        print(f"  {progress_bar[2]} Resize des images...".ljust(70), end='\r')
        subprocess.run(["ffmpeg", "-i", f"{temp_image_dir}/frame_%05d.png", "-vf", f"scale=iw*min({output_dimension_max}/iw\\,{output_dimension_max}/ih):ih*min({output_dimension_max}/iw\\,{output_dimension_max}/ih)", "-loglevel", "error", f"{temp_image_dir}/resized_frame_%05d.png"])

        print(f"  {progress_bar[3]} Ajout du watermark...".ljust(70), end='\r')
        subprocess.run(["mogrify", "-gravity", "SouthEast", "-geometry", "+10+0", "-pointsize", str(watermark_fontsize), "-fill", "white", "-annotate", "+10+0", watermark_text, f"{temp_image_dir}/*.png"], shell=True)

        print(f"  {progress_bar[4]} Génération du gif...".ljust(70), end='\r')
        subprocess.run(["ffmpeg", "-framerate", str(gif_fps), "-i", f"{temp_image_dir}/resized_frame_%05d.png", "-c:v", "gif", "-b:v", "2M", "-loop", "0", "-loglevel", "error", output_file_path])

        print(f"  {progress_bar[5]} Suppression du repertoire temporaire...".ljust(70), end='\r')
        shutil.rmtree(temp_image_dir)

    all_mp4_files = [filename for filename in os.listdir(input_directory) if filename.endswith(".mp4")]
    files_to_process = []
    
    print(f"\033[94mAnalyse de {len(all_mp4_files)} fichier(s) .mp4...\033[0m")
    for filename in all_mp4_files:
        output_file_path = os.path.join(input_directory, f"{os.path.splitext(filename)[0]}.gif")
        if os.path.exists(output_file_path):
            print(f"\033[93m  -> {filename} a déjà été traité (sera sauté).\033[0m")
        else:
            files_to_process.append(filename)
    
    total_files = len(files_to_process)
    
    if total_files == 0:
        print("\033[92mAucun nouveau fichier à convertir.\033[0m")
    else:
        print(f"\033[92m{total_files} fichier(s) à convertir.\033[0m")
        print()
        
    # Démarrer le chronomètre global
    start_time = time.time()

    for i, filename in enumerate(files_to_process, start=1):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(input_directory, f"{os.path.splitext(filename)[0]}.gif")

        # La vérification d'existence est déjà faite, on convertit directement
        print(f" [{i}/{total_files}] Début de conversion de \033[92m{filename}\033[0m")
        
        # Démarrer le chronomètre pour CETTE étape
        step_start_time = time.time()
        
        # Ligne 2 (dynamique) : Appel de la fonction qui va se mettre à jour sur place
        convert_video_to_gif_cr(input_file_path, output_file_path, gif_fps, watermark_fontsize, output_dimension_max, output_quality)
        
        # Calculer le temps de CETTE étape
        step_elapsed_sec = int(time.time() - step_start_time)
        
        # Ligne 2 (finale)
        print(f"  [XXXXXX] Terminé en {step_elapsed_sec}s".ljust(70))
        
        # --- Calcul et affichage de l'estimation ---
        current_time = time.time()
        elapsed_time = current_time - start_time  # Temps écoulé total
        avg_time_per_file = elapsed_time / i       # Temps moyen par fichier
        files_remaining = total_files - i          # Fichiers restants
        etr_seconds = avg_time_per_file * files_remaining # Estimation temps restant (sec)

        # Formatage du temps écoulé
        elapsed_min = int(elapsed_time // 60)
        elapsed_sec = int(elapsed_time % 60)
        
        # Formatage du temps restant
        etr_min = int(etr_seconds // 60)
        etr_sec = int(etr_seconds % 60)
        
        # Ligne 3
        print(f"  Temps restant: \033[94m{etr_min}m {etr_sec}s\033[0m".ljust(70))
        
        print() # Ajoute une ligne vide pour séparer les traitements

    print("\033[92mToutes les conversions sont terminées.\033[0m")
    print()
    input("\033[92m => Appuyez sur Entrée pour fermer la fenêtre...\033[0m")

except Exception as e:
    # Afficher l'erreur
    # En cas d'erreur, on saute une ligne pour ne pas effacer le message d'erreur
    print() 
    print(f"\033[91m Une erreur s'est produite: {e} \033[0m")
    # Ajouter une pause pour voir l'erreur avant de fermer
    input("Appuyez sur Entrée pour fermer la fenêtre...")

