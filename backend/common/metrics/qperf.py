from .common import BMMetricField
import dataclasses


@dataclasses.dataclass
class QpervesMetrics:
    pass
    # transfer_bitrates: BMMetricField\
    #     = BMMetricField(r".*(\d+\.\d+\s+Gbits\/sec).*", collect_list=True)


# example pod log
# tcp_bw:
#     bw              =  3.44 GB/sec
#     msg_rate        =  52.5 K/sec
#     time            =    10 sec
#     send_cost       =   794 ms/GB
#     recv_cost       =   794 ms/GB
#     send_cpus_used  =   273 % cpus
#     recv_cpus_used  =   273 % cpus
# tcp_lat:
#     latency        =  15.2 us
#     msg_rate       =    66 K/sec
#     time           =    10 sec
#     loc_cpus_used  =   147 % cpus
#     rem_cpus_used  =   147 % cpus