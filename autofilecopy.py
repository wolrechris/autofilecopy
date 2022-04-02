import configparser
from shutil import copyfile
from os import listdir, remove
from os.path import exists


# creates full paths for all files of either src or dst of one entry
def get_paths(folder_entry, side):
    file_names = ""
    try:
        file_names = listdir(folder_entry["src"])
    except FileNotFoundError as err:
        if not (config["DEFAULT"]["src"] == err.filename or config["DEFAULT"]["dst"] == err.filename):
            print("The following path you entered could not be found: ", err.filename)
    file_paths = []
    for file in file_names:
        candidate = folder_entry[side] + "/" + file
        if good_path(folder_entry, file):
            file_paths.append(candidate)
    return file_paths


# Returns True, if file path does not contain .DONE (trace file)
# and if dst path does not exist (if skip_existing = True)
def good_path(folder_entry, file):
    if ".DONE" in file:
        return False
    elif folder_entry["skip_existing"] == "True" and exists(folder_entry["dst"] + "/" + file):
        return False
    return True


# Parse config
config = configparser.ConfigParser()
config.read("config.ini")

# Main loop
for entry in config.values():
    print("Moving files from \"" + entry["src"] + "\" to \"" + entry["dst"] + "\"")
    src_paths = get_paths(entry, "src")
    dst_paths = get_paths(entry, "dst")
    i = 0
    while i < len(src_paths):
        print("  Moving file " + src_paths[i])
        copyfile(src_paths[i], dst_paths[i])
        if entry["leave_trace_files"] == "True":
            print("    Creating trace file " + src_paths[i] + ".DONE")
            open(src_paths[i] + ".DONE", "a").close()
        if entry["delete_src_files"] == "True":
            print("    Deleting " + src_paths[i])
            remove(src_paths[i])
        i += 1
