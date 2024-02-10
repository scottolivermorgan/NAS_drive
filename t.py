
import subprocess
import os
UN = input("Enter current user name? ")
#env={'UN': UN}
var = os.environ["UN"] = UN
#print('env', env)
subprocess.Popen(["sh", "t.sh"])