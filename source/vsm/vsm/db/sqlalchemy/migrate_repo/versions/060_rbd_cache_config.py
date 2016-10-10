# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2014 Intel Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from sqlalchemy import Boolean, Column, DateTime, Text
from sqlalchemy import Integer, MetaData, String, Table

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine;
    # bind migrate_engine to your metadata
    meta = MetaData()
    meta.bind = migrate_engine

    rbd_cache_config = Table(
        'rbd_cache_config', meta,
        Column('id', Integer, primary_key=True, nullable=False),
        Column('cache_dir', String(length=255), nullable=False),
        Column('clean_start', String(length=255), nullable=False),
        Column('enable_memory_usage_tracker', Boolean, default=False),
        Column('object_size', String(length=255), nullable=False),
        Column('cache_total_size', String(length=255), nullable=False),
        Column('cache_dirty_ratio_min', String(length=255), nullable=False),
        Column('cache_dirty_ratio_max', String(length=255), nullable=False),
        Column('cache_ratio_health', String(length=255), nullable=False),
        Column('cache_ratio_max', String(length=255), nullable=False),
        Column('cache_flush_interval', String(length=255), nullable=False),
        Column('cache_evict_interval', String(length=255), nullable=False),
        Column('cache_flush_queue_depth', String(length=255), nullable=False),
        Column('agent_thread_num', String(length=255), nullable=False),
        Column('cache_service_threads_num', String(length=255), nullable=False),
        Column('created_at', DateTime(timezone=False)),
        Column('updated_at', DateTime(timezone=False)),
        Column('deleted_at', DateTime(timezone=False)),
        Column('deleted', Boolean(create_constraint=True, name=None)),
    )

    try:
        rbd_cache_config.create()
    except Exception:
        meta.drop_all(tables=[rbd_cache_config])
        raise

def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    rbd_cache_config = Table('rbd_cache_config',
                    meta,
                    autoload=True)
    rbd_cache_config.drop()
