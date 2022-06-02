export const enum BmResource {
  CPU = "cpu",
  MEMORY = "memory",
  DISK = "disk",
  NETWORK = "network",
}

export const enum BmType {
  CPU_SYSBENCH = "cpu-sysbench",
  MEMORY_SYSBENCH = "memory-sysbench",
  DISK_IOPING = "disk-ioping",
  DISK_FIO = "disk-fio",
  NETWORK_IPERF3 = "network-iperf3",
  NETWORK_QPERF = "network-qperf",
}

export default {
  benchmarkNameMapper(bmName: BmResource): string {
    switch (bmName) {
      case BmResource.CPU:
        return "CPU benchmarks";
      case BmResource.MEMORY:
        return "Memory benchmarks";
      case BmResource.DISK:
        return "Disk benchmarks";
      case BmResource.NETWORK:
        return "Network benchmarks";
    }
    return "";
  },
  getBMDuration(options: string): string {
    if (!options) {
      return "1";
    }
    const optionsList = options.split(" ");
    let durationInSec = "";
    for (const option of optionsList) {
      if (option.includes("--time")) {
        durationInSec = option.split("=")[1];
        break;
      }
    }
    return durationInSec;
  },
};
