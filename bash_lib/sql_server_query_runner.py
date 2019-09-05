#!/usr/bin/env python2
import sys
from contextlib import contextmanager
from urlparse import urlparse
from pyodbc import connect
from random import shuffle

from kazoo.client import KazooClient
from luigi.configuration import get_config
from impala.util import as_pandas


__logger = None


class DummyLogger():

    def debug(self, msg):
        print(msg)

    def info(self, msg):
        print(msg)


def getlogger():
    global __logger
    if not __logger:
        __logger = DummyLogger()

    return __logger


@contextmanager
def dbclient(connect_string):
    """Provides db cursor using pyodbc."""

    conn = connect(connect_string)
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.close()


def thisdc():
    """
    :rtype: str
    """
    config = get_config()
    try:
        return config.get("core", "currentdc").strip()
    except Exception:
        getlogger().error("Not sure what DC we're in. Missing luigi config section 'core', returning default")
        return 'lga'


def whichdc(url, defaultdc=None):
    """
    This method takes a URL which points to somewhere in a given datacenter. This can be an http url, hdfs url,
    thrift uri, etc. It will use urlparse to find the hostname, and then return the datacenter referenced by that
    hostname. This could be improved by doing such things as DNS lookups with IP table maps, etc, but for now we
    don't need anything so complex.
    :param url:
    :return:
    """
    data = urlparse(url)
    host = data[1]
    datacenters = ['lga', 'sjc', 'ams']
    for dc in datacenters:
        if dc in host:
            return dc
    if defaultdc:
        return defaultdc
    raise Exception('Unable to determine datacenter for host {0}'.format(host))


def remotedc():
    """
    This is used by distcp tasks to pull data from the "other" dc.
    We may need to rethink this if we ever run with more than two hadoop clusters...
    """
    remote_dcs = {
        'sjc': 'lga',
        'lga': 'sjc',
    }
    return remote_dcs.get(thisdc(), 'lga')


def jdbc_connect(datacenter, database):
    data = db_connections[datacenter]
    instance = ";instanceName={0}".format(data["instancename"]) if data.get("instancename", None) else ""
    return "jdbc:sqlserver://{db_server}{instance};portNumber={port};database={database};".format(
        db_server=data['server'],
        instance=instance,
        port=data['port'],
        database=database,
    )


def pyodbc_connect(datacenter, database=None):
    data = db_connections[datacenter]
    return "DRIVER=FreeTDS;SERVER={db_server};port={port};DATABASE={database};UID={uid};PWD={pwd};TDS_Version=7.3".format(
        db_server=data['server'],
        port=data['port'],
        database=database if database else data['database'],
        uid=data["user"],
        pwd=data["password"],
    )


nameservices = {
    "ha-nameservice-sjc": [
        {
            "host": "sjc-hdfsnn01.pulse.prod",
            "port": 9000,
        },
        {
            "host": "sjc-hdfsnn02.pulse.prod",
            "port": 9000,
        },
    ],
    "nameservice1": [
        {
            "host": "lga-gridnn01.contextweb.prod",
            "port": 9000,
        },
        {
            "host": "lga-gridnn02.contextweb.prod",
            "port": 9000,
        },
    ],
}

job_history_servers = {
    "lga": "history-yarn-hadoop-dm.marathon.mesos.lga:19888",
    "sjc": "history-yarn-hadoop-dm.marathon.mesos.sjc:19888",
}

chronos_server = {
    "lga": "lga-chronos.pulse.prod:4400",
    "sjc": "sjc-chronos.pulse.prod:4400",
}

mesos_server = {
    "lga": "lga-mms.pulse.prod:5050",
    "sjc": "sjc-mms.pulse.prod:5050",
}

impala_statestore = {
    "lga": "statestore-impala-hadoop-dm.marathon.mesos.lga",
    "sjc": "statestore-impala-hadoop-dm.marathon.mesos.sjc",
}

