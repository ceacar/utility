#!/usr/bin/env python
cmd_list="""
docker exec -it acdf2917185b bash
git st
git fetch
cd pyapi-ws
ls
clear
ls
git df
git log |head
clear
git branch
refreshbashrc
refreshbashrc
git pull
git st
git pull
cl src
cd queue
ls
grep -r '>>>>>' deployment_test docker run src utils venv
ls
cl pragma/
aws s3 ls s3://fbd-data/live/
aws s3 ls s3://fbd-dev/
aws s3 ls s3://fbddev-dev/
aws s3 ls s3://twxm-cache/
aws s3 ls s3://fbddev-dev/taq/daily
aws s3 ls s3://fbd-data/taq/daily
aws s3 cp s3://fbd-dev/raw_taq/20180202/SPLITS_US_ALL_BBO_B_20180202.gz - |zcat| grep "|BXE|" |head
clear
ls
ls
git status
git branh
aws s3 ls s3://fbd-data/raw/20180614/csi/
git st
aws s3 ls s3://fbd-data/bats/20180518/
ls
clear
ls -al
history
git df
clear
cd fbd
cd scratch
cd ./home
ls
ls
clear
`1
`2
`3
`4
`5
`6
`7
`8
`9
cd venvmgr/
refreshbashrc
ls
git log |head
ls
aws s3 ls s3://fbd-data/equities/
refreshbashrc
cl /scratch/xiazi/taq/taq_output/temp3/fbd
cd repos
cd pyapi
git diff fbd
conda deactivate
cd venvmgr/
ls
it status
ls
cd fbd_tools/
ls
cd pyapi-ws
ls
git st
clear
aws s3 ls s3://fbd-data/taq/daily/
git df
ls
ls
cl venvmgr_server/
start_midasgui
clear
ls
clear
cl src
sl
clear
cd pyapi
clear
ls
git log |head
docker cp 3457e44bf10f@/home/user1/* ./
docker cp 3457e44bf10f@/home/user1/* ./
git st
clear
conda deactivate
ls
docker cp ./venvmgr_server ./venvmgr_ui 1981e74d41be:/opt/venvmgr/
ls
ls venvmgr_server/
git fetch
ls
git st
ls
ls
git stash
git st
cl src
ls
ls
git stash
git st
docker cp 3457e44bf10f@/home/user1/* ./
ls
ls
ls
clear
git st
git log |head
ls
cl utils/
git st
grep TWXMLIVE ./
cl pragma/
git st
cd pyapi
clear
ls
git pull origin master
cl docker/
grep -r '>>>>>' deployment_test docker run src utils venv
git st
cl conf-jupyterlab/
clear
pip install requests
ls
cl ..
cl 2017
ls
git log |head
clear
aws s3 ls s3://fbd-data/
cd repos
echo $PYAPIWS_PORT
git pull
aws s3 ls s3://fbd-data/live/
ls
ls -al
cl venvmgr_server/
ls
git st
aws s3 ls s3://fbd-data/
ls
git log |head
ls
cl work/
git diff fbd
grep tmux TODO.txt backup bak.log bash bash.notes bats_december_missing_tickers.txt binary_git_log camilo_magic cpp.notes ctrlp.manual data_formats_for_clients.txt
ls
ls
ls
ls
ls
docker cp 3457e44bf10f@/home/user1/* ./
aws s3 ls s3://fbd-data/raw/20180614/csi/
git pull
ls
ls -al
it status
cl venvmgr_server/
ls
git st
ls
cl 2017
sl
ls
ls
cat /etc/hosts
cd pyapi
ls
ls
cd pyapi-ws
ls
grep -r "subprocess" __init__.py authapp compose-all config.midas.env config.prod.env config.qa.env configuration connectors consul datastore deployment_test domock elasticsearch
cl jupyterlab
aws s3 ls s3://fbd-data/
git log |head
ls
ls
git st
ls
cd pyapi-ws
ls
git branch
grep -r '>>>>>' deployment_test docker run src utils venv
source /scratch/xiazi/taq/taq_output/venv_temp/bin/activate
ls
clear
cd docker/
ls
ls
ls -al ~
ls -alh /scratch
git pull
ls
git log |head
ls
ls
ls
git log |head
rundocker ./compose.dtest.pyapi.yml
ls
cl src
ls
ls
ls
cl poyapi
cl pyapi
ls
find . |grep pycache
cl src/tests/deployment_test/
ls
cl test
ls
cl test_script/
ls
ls
clear
ls
git log |head
git st
ls
git st
find . -name *.pyc
git df
clear
ls
cl pyapi
ls
cl utils/
ls
ls
cl docker/
cl conf-pyapi/
docker-build
cat /scratch/xiazi/taq/taq_output/fbd/twxm-live/misc_utility/debugging_cmd
cat /scratch/xiazi/taq/taq_output/fbd/twxm-live/misc_utility/hw.sh
cat /scratch/xiazi/taq/taq_output/fbd/twxm-live/misc_utility/curl_script
cat /scratch/xiazi/taq/taq_output/fbd/twxm-live/misc_utility/sample_curl
cat /scratch/xiazi/taq/taq_output/fbd/connectors
cat /scratch/xiazi/taq/taq_output/fbd/connectors/.pytest_cache
cat /scratch/xiazi/taq/taq_output/fbd/connectors/.pytest_cache/v
cat /scratch/xiazi/taq/taq_output/fbd/connectors/.pytest_cache/v/cache
cat /scratch/xiazi/taq/taq_output/fbd/connectors/.pytest_cache/v/cache/lastfailed
cat /scratch/xiazi/taq/taq_output/fbd/connectors/python
cat /scratch/xiazi/taq/taq_output/fbd/connectors/python/utest
cat /scratch/xiazi/taq/taq_output/fbd/connectors/python/adz
cat /scratch/xiazi/taq/taq_output/fbd/connectors/python/adz/__init__.py
cat /scratch/xiazi/taq/taq_output/fbd/connectors/python/adz/credentials.py
cat /scratch/xiazi/taq/taq_output/fbd/connectors/python/adz/.coverage
cat /scratch/xiazi/taq/taq_output/fbd/connectors/python/adz/health.py
cat /scratch/xiazi/taq/taq_output/fbd/twx_core/setup.py
cat /scratch/xiazi/taq/taq_output/fbd/twx_core/MANIFEST.in
cat /scratch/xiazi/taq/taq_output/fbd/jupyterlab
cat /scratch/xiazi/taq/taq_output/fbd/jupyterlab/jupyterhub_config.py
cat /scratch/xiazi/taq/taq_output/fbd/connectors/setup.py
cat /scratch/xiazi/taq/taq_output/fbd/.docker_registry
cat /scratch/xiazi/taq/taq_output/fbd/.run_sanity_test
cat /scratch/xiazi/taq/taq_output/fbd/queue
cat /scratch/xiazi/taq/taq_output/fbd/queue/src
cat /scratch/xiazi/taq/taq_output/fbd/queue/src/lint
cat /scratch/xiazi/taq/taq_output/fbd/queue/src/broker
cat /scratch/xiazi/taq/taq_output/fbd/queue/src/broker/ob.py
cat /scratch/xiazi/taq/taq_output/fbd/queue/src/broker/__init__.py
aws s3 cp s3://fbd-dev/taq/daily/20180205/exchange/trades_exchange.gz - | zcat |awk '$6=="S"'| gzip >./S.gz
aws s3 cp s3://fbd-dev/taq/daily/20180205/exchange/trades_exchange.gz - | zcat |awk '$6=="C"'| gzip >./S.gz
cd pyapi-ws
ls
ls
ls
clear
ls
ls
cl twx_core/
ls
git pull
clear
git df
ls
aws s3 ls s3://fbd-data/
cl ..
ls
grep envmgr *|grep update
git push origin master
ls
ls
git push origin 26-venvmgr-uses-anaconda
cl xiazi
git st
ls
ls
clear
aws s3 cp s3://fbd-data/bats/20180521/interqueue_20180521.gz - | zcat |head
refreshbashrc
cl twx_core/
git branch
ls
ls
git pull
ls
la
ls
ls
git cherry-pick a1c547bd4d068c51eeaa75040f79d44f3fa4475a b86e071cf5e1cd6a62516e6368ec8f8f4e2c9b45
conda deactivate
conda deactivate
clear
ls
grep envmgr *|grep update
ls
zcat 20180430.csv.gz
ls -al
cl ldap
ls
py.test ./tests.py -v
cd jupyterlab
ls
ls
ls -al
cl jupyterlab
ls
refreshbashrc
git status
aws s3 ls s3://fbd-data/raw/20180614/csi/
git status
ls
ls
ls
git checkout 72-venvmgr-integration-into-jupyterlab
aws s3 ls --human-readable s3://twxm-cache/taq/daily/20180202/quotes/
"""


import subprocess
import os
#git st
#git fetch
import sys
import time
import random
cmd_array = cmd_list.split('\n')
length = len(cmd_array)
selected_index = random.randint(1,length)
#def convert_cmd_to_xdotool_cmd(cmd_input):
#    splitted = cmd_input.split()
#    cmd_final = ""
#    for cmd in splitted:
#        cmd_final = cmd_final + ' '.join(cmd) + ' KP_Space '
#    cmd_final = cmd_final + 'KP_Enter'
#    return cmd_final
#selected_cmd = convert_cmd_to_xdotool_cmd(cmd_array[selected_index])
selected_cmd = cmd_array[selected_index] + '\n'
print(selected_cmd)
time.sleep(0.1)
