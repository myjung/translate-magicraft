import pathlib
import logging
import zipfile
import os
import json
import shutil
from datetime import datetime


# pypi packages
import UnityPy
import toml
import argparse



def make_korean_string_table(input_file_path:str)->dict:
    output = dict()
    with open(input_file_path,"r", encoding='utf-8', newline="\r\n") as f:
        f.readline()
        for line in f:
            if not line:
                continue
            try:
                which_asset, id, chinese_s, _, _,_,_,_,korean = line.strip().split("\t")
                korean = korean.rstrip()
                if korean:
                    # print(which_asset)
                    output.setdefault(which_asset,dict())
                    output[which_asset].setdefault(id, dict())
                    output[which_asset][id] = korean
                else:
                    print(line)
            except ValueError as e:
                print(line.strip().split("\t"))
                # print(e)
    return output

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Translate Fate Seeker 1")

    # Add the arguments
    parser.add_argument("-b", "--backup", action="store_true", help="Extract files")
    parser.add_argument("-e", "--extract", action="store_true", help="Extract Keywords")
    parser.add_argument("-p", "--patch", action="store_true", help="Make patch")

    # Parse the command-line arguments
    args = parser.parse_args()
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()],
    )

    setting_path = pathlib.Path(os.curdir).absolute().joinpath("localconfig.toml")
    asset_path = "Magicraft_Data/resources.assets"
    loaded_toml = toml.load(setting_path)
    backup_dir = pathlib.Path("./backup")
    working_dir = pathlib.Path("./working")
    if args.backup:
        # Extract config files
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(resource_asset_path, backup_dir.joinpath("resources.assets"))
        resource_asset_path = pathlib.Path(loaded_toml['local']['GAME_PATH']).joinpath(asset_path)
        shutil.copyfile(resource_asset_path, backup_dir.joinpath("resources.assets"))

    if args.extract:
        # Extract keywords
        # todo: make extract keywords
        pass

    if args.patch:
        # # Make patch
        shutil.copyfile(backup_dir.joinpath("resources.assets"), working_dir.joinpath("resources.assets"))
        env = UnityPy.load(open(working_dir.joinpath("resources.assets"), 'rb').read())
        translated = make_korean_string_table("./docs/translated.tsv")
        extracted_objects = dict()
        for obj in env.objects:
            if obj.type.name == "TextAsset":
                data = obj.read()
                if "TextConfig" in data.m_Name:
                    # print(repr(data.m_Script))
                    # break
                    extracted_objects[data.m_Name] = data
        
        current_time = datetime.now().strftime("%y%m%d%H%M")
        zipf = zipfile.ZipFile(f"./dist/MagicraftKorean_{current_time}.zip", "w", zipfile.ZIP_DEFLATED)
        zipf.write("readme-patchInfo.txt")
        for k, v in extracted_objects.items():
            print(k)
            new_texts = json.loads(v.m_Script)
            if k in translated:
                print("found")
                for text in new_texts:
                    if nt := translated[k].get(str(text["id"]),""):
                        text["english"] = nt
            else:
                print("not found")
            v.m_Script = json.dumps(new_texts, ensure_ascii=False, indent=2)
            v.save()
        
        with open(working_dir.joinpath("resources.assets"), 'wb') as f:
            f.write(env.file.save())
        zipf.write(working_dir.joinpath("resources.assets"), asset_path)
        # # zip 파일을 닫습니다
        zipf.close()
        pass

    if not args.backup and not args.extract and not args.patch:
        parser.print_help()


if __name__ == "__main__":
    main()
