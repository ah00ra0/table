ERROR: Can not perform a '--user' install. User site-packages are not visible in this virtualenv.



https://github.com/kanishksh4rma/Brain_Tumour_detection_using_MRI_Scans/blob/main/Brain_Tumour_Detection_using_MRI_scans.ipynb

https://github.com/Armin-Abdollahi/Brain-Tumor-Diagnosis/blob/main/Brain_Tumor_Diagnosis.ipynb

https://github.com/Armin-Abdollahi/Brain-Tumor-Diagnosis/blob/main/Brain_Tumor_Diagnosis.ipynb

https://github.com/sanidhyy/apple-clone
https://github.com/junhoyeo/iphone
https://github.com/omunite215/Project_3DPortfolio

apple
 # 👇️ if you use npm
npm install
npm install vite
1
npm run dev

# 👇️ if you use yarn
yarn install
yarn add vite

yarn dev
#******! 
[Setup]
AppName=برنامه من
AppVersion=1.0
DefaultDirName={pf}\برنامه من
DefaultGroupName=برنامه من
DisableProgramGroupPage=yes
LicenseFile=C:\MySource\license.txt
OutputDir=C:\MySource
OutputBaseFilename=Setup_Barnamé_Man
Compression=lzma
SolidCompression=yes
WizardStyle=modern
Uninstallable=no

[Files]
Source: "C:\MySource\myfile.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\برنامه من"; Filename: "{app}\myfile.txt"

[Run]

[Code]
procedure InitializeWizard;
begin
  WizardForm.WelcomeLabel1.Caption := 'به نصب‌کننده برنامه من خوش آمدید';
  WizardForm.WelcomeLabel2.Caption := 'این مراحل به شما کمک می‌کند تا فایل را در محل دلخواه کپی کنید.';
end;


test2
TEST3
test
IN BRAY TEXT TESST AST
<meta property="og:image" content="https://yourgithubrepo.com/path/to/image.jpg">

sudo apt update
sudo apt install -y python3 python3-pip git zip unzip openjdk-17-jdk \
build-essential ccache libffi-dev libssl-dev


pip3 install --user buildozer
export PATH=$PATH:~/.local/bin

mkdir hi_app
cd hi_app

from kivy.app import App
from kivy.uix.label import Label

class HiApp(App):
    def build(self):
        return Label(text='hi', font_size=50)

if __name__ == '__main__':
    HiApp().run()

buildozer init


title = Hi App
package.name = hiapp
package.domain = org.example


buildozer -v android debug

bin/hiapp-debug.apk

Command 'pyhton3.11' not found, did you mean:
  command 'python3.11' from deb python3.11 (3.11.7-2)
Try: sudo apt install <deb name>
#ششنشنت

(venv) ahoora@ahoora001:~/Desktop/a/venv/bin$ buildozer -v android debug
# Check configuration tokens
# Ensure build layout
# Check configuration tokens
# Preparing build
# Check requirements for android
# Search for Git (git)
#  -> found at /usr/bin/git
# Search for Cython (cython)
# Search for Java compiler (javac)
#  -> found at /usr/lib/jvm/java-17-openjdk-amd64/bin/javac
# Search for Java keytool (keytool)
#  -> found at /usr/lib/jvm/java-17-openjdk-amd64/bin/keytool
# Install platform
# Run ['git', 'clone', '-b', 'master', '--single-branch', 'https://github.com/kivy/python-for-android.git', 'python-for-android']
# Cwd /home/ahoora/Desktop/a/venv/bin/.buildozer/android/platform
Cloning into 'python-for-android'...
# Run ['/home/ahoora/Desktop/a/venv/bin/python3.11', '-m', 'pip', 'install', '-q', 'appdirs', 'colorama>=0.3.3', 'jinja2', 'sh>=1.10, <2.0; sys_platform!="win32"', 'build', 'toml', 'packaging', 'setuptools']
# Cwd None

[notice] A new release of pip is available: 24.0 -> 25.3
[notice] To update, run: pip install --upgrade pip
# Android ANT is missing, downloading
# Downloading https://archive.apache.org/dist/ant/binaries/apache-ant-1.9.4-bin.tar.gz
# Run ['tar', 'xzf', 'apache-ant-1.9.4-bin.tar.gz']
# Cwd /home/ahoora/.buildozer/android/platform/apache-ant-1.9.4
# Apache ANT installation done.
# Android SDK is missing, downloading
# Downloading https://dl.google.com/android/repository/commandlinetools-linux-6514223_latest.zip
Traceback (most recent call last):
  File "/home/ahoora/Desktop/a/venv/bin/buildozer", line 8, in <module>
    sys.exit(main())
             ^^^^^^
  File "/home/ahoora/Desktop/a/venv/lib/python3.11/site-packages/buildozer/scripts/client.py", line 13, in main
    Buildozer().run_command(sys.argv[1:])
  File "/home/ahoora/Desktop/a/venv/lib/python3.11/site-packages/buildozer/__init__.py", line 1024, in run_command
    self.target.run_commands(args)
  File "/home/ahoora/Desktop/a/venv/lib/python3.11/site-packages/buildozer/target.py", line 93, in run_commands
    func(args)
  File "/home/ahoora/Desktop/a/venv/lib/python3.11/site-packages/buildozer/target.py", line 103, in cmd_debug
    self.buildozer.prepare_for_build()
  File "/home/ahoora/Desktop/a/venv/lib/python3.11/site-packages/buildozer/__init__.py", line 172, in prepare_for_build
    self.target.install_platform()
  File "/home/ahoora/Desktop/a/venv/lib/python3.11/site-packages/buildozer/targets/android.py", line 614, in install_platform
    self._install_android_sdk()
  File "/home/ahoora/Desktop/a/venv/lib/python3.11/site-packages/buildozer/targets/android.py", line 376, in _install_android_sdk
    self.buildozer.download(url,
  File "/home/ahoora/Desktop/a/venv/lib/python3.11/site-packages/buildozer/__init__.py", line 658, in download
    urlretrieve(url, filename, report_hook)
  File "/usr/local/lib/python3.11/urllib/request.py", line 1848, in retrieve
    block = fp.read(bs)
            ^^^^^^^^^^^
  File "/usr/local/lib/python3.11/tempfile.py", line 500, in func_wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
ValueError: read of closed file

