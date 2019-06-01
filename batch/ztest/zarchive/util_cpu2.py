# -*- coding: utf-8 -*-
# pylint: disable=C0103,W0601,E1123,W0614,F0401,E1120,E1101,E0611,W0702

import argparse
import arrow
import copy
import csv
# stdlib imports
import logging
import os
import platform
import random
import shlex
import subprocess
import sys
import time
from collections import namedtuple
from datetime import datetime
from time import sleep, time

# non-stdlib imports
import psutil
# noinspection PyUnresolvedReferences
import util_log

"""
Launch processors and monitor the CPU, memory usage.
Maintain same leve of processors over time.

"""
VERSION = "0.0.1.1"


############# Root folder #####################################################
def os_getparent(dir0):
    return os.path.abspath(os.path.join(dir0, os.pardir))


DIRCWD = os_getparent(os.path.dirname(os.path.abspath(__file__)))

# os.chdir(DIRCWD)
# sys.path.append(DIRCWD + '/aapackage')
# print('Root Folder', DIRCWD)
# import util


###############################################################################
#############Variable #########################################################
APP_ID = __file__ + ',' + str(os.getpid()) + '_' + str(random.randrange(10000))
logfolder = '_'.join(
    [arg.logfolder, arg.name, arg.consumergroup, arg.input_topic,
     arrow.utcnow().to('Japan').format("YYYYMMDD_HHmm_ss"),
     str(random.randrange(1000))])
util.os_folder_create(logfolder)
LOGFILE = logfolder + '/stream_monitor_cli.txt'
Mb = 1024 * 1024


############# Arg parsing #####################################################
def load_arguments():
    try:
        ppa = argparse.ArgumentParser()
        ppa.add_argument("--DIRCWD", type=str, default="", help=" Root Folder")
        ppa.add_argument("--do", type=str, default="zdoc", help="action")
        ppa.add_argument("--verbose", type=int, default=0, help=" Verbose mode")
        ppa.add_argument("--test", type=int, default=0, help=" ")
        ppa.add_argument(
            "--configfile", type=str, default="/config/config.txt", help=" config file"
        )
        arg = ppa.parse_args()
        if arg.DIRCWD != "":
            DIRCWD = arg.DIRCWD

    except Exception as e:
        print(e)
        sys.exit(1)
    return arg


###############################################################################
######### Logging #############################################################
def log(s="", s1="", s2="", s3="", s4="", s5="", s6="", s7="", s8="", s9="", s10=""):
    try:
        prefix = (
            util_log.APP_ID
            + ","
            + arrow.utcnow().to("Japan").format("YYYYMMDD_HHmmss,")
        )
        s = ",".join(
            [
                prefix,
                str(s),
                str(s1),
                str(s2),
                str(s3),
                str(s4),
                str(s5),
                str(s6),
                str(s7),
                str(s8),
                str(s9),
                str(s10),
            ]
        )

        logging.info(s)

    except Exception as e:
        logging.info(str(e))


###############################################################################


def ps_get_cpu_percent(process):
    try:
        return process.cpu_percent()
    except AttributeError:
        return process.get_cpu_percent()


def ps_get_memory_percent(process):
    try:
        return process.memory_info()
    except AttributeError:
        return process.get_memory_info()


def ps_all_children(pr):
    processes = []
    children = []
    try:
        children = pr.children()
    except AttributeError:
        children = pr.get_children()
    except Exception:  # pragma: no cover
        pass

    for child in children:
        processes.append(child)
        processes += ps_all_children(child)
    return processes


def ps_get_process_status(pr):
    try:
        pr_status = pr.status()
    except TypeError:  # psutil < 2.0
        pr_status = pr.status
    except psutil.NoSuchProcess:  # pragma: no cover
        raise psutil.NoSuchProcess
    return pr_status


def ps_get_computer_resources_usage():
    cpu_used_percent = psutil.cpu_percent()

    mem_info = dict(psutil.virtual_memory()._asdict())
    mem_used_percent = 100 - mem_info["available"] / mem_info["total"]

    return cpu_used_percent, mem_used_percent


