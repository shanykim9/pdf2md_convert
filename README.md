# pdf2md

윈도우에서 폴더를 선택해 PDF를 일괄로 Markdown(.md)으로 변환하는 간단한 도구입니다. 파일명에 유효한 날짜(YYYYMMDD, 예: 20251113)가 포함된 PDF만 변환하며, 변환이 끝나면 팝업으로 통계를 알려줍니다.

## 주요 기능
- 입력/출력 폴더를 GUI 대화상자( tkinter )로 선택
- 파일명에 유효한 8자리 날짜(YYYYMMDD)가 포함된 PDF만 변환
- 변환 결과는 사용자가 지정한 출력 폴더에 저장(폴더 없으면 자동 생성)
- 변환 완료 후 요약 팝업 및 콘솔 로그 출력(총 파일/변환/건너뜀/저장 위치)
- PyMuPDF로 페이지 텍스트 추출, 페이지 구분선 삽입

## 요구 사항
- Windows 11 + Python 3.10 ~ 3.12 (64-bit 권장)
- 패키지:
  - PyMuPDF (필수)
  - PyInstaller (실행파일 생성 시)
  - tkinter는 보통 Windows용 Python에 기본 포함

## 설치
```powershell
cd "C:\Users\shany\OneDrive\바탕 화면\pdf2md"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install PyMuPDF
```

## 사용법
### 1) GUI로 간단 실행
그냥 실행하면 폴더 선택 창이 2번 나타납니다.
```powershell
python ".\pdf2md.py"
```
순서
1. PDF 파일이 들어있는 폴더 선택
2. 변환된 Markdown(.md)을 저장할 폴더 선택
3. 자동 변환 → 완료 팝업 표시

### 2) CLI 인자로 실행(자동화에 유용)
```powershell
python ".\pdf2md.py" --input-dir "C:\path\to\pdfs" --output-dir "C:\path\to\markdowns"
```

## 변환 규칙
- 입력 폴더의 최상위 `*.pdf`만 처리(하위 폴더는 기본 미포함)
- 파일명 어딘가에 8자리 숫자(예: 20251113)가 있고 실제 유효한 날짜여야 변환
- 출력 파일명은 원본 이름과 동일한 `.md` 확장자로 저장
- 기존 동일 이름의 `.md`가 있으면 덮어쓰기

## 실행파일(.exe) 만들기
필요 패키지 설치 후 PyInstaller로 빌드합니다.
```powershell
pip install pyinstaller

# 콘솔창 없이 GUI 전용
pyinstaller --onefile --noconsole ^
  --hidden-import=tkinter ^
  --hidden-import=tkinter.filedialog ^
  --hidden-import=fitz ^
  -n pdf2md pdf2md.py
```
결과물: `dist\pdf2md.exe`  
원하면 바탕화면으로 복사:
```powershell
Copy-Item ".\dist\pdf2md.exe" "$env:USERPROFILE\OneDrive\바탕 화면\"
```

> PowerShell 여러 줄 기호는 백틱(`)을, CMD는 캐럿(^)을 사용합니다. 위 예시는 CMD 기준(^). PowerShell 한 줄 버전은 아래와 같습니다.
```powershell
pyinstaller --onefile --noconsole --hidden-import=tkinter --hidden-import=tkinter.filedialog --hidden-import=fitz -n pdf2md pdf2md.py
```

## 흔한 문제 해결
- `fatal: not a git repository` → `git init`로 저장소 초기화 후 커밋/푸시
- `git add.` 오류 → `git add .`처럼 `add`와 `.` 사이에 공백 필요
- `tkinter` 관련 오류 → Windows용 공식 Python 재설치(대부분 기본 포함)
- 폴더 경로에 공백/한글 → 명령어에서 경로는 반드시 따옴표로 감싸기

## 프로젝트 구조(간단)
```
pdf2md/
├─ pdf2md.py        # 메인 스크립트 (GUI 폴더 선택 + 배치 변환 + 팝업)
└─ README.md
```

## 라이선스
프로젝트 사용 조건을 정하고 싶다면 `LICENSE` 파일을 추가하세요. 기본적으로는 별도 라이선스를 포함하지 않습니다.


