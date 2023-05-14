wget https://raw.githubusercontent.com/ilovapples/terminal/main/src/apyterm_ilovapples/cmds.yaml
touch .users.txt
echo 'default' > dir.txt
echo 'echo $(pwd) > dir.txt' > set_dir.sh
echo 'echo %cd% > dir.txt' > set_dir.bat
echo -e '#!/usr/bin/env bash\nrm -r data/*\ntouch data/placeholder.txt\necho '\"'\" > .users.txt\necho '\"default'\" > dir.txt' > reset.sh
echoe -e 'rmdir data /S /Q\nmd data\ntype nul > data/placeholder.txt\ntype nul > .users.txt\ntype '\"default'\" > dir.txt' > reset.bat
[ -d data ] || mkdir data
touch data/placeholder.txt
wget https://raw.githubusercontent.com/ilovapples/terminal/main/README.md
[ -d default_data ] || mkdir default_data
echo 'clear' > default_data/.startup
cp README.md default_data/README.md