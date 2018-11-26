import os
from get_links import output_folder, links_files_name
from download import get_links_from_file
import glob
from collections import Counter

dup_files_name = "dups.txt"
links_files = glob.glob(os.path.join(output_folder, "*", links_files_name))
dups_files = glob.glob(os.path.join(output_folder, "*", dup_files_name))


def get_links_count(links):
    counted_links = Counter(links)
    return counted_links.most_common()


def write_dups_to_file(links_counts, file_name):
    content = "\n".join(str(i) for i in links_counts)
    with open(file_name, 'w') as f:
        f.write(content)


def do():
    for link_file in links_files:
        unfiltered_links = get_links_from_file(link_file)
        links_by_count = get_links_count(unfiltered_links)
        write_dups_to_file(links_by_count, os.path.join(os.path.dirname(link_file), dup_files_name))


if __name__ == "__main__":
    do()
