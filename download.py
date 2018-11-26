import os
from get_links import output_folder, links_files_name
import glob


links_files = glob.glob(os.path.join(output_folder, "*", links_files_name))


def get_links_from_file(file_name):
    with open(file_name, 'r') as f:
        return f.read().split("\n")


def download_links(dest_folder, links):
    for l in links:
        os.system('youtube-dl -o "{output_dir}\%(title)s-%(id)s.%(ext)s" {link}'.format(output_dir=dest_folder, link=l))


def do():
    for f in links_files:
        current_links = get_links_from_file(f)
        download_links(os.path.dirname(f), current_links)


if __name__ == "__main__":
    do()



