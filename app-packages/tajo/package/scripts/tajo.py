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
import os

from resource_management import *
import sys
import shutil

def tajo(name=None # 'master' or 'worker' or 'client'
              ):
  import params

  """
  if name in ["master","worker"]:
    params.HdfsDirectory(params.tajo_hdfs_root_dir,
                         action="create_delayed"
    )
    params.HdfsDirectory(None, action="create")
  """

  Directory( params.conf_dir,
      owner = params.tajo_user,
      group = params.user_group,
      recursive = True,
      content = params.input_conf_files_dir
  )

  XmlConfig( "tajo-site.xml",
            conf_dir = params.conf_dir,
            configurations = params.config['configurations']['tajo-site'],
            owner = params.tajo_user,
            group = params.user_group
  )

  File(format("{conf_dir}/tajo-env.sh"),
       owner = params.tajo_user,
       content=InlineTemplate(params.tajo_env_sh_template)
  )


  if (params.log4j_props != None):
    File(format("{params.conf_dir}/log4j.properties"),
         mode=0644,
         group=params.user_group,
         owner=params.tajo_user,
         content=params.log4j_props
    )
  elif (os.path.exists(format("{conf_dir}/log4j.properties"))):
    File(format("{params.conf_dir}/log4j.properties"),
      mode=0644,
      group=params.user_group,
      owner=params.tajo_user
    )

def tajo_TemplateConfig(name,
                         tag=None
                         ):
  import params

  TemplateConfig( format("{conf_dir}/{name}"),
      owner = params.tajo_user,
      template_tag = tag
  )
