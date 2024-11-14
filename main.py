import pathlib
import logging
import zipfile
import os
from datetime import datetime

# pypi packages
import toml
import argparse

# custom packages
from patcher.extractor import FateSeeker1Patcher, FateSeeker1MetaInfo, FateSeeker1PatchHelper, FateSeekerCsvParser


def make_korean_string_table(input_file_path:str)->dict:
    output = dict()
    with open(input_file_path,"r",encoding="utf8") as f:
        for line in f:
            try:
                rows = line.strip().split("\t")
                id,Key,New = rows[0],rows[1],rows[5]
                output[Key] = New
            except Exception as e:
                print(line, e)
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

    setting_path = pathlib.Path("localconfig.toml")
    fate_patcher = FateSeeker1Patcher(pathlib.Path(os.path.abspath(".")).joinpath("extracted_assets"))
    fate_pach_helper = FateSeeker1PatchHelper(fate_patcher)
    if args.backup:
        # Extract config files
        FateSeeker1Patcher.backup_asset(setting_path)

    if args.extract:
        # Extract keywords
        # patch_helper.extract_every_keywords_to_file("./data/extracted_strings.csv")
        pass

    if args.patch:
        # # Make patch
        i = make_korean_string_table("./docs/input.tsv")
        t = fate_patcher.get_text("assets/forassetbundles/textfiles/localization.csv")
        fs_localizations = FateSeekerCsvParser(t)
        output = fs_localizations.change_by_key(i)
        fate_patcher.set_text("assets/forassetbundles/textfiles/localization.csv", output)
        fate_patcher.save_asset("./build/textfiles")
        current_time = datetime.now().strftime("%y%m%d%H%M")
        zipf = zipfile.ZipFile(f"./release/Fateseeker1Kor_{current_time}.zip", "w", zipfile.ZIP_DEFLATED)
        zipf.write("readme-patchInfo.txt")

        # # ./build 경로의 모든 파일을 /古龙风云录/AssetBundles/ 경로에 추가
        for root, dirs, files in os.walk("./build"):
            for file in files:
                # 파일의 전체 경로를 가져옵니다
                full_path = os.path.join(root, file)
                # zip 파일 내의 경로를 설정합니다
                in_zip_path = os.path.join("FateSeeker/FateSeeker_Data/StreamingAssets/StandaloneWindows64", os.path.relpath(full_path, "./build"))
                # 파일을 zip 파일에 추가합니다
                zipf.write(full_path, in_zip_path)

        # # zip 파일을 닫습니다
        zipf.close()
        pass

    if not args.backup and not args.extract and not args.patch:
        parser.print_help()


if __name__ == "__main__":
    main()
