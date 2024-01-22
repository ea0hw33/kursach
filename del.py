
#!/usr/bin/python
#
# A simple example of connecting to a cluster
# To install the driver Run pip install scylla-driver
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import DCAwareRoundRobinPolicy, TokenAwarePolicy
from cassandra.auth import PlainTextAuthProvider


def getCluster():
    profile = ExecutionProfile(load_balancing_policy=TokenAwarePolicy(DCAwareRoundRobinPolicy(local_dc='AWS_US_EAST_1')))

    return Cluster(
        execution_profiles={EXEC_PROFILE_DEFAULT: profile},
        contact_points=[
            "node-0.aws-us-east-1.3a4985428459cbf182aa.clusters.scylla.cloud", "node-1.aws-us-east-1.3a4985428459cbf182aa.clusters.scylla.cloud", "node-2.aws-us-east-1.3a4985428459cbf182aa.clusters.scylla.cloud"
        ],
        port=9042,
        auth_provider = PlainTextAuthProvider(username='scylla', password='BnOGd0b6q2pQeIl'))

print('Connecting to cluster')
cluster = getCluster()
session = cluster.connect()

print('Connected to cluster %s' % cluster.metadata.cluster_name)

print('Getting metadata')
for host in cluster.metadata.all_hosts():
    print('Datacenter: %s; Host: %s; Rack: %s' % (host.datacenter, host.address, host.rack))

cluster.shutdown()