resource_managers = {
    "lga": [
        "http://lga-grid108.contextweb.prod:8088/",
        "http://lga-grid109.contextweb.prod:8088/",
    ],
    "sjc": [
        "http://sjc-hdfsjt01.pulse.prod:8088/",
        "http://sjc-hdfsjt02.pulse.prod:8088/",
    ],
}

db_connections = {
    "lga": {
        "server":   "lga-db3.pulse.data",
        "port":     50577,
        "database": "ContextAd",
        "user":     "sqoopuser",
        "password": "sqoop@207*",
        "instancename": "Portal",
    },
    "sjc": {
        "server":   "sjc-db1.pulse.data",
        "port":     53353,
        "database": "ContextAd",
        "user":     "sqoopuser",
        "password": "sqoop@207*",
        "instancename": "DR",
    },
    "utility": {
        "server":   "lga-dbs01.pulse.data",
        "port":     51172,
        "database": "Utility",
        "user":     "sqoopuser",
        "password": "sqoop@207*",
        "instancename": "aux",
    },
}

graphite_hosts = {
    "lga": {
        "graphite_host": "lga-crelay.pulse.prod",
        "graphite_port": 2003,
    },
}

krb_config = {
    "dev": {
        "use_sasl": True,
        "principal": "hdfs/lga-hdfsdev02.pulse.prod@PULSE.TESTING",
        "keytab_file": "/etc/krb5/dev-hdfs.keytab",
    },
    "lga": {
        "use_sasl": True,
        "principal": "aggr@PULSE.CORP",
        "keytab_file": "/etc/krb5/aggr.keytab",
        "beeline_user": "aggr",
        "beeline_password": "Pulse1ag",
    },
    "sjc": {
        "use_sasl": True,
        "principal": "aggr@PULSE.CORP",
        "keytab_file": "/etc/krb5/aggr.keytab",
        "beeline_user": "aggr",
        "beeline_password": "Pulse1ag",
    }
}

graphite_stores = {
    "lga": "http://lga-graphite02.pulse.prod/",
    "sjc": "http://sjc-graphite02.pulse.prod/",
}

hive_metastore_services = {
    "lga": [
        {
            "host": "lga-metastore01.pulse.prod",
            "port": 9083,
            "use_sasl": False,
            "username": "hdfsmeta",
            "password": "BLatbyunMysAjv8",
        },
    ],
    "dev": [
        {
            "host": "lga-hdfsdev01.pulse.prod",
            "port": 9083,
            "use_sasl": True,
            "username": "admin",
            "password": "admin",
        }
    ]
}

hdfs_web_config = {
    'lga': {
        'http_namenodes': [
            'http://lga-gridnn01.contextweb.prod:50070',
            'http://lga-gridnn02.contextweb.prod:50070'
        ]
    }
}

hdfs_config = {
    "dev": {
        "host": "nsdev1",
        "port": None,
        "pars": {
            "dfs.nameservices": "nsdev1",
            "dfs.ha.namenodes.nsdev1": "namenode01,namenode02",
            "dfs.namenode.rpc-address.nsdev1.namenode01": "lga-hdfsdev01.pulse.prod:8020",
            "dfs.namenode.rpc-address.nsdev1.namenode02": "lga-hdfsdev02.pulse.prod:8020",
            "dfs.namenode.http-address.nsdev1.namenode01": "lga-hdfsdev01.pulse.prod:50070",
            "dfs.namenode.http-address.nsdev1.namenode02": "lga-hdfsdev02.pulse.prod:50070",
            "hadoop.security.authentication": "kerberos",
        },
    },
    "lga": {
        "host": "nameservice1",
        "port": None,
        "pars": {
            "dfs.nameservices": "nameservice1",
            "dfs.ha.namenodes.nameservice1": "namenode01,namenode02",
            "dfs.namenode.rpc-address.nameservice1.namenode01": "lga-gridnn01.contextweb.prod:9000",
            "dfs.namenode.rpc-address.nameservice1.namenode02": "lga-gridnn02.contextweb.prod:9000",
            "dfs.namenode.http-address.nameservice1.namenode01": "lga-gridnn01.contextweb.prod:50070",
            "dfs.namenode.http-address.nameservice1.namenode02": "lga-gridnn02.contextweb.prod:50070",
            "hadoop.security.authentication": "kerberos",
        },
    }
}

