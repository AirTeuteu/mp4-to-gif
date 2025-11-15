# Convertisseur MP4 vers GIF (MP4 to GIF Converter)

Un simple script Python pour convertir en masse des fichiers `.mp4` en `.gif` animés, avec redimensionnement et ajout d'un filigrane.

A simple Python script to bulk convert `.mp4` files to animated `.gif` files, with resizing and watermarking.

## Description (Français) 🇫🇷

Ce script scanne le dossier dans lequel il se trouve à la recherche de tous les fichiers `.mp4`. Pour chaque fichier trouvé, il effectue les opérations suivantes :

* Convertit la vidéo en une séquence d'images.

* Redimensionne les images (en gardant les proportions).

* Ajoute un filigrane (watermark) en bas à droite.

* Compile les images en un fichier `.gif` animé optimisé.

Les fichiers `.gif` générés sont sauvegardés dans le même dossier.

## Description (English) 🇬🇧

This script scans its current directory for all `.mp4` files. For each file found, it performs the following operations:

* Converts the video into a sequence of frames.

* Resizes the frames (while maintaining aspect ratio).

* Adds a watermark to the bottom-right corner.

* Compiles the frames into an optimized animated `.gif` file.

The generated `.gif` files are saved in the same directory.

## 🚀 Utilisation (Usage)

### 1. Dépendances (Dependencies)

Ce script n'utilise pas de bibliothèques Python externes, mais il dépend de deux outils en ligne de commande très courants :

This script does not use external Python libraries, but it relies on two very common command-line tools:

* **FFmpeg**: Pour l'extraction des images et la création du GIF.

* **ImageMagick**: Pour l'ajout du filigrane (via la commande `mogrify`).

Assurez-vous qu'ils sont installés sur votre système et accessibles depuis votre terminal.
(Make sure they are installed on your system and available in your PATH.)

### 2. Lancement (Running)

1. Placez le script (`mp4-to-gif.py`) dans le dossier contenant vos fichiers `.mp4`.
   (Place the script (`mp4-to-gif.py`) in the directory containing your `.mp4` files.)

2. Ouvrez un terminal dans ce dossier.
   (Open a terminal in that directory.)

3. Exécutez le script :
   (Run the script:)

   ```
   python mp4-to-gif.py
   
   ```

Le script traitera tous les fichiers `.mp4` qui n'ont pas encore de `.gif` correspondant et affichera la progression.
(The script will process all `.mp4` files that do not already have a corresponding `.gif` and will display the progress.)
