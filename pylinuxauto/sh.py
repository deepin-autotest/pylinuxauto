import os
import re
import subprocess
import sys
from funnylog2 import logger

import pylinuxauto


class ShellExecutionFailed(Exception):

    def __init__(self, msg):
        err = f"Shell执行失败: {msg}"
        logger.error(err)
        Exception.__init__(self, err)


def _run(command, _input=None, timeout=None, check=False, executable=None, **kwargs):
    with subprocess.Popen(command, **kwargs) as process:
        try:
            stdout, stderr = process.communicate(_input, timeout=timeout)
        except:
            process.kill()
            raise
        retcode = process.poll()
        if check and retcode:
            raise subprocess.CalledProcessError(
                retcode, process.args, output=stdout, stderr=stderr
            )
    return subprocess.CompletedProcess(process.args, retcode, stdout, stderr)


def _getstatusoutput(command, timeout, executable):
    kwargs = {
        "shell": True,
        "stderr": subprocess.STDOUT,
        "stdout": subprocess.PIPE,
        "timeout": timeout,
        "executable": executable,
    }
    try:
        if sys.version_info >= (3, 7):
            kwargs["text"] = True
        result = _run(command, **kwargs)
        data = result.stdout
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        exitcode = result.returncode
    except subprocess.CalledProcessError as ex:
        data = ex.output
        exitcode = ex.returncode
    except subprocess.TimeoutExpired as ex:
        data = ex.__str__()
        exitcode = -1
    if data[-1:] == "\n":
        data = data[:-1]
    return exitcode, data


def run(
        command: str,
        interrupt: bool = False,
        timeout: [None, int] = 25,
        print_log: bool = True,
        command_log: bool = True,
        return_code: bool = False,
        executable: str = "/bin/bash",
):
    """
     执行shell命令
    :param command: shell 命令
    :param interrupt: 命令异常时是否中断
    :param timeout: 命令执行超时
    :param out_debug_flag: 命令返回信息输出日志
    :param command_log: 执行的命令字符串日志
    :return: 返回终端输出
    """
    exitcode, stdout = _getstatusoutput(command, timeout=timeout, executable=executable)
    if command_log:
        logger.debug(command)
    if exitcode != 0 and interrupt:
        raise ShellExecutionFailed(stdout)
    if print_log and stdout:
        logger.debug(stdout)
    if return_code:
        return stdout, exitcode
    return stdout


def sudo_run(
        command,
        password: str = None,
        workdir: str = None,
        interrupt: bool = False,
        timeout: int = 25,
        print_log: bool = True,
        command_log: bool = True,
        return_code: bool = False
):
    if password is None:
        password = "1"
    wd = ""
    if workdir:
        if not os.path.exists(workdir):
            raise FileNotFoundError
        wd = f"cd {workdir} && "
    res = run(
        f"{wd}echo '{password}' | sudo -S {command}",
        interrupt=interrupt,
        timeout=timeout,
        print_log=print_log,
        command_log=command_log,
        return_code=return_code
    )
    if return_code is False:
        return res.lstrip("请输入密码●")
    else:
        res = list(res)
        res[0] = res[0].lstrip("请输入密码●")
        return res


def copy(source, dest):
    return run(f"cp -rf {source} {dest}")


def apt_policy(package_name):
    ret = run(f"apt policy {package_name}")
    ret = re.search("已安装：(.*)", ret).group(1)
    return ret


def move(source, dest):
    return run(f"move -rf {source} {dest}")
