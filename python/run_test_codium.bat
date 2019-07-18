::set dev_path=%dp0%..\
set dev_path=C:\Users\Albert\Desktop\GitHub\Industrial-Robots-VSCode\

echo %dev_path%

cd "C:\Users\Albert\Desktop\RoboDK\Deploy\RoboDK_MSVC2017_Qt5.11.2x64\Other\VSCodium\"

VSCodium --disable-extensions --extensionDevelopmentPath=%dev_path%