###############################################################################
########### Utilities #########################################################
def ps_find_procs_by_name(name, ishow=1, cmdline=None):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(attrs=["pid", "name", "exe", "cmdline"]):
        if name.lower() in p.info["name"].lower():
            if cmdline:
                if cmdline.lower() in " ".join(p.info["cmdline"]).lower():
                    ls.append(copy.deepcopy(p))
            else:
                ls.append(copy.deepcopy(p))

            if ishow == 1:
                util_log.printlog(p.pid, " ".join(p.info["cmdline"]))
    return ls


def launch(commands):
    processes = []
    for cmd in commands:
        try:
            p = subprocess.Popen(cmd, shell=False)
            processes.append(p.pid)
            log("Launched: ", p.pid, " ".join(cmd))
            sleep(1)

        except Exception as e:
            log(str(e))
    return processes


def terminate(processes):
    for p in processes:
        pidi = p.pid
        try:
            os.kill(p.pid, 9)
            log("killed ", pidi)
        except Exception as e:
            log(str(e))
            try:
                os.kill(pidi, 9)
                log("killed ", pidi)
            except:
                pass


def extract_commands(csv_file, has_header=False):
    with open(csv_file, "r", newline="") as file:
        reader = csv.reader(file, skipinitialspace=True)
        if has_header:
            headers = next(reader)  # pass header
        commands = [row for row in reader]

    return commands


def is_issue(p):
    pdict = p.as_dict()
    pidi = p.pid

    log("Worker PID;CPU;RAM:", pidi, pdict["cpu_percent"], pdict["memory_full_info"][0] / Mb)

    try:
        if not psutil.pid_exists(pidi):
            log("Process has been killed ", pidi)
            return True

        elif pdict["status"] == "zombie":
            log("Process  zombie ", pidi)
            return True

        elif pdict["memory_full_info"][0] >= pars["max_memory"]:
            log("Process  max memory ", pidi)
            return True

        elif pdict["cpu_percent"] >= pars["max_cpu"]:
            log("Process MAX CPU ", pidi)
            return True

        else:
            return False
    except Exception as e:
        log(str(e))
        return True


def ps_net_send(tperiod=5):
    x0 = psutil.net_io_counters(pernic=False).bytes_sent
    t0 = time()
    sleep(tperiod)
    t1 = time()
    x1 = psutil.net_io_counters(pernic=False).bytes_sent
    return (x1 - x0) / (t1 - t0)


def is_issue_system():
    try:
        if psutil.cpu_percent(interval=5) > pars["cpu_usage_total"]:
            return True

        elif psutil.virtual_memory().available < pars["mem_available_total"]:
            return True

        else:
            return False

    except:
        return True


def monitor_maintain():
    """
       Launch processors and monitor the CPU, memory usage.
       Maintain same leve of processors over time.
    """
    log("start monitoring", str(len(CMDS)))
    cmds2 = []
    for cmd in CMDS:
        ss = shlex.split(cmd)
        cmds2.append(ss)

    processes = launch(cmds2)
    try:
        while True:
            has_issue = []
            ok_process = []
            log("N_process", str(len(processes)))

            ### check global system  ##########################################
            if len(processes) == 0 or is_issue_system():
                log("Reset all process")
                lpp = ps_find_procs_by_name(pars["proc_name"], 1)
                terminate(lpp)
                processes = launch(cmds2)
                sleep(5)

            ## pid in process   ###############################################
            for pidi in processes:
                try:
                    p = psutil.Process(pidi)
                    log("Checking", p.pid)

                    if is_issue(p):
                        has_issue.append(p)

                    else:
                        log("Process Fine ", pidi)
                        ok_process.append(p)

                except Exception as e:
                    log(str(e))

            ### Process with issues    ########################################
            for p in has_issue:
                try:
                    log("Relaunching", p.pid)
                    pcmdline = p.cmdline()
                    pidlist = launch([pcmdline])  # New process can start before

                    sleep(3)
                    terminate([p])
                except:
                    pass

            ##### Check the number of  processes    ###########################
            sleep(5)
            lpp = ps_find_procs_by_name(pars["proc_name"], 1)

            log("Active process", str(len(lpp)))
            if len(lpp) < pars["nproc"]:
                for i in range(0, pars["nproc"] - len(lpp)):
                    pidlist = launch([shlex.split(pars["proc_cmd"])])

            else:
                for i in range(0, len(lpp) - pars["nproc"]):
                    pidlist = terminate([lpp[i]])

            sleep(5)
            lpp = ps_find_procs_by_name(pars["proc_name"], 0)
            processes = [x.pid for x in lpp]

            log("Waiting....")
            sleep(arg.nfreq)

    except Exception as e:
        log(str(e))


