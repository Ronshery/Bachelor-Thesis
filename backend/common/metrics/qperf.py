from .common import BMMetricField
import dataclasses


@dataclasses.dataclass
class QpervesMetrics:
    tcp_bw_bandwidth: BMMetricField\
        = BMMetricField(r".*bw\s*=\s*(\d+\.\d+\s+GB\/sec)")
    tcp_bw_msg_rate: BMMetricField\
        = BMMetricField(r".*msg_rate\s*=\s*([\d\.]+\s+K\/sec)")
    tcp_bw_send_cost: BMMetricField\
        = BMMetricField(r".*send_cost\s*=\s*(\d+\.\d+\s+sec/GB)")
    tcp_bw_recv_cost: BMMetricField\
        = BMMetricField(r".*recv_cost\s*=\s*(\d+\.\d+\s+sec/GB)")
    tcp_bw_send_cpus_used: BMMetricField\
        = BMMetricField(r".*send_cpus_used\s*=\s*(\d+\s+% cpus)")
    tcp_bw_recv_cpus_used: BMMetricField\
        = BMMetricField(r".*recv_cpus_used\s*=\s*(\d+\s+% cpus)")

    tcp_lat_latency: BMMetricField\
        = BMMetricField(r".*latency\s*=\s*(\d+\.\d+\s+us)")
    tcp_lat_loc_cpus_used: BMMetricField\
        = BMMetricField(r".*loc_cpus_used\s*=\s*(\d+\s+% cpus)")
    tcp_lat_rem_cpus_used: BMMetricField\
        = BMMetricField(r".*rem_cpus_used\s*=\s*(\d+\s+% cpus)")


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