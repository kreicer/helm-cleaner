# Helm Cleaner
Python script for cleaning helm from old releases.  
It may be useful in develop environment.  

# Usage
```
$ python /path/to/script/helm-cleaner.py --days {number} --hostname {tiller host} --purge
```
**--days {number}** - number of days since last releas was deploy to clean, default "7"  
**--hostname {tiller host}** - tiller hostname or IP, default "127.0.0.1"  
**--purge** - flag to purge releases, default "False"  

# Requirements
See requirements in requirements.txt.  
Use pip to install all packages.  
```
$ pip install -r requirements.txt
```

# Cron example
```
0 0 */1 * * tiller_host=$(kubectl get ep -n kube-system | grep tiller-deploy | awk '{print $2}' | awk -F":" '{print $1}'); python ./helm-cleaner.py --hostname $tiller_host --purge >> helm-cleaner.log
```
0 0 */1 * * - run everyday  
**kubectl get ep -n kube-system** - get all endpoints in kube-system namespace  
**grep tiller-deploy** - get line with tiller endpoint  
**awk '{print $2}'** - get only 2nd column (ip address and port here)  
**awk -F":" '{print $1}')** - get only ip  
**python /root/helm-cleaner.py --hostname $tiller_host --purge** - run helm-cleaner  
**>> helm-cleaner.log** - redirect output into log file  

# Compatibility
Tested with:
- Helm 2.14.1

Will not work with:
- Helm 3+