hive_servers = {
    "lga": {
        "beeline_uri": "jdbc:hive2://lga-zk00.pulse.prod:2181,lga-zk01.pulse.prod:2181,lga-zk02.pulse.prod:2181/;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2",
        "username": "aggr",
        "password": "Pulse1ag",
        "discovery": {"zk": "lga-zk00.pulse.prod:2181,lga-zk01.pulse.prod:2181,lga-zk02.pulse.prod:2181", "ns": "hiveserver2"},
    },
}

# memcached nodes for audience segments, e.g. LiveRamp, Hudson, Health, etc.
audience_memcached_nodes = {
    "lga": [
        ('10.201.12.78', 11303),
        ('10.201.12.79', 11303),
        ('10.201.13.133', 11303),
        ('10.201.15.200', 11303)
    ],
    "sjc": [
        ('10.210.13.48',  11303),
        ('10.210.101.37', 11303),
        ('10.210.15.26',  11303)
    ],
    "ams": [
        ('10.220.13.21', 11303),
        ('10.220.13.22', 11303)
    ]
}


def is_secure(dc=None):
    if not dc:
        dc = thisdc()

    try:
        return hdfs_config[dc]["pars"]["hadoop.security.authentication"].lower() == "kerberos"
    except KeyError:
        return False


def get_datacenters():
    return [
        "ams",
        "lga",
        "sjc",
    ]


def get_sources():
    """The list of sources in fact tables"""
    # TODO add fix clicks and any other sources when we add them
    return ["{}-kafka".format(datacenter) for datacenter in get_datacenters()]


def get_beeline_cmd_params(dc, hive_server_conf=hive_servers):
    params = ['--showHeader', 'false', '--fastConnect', 'true',
              '--autoCommit', 'false', '--showNestedErrs', 'true',
              '--autosave', 'false', '--incremental', 'true',
              ]
    uri = hive_server_conf.get(dc, {}).get('beeline_uri', None)
    if uri:
        params.extend(['-u', "'{uri}'".format(uri=uri)])
    user = krb_config.get(dc, {}).get('beeline_user', None)
    if user:
        params.extend(['-n', user])
    password = krb_config.get(dc, {}).get('beeline_password', None)
    if password:
        params.extend(['-p', password])
    return params


def get_random_hive_host(dc=None):
    if not dc:
        dc = thisdc()
    hive = hive_servers[dc]
    ret = {"username": hive['username'], "password": hive['password']}
    zkhosts = hive['discovery']['zk']

    zk_retry = {
        "max_tries": 10,
        "delay": 1.0,
        "max_delay": 120,
    }

    zk = KazooClient(
        hosts=zkhosts,
        timeout=10.0,
        connection_retry=zk_retry,
        command_retry=zk_retry,
        logger=getlogger(),
    )
    zk.start()

    try:
        hosts = zk.get_children('/' + hive['discovery']['ns'])
        hosts = [x.replace('serverUri=', '') for x in hosts]
        hosts = [x.split(';')[0] for x in hosts]
        hosts = [x.split(':') for x in hosts]
        hosts = [(x[0], int(x[1])) for x in hosts]
        shuffle(hosts)
        host = hosts[0]
        ret['host'] = host[0]
        ret['port'] = host[1]
    finally:
        zk.stop()
        zk.close()

    return ret


class QueryRunner():
    database = ''
    dc = 'lga'
    query = ''

    def run_query(self, query):
        with dbclient(pyodbc_connect(self.dc, self.database)) as cursor:
            res = cursor.execute(self.query)
            getlogger().debug('\n>>>>>>>>>>>>>>>>type of cursor.execute is {}'.format(type(res)))
            return as_pandas(res)


if __name__ == '__main__':
    query = '\n'.join(sys.argv[1:])
    sys.stderr.write('Running query {}'.format(query))
    query_runner = QueryRunner()
    res = query_runner.run_query(query)
    print(res)