############ AZURE NODE #################################################################
"""TVM stats"""



# from applicationinsights import TelemetryClient


# _DEFAULT_STATS_UPDATE_INTERVAL = 5


def setup_logger():
    # logger defines
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s.%(msecs)03dZ %(levelname)s %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


# logger = setup_logger()

# global defines
_IS_PLATFORM_WINDOWS = platform.system() == "Windows"

_OS_DISK = None
_USER_DISK = None

if _IS_PLATFORM_WINDOWS:
    _OS_DISK = "C:/"  # This is inverted on Cloud service
    _USER_DISK = "D:/"
else:
    _OS_DISK = "/"
    _USER_DISK = "/mnt/resources"
    if not os.path.exists(_USER_DISK):
        _USER_DISK = "/mnt"


#########################################################################################
#########################################################################################
def python_environment():  # pragma: no cover
    return " ".join([platform.python_implementation(), platform.python_version()])


def os_environment():
    return platform.platform()


def is_windows():
    return _IS_PLATFORM_WINDOWS


def avg(list):
    return sum(list) / float(len(list))


def pretty_nb(num, suffix=""):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1000.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1000.0
    return "%.1f%s%s" % (num, "Yi", suffix)


NodeIOStats = namedtuple("NodeIOStats", ["read_bps", "write_bps"])


class NodeStats:
    """Persistent Task Stats class"""

    def __init__(
        self,
        num_connected_users=0,
        num_pids=0,
        cpu_count=0,
        cpu_percent=None,
        mem_total=0,
        mem_avail=0,
        swap_total=0,
        swap_avail=0,
        disk_io=None,
        disk_usage=None,
        net=None,
    ):
        """
        Map the attributes
        """
        self.num_connected_users = num_connected_users
        self.num_pids = num_pids
        self.cpu_count = cpu_count
        self.cpu_percent = cpu_percent
        self.mem_total = mem_total
        self.mem_avail = mem_avail
        self.swap_total = swap_total
        self.swap_avail = swap_avail
        self.disk_io = disk_io or NodeIOStats(0, 0)
        self.disk_usage = disk_usage or dict()
        self.net = net or NodeIOStats(0, 0)

    @property
    def mem_used(self):
        """
            Return the memory used
        """
        return self.mem_total - self.mem_avail


class IOThroughputAggregator:
    def __init__(self):
        self.last_timestamp = None
        self.last_read = 0
        self.last_write = 0

    def aggregate(self, cur_read, cur_write):
        """
            Aggregate with the new values
        """
        now = datetime.now()
        read_bps = 0
        write_bps = 0
        if self.last_timestamp:
            delta = (now - self.last_timestamp).total_seconds()
            read_bps = (cur_read - self.last_read) / delta
            write_bps = (cur_write - self.last_write) / delta

        self.last_timestamp = now
        self.last_read = cur_read
        self.last_write = cur_write

        return NodeIOStats(read_bps, write_bps)


