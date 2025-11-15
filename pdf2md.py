import fitz  # PyMuPDF
from pathlib import Path
import re
from datetime import datetime
import argparse
import sys

try:
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox
except Exception:
    tk = None
    filedialog = None
    messagebox = None

def pdf_to_markdown(pdf_path: str, output_dir: Path):
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")

    # 결과 .md 파일 경로 (출력 폴더, 같은 이름)
    md_path = Path(output_dir) / (pdf_path.stem + ".md")

    # PDF 열기
    doc = fitz.open(pdf_path)

    all_text_lines = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        # 페이지에서 텍스트 추출 (레이아웃 고려)
        text = page.get_text("text")  # "text" or "blocks" 도 가능

        # 페이지 구분선 추가 (원하면)
        all_text_lines.append(f"\n\n--- 페이지 {page_num + 1} ---\n\n")
        all_text_lines.append(text.strip())

    doc.close()

    # Markdown 형식으로 저장 (여기서는 단순히 텍스트만 저장)
    md_content = "\n".join(all_text_lines)

    # 줄 끝 공백 정리
    md_content = "\n".join(line.rstrip() for line in md_content.splitlines())

    output_dir.mkdir(parents=True, exist_ok=True)
    md_path.write_text(md_content, encoding="utf-8")
    print(f"변환 완료: {md_path}")


def _stem_has_valid_yyyymmdd(stem: str) -> bool:
    m = re.search(r"(?<!\d)(\d{8})(?!\d)", stem)
    if not m:
        return False
    date_token = m.group(1)
    try:
        datetime.strptime(date_token, "%Y%m%d")
        return True
    except ValueError:
        return False


def convert_folder(input_dir: str, output_dir: str):
    in_dir = Path(input_dir)
    out_dir = Path(output_dir)

    if not in_dir.exists():
        raise FileNotFoundError(f"입력 폴더를 찾을 수 없습니다: {in_dir}")

    out_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(in_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"처리할 PDF가 없습니다: {in_dir}")
        return 0, 0, 0

    converted = 0
    skipped = 0
    for pdf_path in pdf_files:
        if _stem_has_valid_yyyymmdd(pdf_path.stem):
            pdf_to_markdown(str(pdf_path), out_dir)
            converted += 1
        else:
            print(f"건너뜀(날짜 형식 미포함): {pdf_path.name}")
            skipped += 1

    return converted, skipped, len(pdf_files)


def _ask_directory(title: str, must_exist: bool = True) -> str:
    if tk is None or filedialog is None:
        raise RuntimeError("GUI 대화상자를 열 수 없습니다. tkinter가 설치되어 있는지 확인하세요.")
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory(title=title, mustexist=must_exist)
    root.destroy()
    return path or ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="폴더 내 PDF를 Markdown으로 변환(YYYYMMDD 포함 파일만)")
    parser.add_argument("--input-dir", required=False, help="입력 PDF 폴더 경로(미지정 시 대화상자 표시)")
    parser.add_argument("--output-dir", required=False, help="생성된 .md 저장 폴더 경로(미지정 시 대화상자 표시)")
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    if not input_dir:
        try:
            input_dir = _ask_directory("1) PDF 파일이 들어있는 폴더를 선택하세요")
        except RuntimeError as e:
            print(e)
            sys.exit(1)
        if not input_dir:
            print("입력 폴더 선택이 취소되었습니다.")
            sys.exit(0)

    if not output_dir:
        try:
            output_dir = _ask_directory("2) 변환된 Markdown(.md)을 저장할 폴더를 선택하세요", must_exist=False)
        except RuntimeError as e:
            print(e)
            sys.exit(1)
        if not output_dir:
            print("출력 폴더 선택이 취소되었습니다.")
            sys.exit(0)

    conv, skip, total = convert_folder(input_dir, output_dir)

    summary = (
        f"처리 완료\n\n"
        f"- 총 파일: {total}\n"
        f"- 변환됨: {conv}\n"
        f"- 건너뜀: {skip}\n\n"
        f"저장 위치: {output_dir}"
    )
    print(summary)

    # GUI 알림 팝업 (가능한 경우)
    if messagebox is not None:
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo("PDF → Markdown 변환", summary)
            root.destroy()
        except Exception:
            pass
