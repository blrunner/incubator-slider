#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from functions import calc_xmn_from_xms
from resource_management import *
import status_params

# server configurations
config = Script.get_config()

tajo_root = config['configurations']['global']['app_root']
tajo_version = config['configurations']['global']['tajo_version']
conf_dir = format("{tajo_root}/conf")
daemon_script = format("{tajo_root}/tajo-{tajo_version}/bin/tajo-daemon.sh")

tajo_user = status_params.tajo_user
_authentication = config['configurations']['core-site']['hadoop.security.authentication']
security_enabled = ( not is_empty(_authentication) and _authentication == 'kerberos')
user_group = config['configurations']['global']['user_group']

# not supporting 32 bit jdk.
java64_home = config['hostLevelParams']['java_home']

# hadoop_home = config['configurations']['global']['hadoop_home']
log_dir = config['configurations']['global']['app_log_dir']
master_heapsize = config['configurations']['tajo-env']['tajo_master_heapsize']

worker_heapsize = config['configurations']['tajo-env']['tajo_worker_heapsize']
worker_xmn_max = config['configurations']['tajo-env']['tajo_worker_xmn_max']
worker_xmn_percent = config['configurations']['tajo-env']['tajo_worker_xmn_ratio']
worker_xmn_size = calc_xmn_from_xms(worker_heapsize, worker_xmn_percent, worker_xmn_max)

pid_dir = status_params.pid_dir
input_conf_files_dir = config['configurations']['global']['app_input_conf_dir']

ganglia_server_host = default('/configurations/global/ganglia_server_host', '')
ganglia_server_port = default('/configurations/global/ganglia_server_port', '8663')

#log4j.properties
if (('tajo-log4j' in config['configurations']) and ('content' in config['configurations']['tajo-log4j'])):
  log4j_props = config['configurations']['tajo-log4j']['content']
else:
  log4j_props = None

tajo_env_sh_template = config['configurations']['tajo-env']['content']

tajo_hdfs_root_dir = config['configurations']['tajo-site']['tajo.rootdir']

#for create_hdfs_directory
hostname = config["hostname"]
hadoop_conf_dir = "/etc/hadoop/conf"
hdfs_user_keytab = config['configurations']['global']['hdfs_user_keytab']
hdfs_user = config['configurations']['global']['hdfs_user']
kinit_path_local = functions.get_kinit_path([default("kinit_path_local",None), "/usr/bin", "/usr/kerberos/bin", "/usr/sbin"])
import functools
#create partial functions with common arguments for every HdfsDirectory call
#to create hdfs directory we need to call params.HdfsDirectory in code
HdfsDirectory = functools.partial(
  HdfsDirectory,
  conf_dir=hadoop_conf_dir,
  hdfs_user=hdfs_user,
  security_enabled = security_enabled,
  keytab = hdfs_user_keytab,
  kinit_path_local = kinit_path_local
)