class NodeStatsCollector:
    """
    Node Stats Manager class
    """

    def __init__(
        self,
        pool_id,
        node_id,
        refresh_interval=_DEFAULT_STATS_UPDATE_INTERVAL,
        app_insights_key=None,
    ):
        self.pool_id = pool_id
        self.node_id = node_id
        self.telemetry_client = None
        self.first_collect = True
        self.refresh_interval = refresh_interval

        self.disk = IOThroughputAggregator()
        self.network = IOThroughputAggregator()

        if (
            app_insights_key
            or "APP_INSIGHTS_INSTRUMENTATION_KEY" in os.environ
            or "APP_INSIGHTS_KEY" in os.environ
        ):
            key = (
                app_insights_key
                or os.environ.get("APP_INSIGHTS_INSTRUMENTATION_KEY")
                or os.environ.get("APP_INSIGHTS_KEY")
            )

            logger.info("Detected instrumentation key. Will upload stats to app insights")
            self.telemetry_client = TelemetryClient(key)
            context = self.telemetry_client.context
            context.application.id = "AzureBatchInsights"
            context.application.ver = VERSION
            context.device.model = "BatchNode"
            context.device.role_name = self.pool_id
            context.device.role_instance = self.node_id
        else:
            logger.info(
                "No instrumentation key detected. Cannot upload to app insights."
                + "Make sure you have the APP_INSIGHTS_INSTRUMENTATION_KEY environment variable setup"
            )

    def init(self):
        """
            Initialize the monitoring
        """
        # start cpu utilization monitoring, first value is ignored
        psutil.cpu_percent(interval=None, percpu=True)

    def _get_network_usage(self):
        netio = psutil.net_io_counters()
        return self.network.aggregate(netio.bytes_recv, netio.bytes_sent)

    def _get_disk_io(self):
        diskio = psutil.disk_io_counters()
        return self.disk.aggregate(diskio.read_bytes, diskio.write_bytes)

    def _get_disk_usage(self):
        disk_usage = dict()
        try:
            disk_usage[_OS_DISK] = psutil.disk_usage(_OS_DISK)
            disk_usage[_USER_DISK] = psutil.disk_usage(_USER_DISK)
        except Exception as e:
            logger.error("Could not retrieve user disk stats for {0}: {1}".format(_USER_DISK, e))
        return disk_usage

    def _sample_stats(self):
        # get system-wide counters
        mem = psutil.virtual_memory()
        disk_stats = self._get_disk_io()
        disk_usage = self._get_disk_usage()
        net_stats = self._get_network_usage()

        swap_total, _, swap_avail, _, _, _ = psutil.swap_memory()

        stats = NodeStats(
            cpu_count=psutil.cpu_count(),
            cpu_percent=psutil.cpu_percent(interval=None, percpu=True),
            num_pids=len(psutil.pids()),
            # Memory
            mem_total=mem.total,
            mem_avail=mem.available,
            swap_total=swap_total,
            swap_avail=swap_avail,
            # Disk IO
            disk_io=disk_stats,
            # Disk usage
            disk_usage=disk_usage,
            # Net transfer
            net=net_stats,
        )
        del mem
        return stats

    def _collect_stats(self):
        """
            Collect the stats and then send to app insights
        """
        # collect stats
        stats = self._sample_stats()

        if self.first_collect:
            self.first_collect = False
            return

        if stats is None:
            logger.error("Could not sample node stats")
            return

        if self.telemetry_client:
            self._send_stats(stats)
        else:
            self._log_stats(stats)

    def _send_stats(self, stats):
        """
            Retrieve the current stats and send to app insights
        """
        process = psutil.Process(os.getpid())

        logger.debug(
            "Uploading stats. Mem of this script: %d vs total: %d",
            process.memory_info().rss,
            stats.mem_avail,
        )
        client = self.telemetry_client

        for cpu_n in range(0, stats.cpu_count):
            client.track_metric("Cpu usage", stats.cpu_percent[cpu_n], properties={"Cpu #": cpu_n})

        for name, disk_usage in stats.disk_usage.items():
            client.track_metric("Disk usage", disk_usage.used, properties={"Disk": name})
            client.track_metric("Disk free", disk_usage.free, properties={"Disk": name})

        client.track_metric("Memory used", stats.mem_used)
        client.track_metric("Memory available", stats.mem_avail)
        client.track_metric("Disk read", stats.disk_io.read_bps)
        client.track_metric("Disk write", stats.disk_io.write_bps)
        client.track_metric("Network read", stats.net.read_bps)
        client.track_metric("Network write", stats.net.write_bps)
        self.telemetry_client.flush()

    def _log_stats(self, stats):
        logger.info("========================= Stats =========================")
        logger.info("Cpu percent:            %d%% %s", avg(stats.cpu_percent), stats.cpu_percent)
        logger.info(
            "Memory used:       %sB / %sB", pretty_nb(stats.mem_used), pretty_nb(stats.mem_total)
        )
        logger.info(
            "Swap used:         %sB / %sB", pretty_nb(stats.swap_avail), pretty_nb(stats.swap_total)
        )
        logger.info("Net read:               %sBs", pretty_nb(stats.net.read_bps))
        logger.info("Net write:              %sBs", pretty_nb(stats.net.write_bps))
        logger.info("Disk read:               %sBs", pretty_nb(stats.disk_io.read_bps))
        logger.info("Disk write:              %sBs", pretty_nb(stats.disk_io.write_bps))
        logger.info("Disk usage:")
        for name, disk_usage in stats.disk_usage.items():
            logger.info(
                "  - %s: %i/%i (%i%%)", name, disk_usage.used, disk_usage.total, disk_usage.percent
            )

        logger.info("-------------------------------------")
        logger.info("")

    def run(self):
        """
            Start collecting information of the system.
        """
        logger.debug("Start collecting stats for pool=%s node=%s", self.pool_id, self.node_id)
        while True:
            self._collect_stats()
            time.sleep(self.refresh_interval)


