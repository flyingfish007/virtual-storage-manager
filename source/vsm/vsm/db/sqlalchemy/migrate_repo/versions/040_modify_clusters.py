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

from sqlalchemy import and_, String, Column, MetaData, select, Table, Integer

def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    clusters = Table('clusters', meta, autoload=True)
    clusters.drop_column('primary_public_network')
    clusters.drop_column('secondary_public_network')
    clusters.drop_column("journal_size")
    clusters.drop_column("size")
    clusters.drop_column("osd_heartbeat_interval")
    clusters.drop_column("osd_heartbeat_grace")

    management_network = Column('management_network', String(length=255))
    ceph_public_network = Column('ceph_public_network', String(length=255))

    clusters.create_column(management_network)
    clusters.create_column(ceph_public_network)


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    clusters = Table('clusters', meta, autoload=True)

    clusters.drop_column('management_network')
    clusters.drop_column('ceph_public_network')
    primary_public_network = Column('primary_public_network', String(length=255))
    secondary_public_network = Column('secondary_public_network', String(length=255))
    journal_size = Column(Integer, nullable=False)
    size = Column(Integer, nullable=True)
    osd_heartbeat_interval = Column('osd_heartbeat_interval',Integer, nullable=True)
    osd_heartbeat_grace=Column('osd_heartbeat_grace',Integer, nullable=True)

    clusters.create_column(primary_public_network)
    clusters.create_column(secondary_public_network)
    clusters.create_column(journal_size)
    clusters.create_column(size)
    clusters.create_column(osd_heartbeat_interval)
    clusters.create_column(osd_heartbeat_grace)
