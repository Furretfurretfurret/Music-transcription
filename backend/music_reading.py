import os
import subprocess

# os.system('cmd /c "Your Command Prompt Command"')

def scanningMusic(input_path, output_path):
    # print(f'cmd /c "oemer {path_to_sheet}"')
    command = ['oemer', input_path, '-o', output_path, '--save-cache']
    subprocess.run(command, check=True)
    

def folderSheetMusic(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    #     try:
    #         os.makedirs(output_path)
    #         print("Directory created successfully")
    #     except OSError as error:
    #         print("Directory creation failed:", error)
    # else:
    #     print(f"Directory '{dir_name}' already exists")

def main():
    name_of_sheet = 'dragonspine.jpg'
    input_path = os.path.join('..', 'sheets', name_of_sheet)
    output_path = os.path.join('..', 'xmls', name_of_sheet)

    index = output_path.find('.', 2)
    output_path = output_path[0: index]

    folderSheetMusic(output_path)
    scanningMusic(input_path, output_path)

if __name__ == "__main__":
    main()