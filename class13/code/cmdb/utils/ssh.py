#encoding: utf-8
import paramiko
import traceback

def exec_cmds(host,port,username,password,cmds=[]):
    client = paramiko.SSHClient()
    rt_list = []
    try:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host,port,username,password)

        for cmd in cmds:
            stdin,stdout,stderr = client.exec_command(cmd)
            output = stdout.readlines()
            error = stderr.readlines()
            rt_list.append([cmd,output,error])
    except paramiko.AuthenticationException  as e:
        print u'用户名秘密错误'
        print e
    except  BaseException as e:
        print u'未知错误'
        print e

    client.close()
    return rt_list

def upload_files(host,port,username,password,file=[]):
    t = paramiko.Transport((host,port))
    rt_list = []
    try:
        t.connect(username=username,password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        for local,remote in files:
            sftp.put(local,remote)
            rt_list.append([local,remote])
    except paramiko.AuthenticationException as e:
        print u'用户名密码错误'
        print e
    except BaseException as e:
        print e
        print traceback.format_exc()
    t.close()
    return rt_list

if __name__ =='__main__':
    files = [('/data/reboot/class12/code/agent/agent.py','/jiaoben/agent.py')]
    print upload_files('60.205.136.199',22,'root','lirui@123',files)
    cmds = ["ps aux | grep python | grep agent.py | grep -v grep | awk '{print $2}' | xargs kill -9",
            'nohup python /jiaoben/agent.py 59.110.20.187 5000 > /dev/null 2>&1 &'
              ]
    print exec_cmds('60.205.136.199',22,'root','lirui@123',cmds)