def main_azure():
    """
    Main entry point for prism
    """
    # log basic info
    logger.info("Python args: %s", sys.argv)
    logger.info("Python interpreter: %s", python_environment())
    logger.info("Operating system: %s", os_environment())
    logger.info("Cpu count: %s", psutil.cpu_count())

    pool_id = os.environ.get("AZ_BATCH_POOL_ID", "_test-pool-1")
    node_id = os.environ.get("AZ_BATCH_NODE_ID", "_test-node-1")

    # get and set event loop mode
    logger.info("enabling event loop debug mode")

    app_insights_key = None
    if len(sys.argv) > 2:
        pool_id = sys.argv[1]
        node_id = sys.argv[2]
    if len(sys.argv) > 3:
        app_insights_key = sys.argv[3]

    # create node stats manager
    collector = NodeStatsCollector(pool_id, node_id, app_insights_key=app_insights_key)
    collector.init()
    collector.run()


def generate_cmdline():
    pars = {
        "max_memory": 1500.0 * Mb,
        "max_cpu": 85.0,
        "proc_name": "streaming_couchbase_update_cli.py",
        "nproc": arg.nproc,
        "proc_cmd": "python kafkastreaming/streaming_couchbase_update_cli.py   --consumergroup {0} --nlogfreq {1}  --logfile {2} --verbose {3}  --input_topic {4}  --test {5}  --mode {6} ".format(
            arg.consumergroup + "couch" + arg.mode,
            arg.nlogfreq,
            logfolder + "/stream_couchbase_" + str(arg.consumergroup) + ".txt",
            arg.verbose,
            arg.input_topic,
            arg.test,
            arg.mode,
        ),
        "mem_available_total": 2000.0 * Mb,
        "cpu_usage_total": 98.0,
    }
    CMDS = [pars["proc_cmd"]] * pars["nproc"]
    return CMDS, pars


if __name__ == "__main__":
    ################## Initialization #########################################
    log(" Initialize workers", arg.name)

    log(arg.name, "parameters", pars)

    CMDS, pars = generate_cmdline()

    ############## RUN Monitor ################################################
    # monitor()
