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

export const mappings = {
  num_threads: "Number of threads",
  prime_numbers_limit: "Prime numbers limit",
  total_time: "Total time",
  [BmResource.CPU]: "CPU benchmarks",
  [BmResource.MEMORY]: "Memory benchmarks",
  [BmResource.DISK]: "Disk benchmarks",
  [BmResource.NETWORK]: "Network benchmarks",
};

export const defaultBarOptions = {
  chart: {
    id: "",
    type: "bar",
    stacked: false,
    group: undefined,
  },
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 2,
      dataLabels: {
        position: "top",
      },
    },
  },
  tooltip: {
    intersect: false,
    shared: true,
    fixed: {
      enabled: true,
      position: "topRight",
      offsetY: -150,
    },
  },
  dataLabels: {
    offsetY: -20,
    style: {
      colors: ["#000000"],
    },
  },
  xaxis: {
    type: "category",
    min: 1,
    max: 4,
    categories: [],
    tickPlacement: "between",
  },
  noData: {
    text: "run to see results",
    offsetY: -15,
    style: {
      color: "#000000",
    },
  },
};

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
