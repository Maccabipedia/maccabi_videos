import os
import glob
import re

output_folder = "F:\\tmp"
exctracted_xlsx_folder = "F:\\m\\xl\\worksheets"
xmls_path = os.path.join(exctracted_xlsx_folder, "*.xml")
links_files_name = "links.txt"
takzir_bytes_in_hebrew = '\xd7\xaa\xd7\xa7\xd7\xa6\xd7\x99\xd7\xa8'

xmls = glob.glob(xmls_path)


class NotTakzirException(Exception):
    pass


def get_content(file_name):
    with open(file_name, 'r') as f:
        return f.read()


def extract_link(wrapped_link):
    without_hyperlink_prefix = wrapped_link.split("HYPERLINK")[1]  # ['<f>', '("https://www.youtube.com/watch?v=rT1ruf9IlaQ","\xd7\xaa\xd7\xa7\xd7\xa6\xd7\x99\xd7\xa8")</f>']
    without_suffix_ftag = without_hyperlink_prefix.split("</f>")[0]  # ("https://www.youtube.com/watch?v=rT1ruf9IlaQ","\xd7\xaa\xd7\xa7\xd7\xa6\xd7\x99\xd7\xa8")
    link_and_description = eval(without_suffix_ftag)
    # Only takzir:
    if link_and_description[1] == takzir_bytes_in_hebrew:
        return link_and_description[0]
    else:
        print "no takzir : {t} --- {l}".format(t=link_and_description[1], l=link_and_description[0])
        raise NotTakzirException(link_and_description[1])


def write_to_errors(what):
    with open(os.path.join(output_folder, "errors.txt"), 'a') as ff:
        ff.write(what)
        ff.write("\n")


def get_links_from_files(file_name):
    wrapped_links = re.findall('<f>[^<]+<\/f>', get_content(file_name))
    final_links = []
    for wrapped in wrapped_links:
        try:
            just_link = extract_link(wrapped)
            if "youtube" in just_link:
                final_links.append(extract_link(wrapped))
            else:
                write_to_errors(wrapped + ":::" + os.path.splitext(os.path.basename(file_name))[0])
        except NotTakzirException as e:
            write_to_errors(wrapped + ":::" + e.message + ":::" + os.path.splitext(os.path.basename(file_name))[0])
        except Exception as e:
            write_to_errors("Exception: " + wrapped + ":::" + e.message + ":::" + os.path.splitext(os.path.basename(file_name))[0])

    return final_links


def create_dir(xml):
    full_dir_path = os.path.join(output_folder, os.path.splitext(os.path.basename(xml))[0])

    if not os.path.isdir(full_dir_path):
        os.mkdir(full_dir_path)

    return full_dir_path


def save_links(dir_path, links):
    with open(os.path.join(dir_path, links_files_name), 'w') as f:
        f.write("\n".join(links))


def do():
    for xml in xmls:
        dir_path = create_dir(xml)
        save_links(dir_path, get_links_from_files(xml))


if __name__ == "__main__":
    do()

