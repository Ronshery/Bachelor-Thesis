import { Collection, Item } from "@vuex-orm/core";
import Benchmark from "@/models/Benchmark";

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
  block_size: "Block size",
  total_size: "Total size",
  operation: "Operation",
  number_of_requests: "Number of requests",
  number_of_processes: "Number of processes",
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
  latencyApexArguments(
    currentBms: Collection<Benchmark>,
    latestBm: Item<Benchmark>,
    bmType: BmType
  ) {
    const latencySeries = [
      {
        name: "min (ms)",
        data: [] as string[],
      },
      {
        name: "avg (ms)",
        data: [] as string[],
      },
      {
        name: "max (ms)",
        data: [] as string[],
      },
      {
        name: "95p (ms)",
        data: [] as string[],
      },
    ];

    if (bmType == BmType.DISK_IOPING) {
      latencySeries.splice(3, 1, {
        name: "mdev",
        data: [] as string[],
      });
    }
    const categories: string[] = [];
    for (const bm of currentBms) {
      const tmp = bm.$getAttributes();
      const metrics = tmp.metrics;
      latencySeries[0].data.push(metrics.latency_min);
      latencySeries[1].data.push(metrics.latency_avg);
      latencySeries[2].data.push(metrics.latency_max);
      if (bmType == BmType.DISK_IOPING) {
        latencySeries[3].data.push(metrics.latency_mdev);
      } else {
        latencySeries[3].data.push(metrics.latency_95p);
      }
      const date = new Date(tmp.started + "Z");
      const clock = date.toLocaleString("en-US", {
        hour: "numeric",
        minute: "numeric",
        hour12: true,
      });
      const month =
        date.getMonth() < 10 ? `0${date.getMonth()}` : date.getMonth();
      categories.push(`${month}/${date.getDate()} ${clock}`);
    }

    // on: panning and zoom enabled
    const tickPlacement = currentBms.length <= 3 ? "between" : "on";

    //  because of bug needs to be defined here
    let latencyOptions = JSON.parse(JSON.stringify(defaultBarOptions));
    latencyOptions = {
      ...latencyOptions,
      chart: {
        ...latencyOptions.chart,
        id: "latency-" + latestBm?.$getAttributes().id,
        group: bmType,
      },
      xaxis: {
        ...latencyOptions.xaxis,
        min: currentBms.length - 3,
        max: currentBms.length,
        categories: categories,
        tickPlacement: tickPlacement,
      },
      tooltip: {
        ...latencyOptions.tooltip,
        fixed: {
          ...latencyOptions.tooltip.fixed,
          offsetY: -120,
        },
      },
    };
    return { latencyOptions, latencySeries };
  },
  eventsApexArguments(
    currentBms: Collection<Benchmark>,
    latestBm: Item<Benchmark>,
    bmType: BmType
  ) {
    const eventsSeries = [
      {
        name: "#events avg",
        data: [] as string[],
      },
      {
        name: "#events stddev",
        data: [] as string[],
      },
      {
        name: "exctime avg (ms)",
        data: [] as string[],
      },
      {
        name: "exctime stddev (ms)",
        data: [] as string[],
      },
    ];
    if (bmType == BmType.CPU_SYSBENCH) {
      eventsSeries.splice(0, 0, {
        name: "#events per second",
        data: [] as string[],
      });
    }
    const categories: string[] = [];
    for (const bm of currentBms) {
      const tmp = bm.$getAttributes();
      const metrics = tmp.metrics;

      if (bmType == BmType.MEMORY_SYSBENCH) {
        eventsSeries[0].data.push(
          Number(metrics.fairness_events.split("/")[0]).toFixed(0)
        );
        eventsSeries[1].data.push(
          Number(metrics.fairness_events.split("/")[1]).toFixed(0)
        );
        eventsSeries[2].data.push(
          Number(metrics.fairness_exctime.split("/")[0]).toFixed(2)
        );
        eventsSeries[3].data.push(
          Number(metrics.fairness_exctime.split("/")[1]).toFixed(2)
        );
      } else {
        eventsSeries[0].data.push(Number(metrics.events_per_second).toFixed(0));
        eventsSeries[1].data.push(
          Number(metrics.fairness_events_avg).toFixed(0)
        );
        eventsSeries[2].data.push(
          Number(metrics.fairness_events_stddev).toFixed(0)
        );
        eventsSeries[3].data.push(
          Number(metrics.fairness_exctime_avg).toFixed(2)
        );
        eventsSeries[4].data.push(
          Number(metrics.fairness_exctime_stddev).toFixed(2)
        );
      }

      const date = new Date(tmp.started + "Z");
      const clock = date.toLocaleString("en-US", {
        hour: "numeric",
        minute: "numeric",
        hour12: true,
      });
      const month =
        date.getMonth() < 10 ? `0${date.getMonth()}` : date.getMonth();
      categories.push(`${month}/${date.getDate()} ${clock}`);
    }
    const tickPlacement = currentBms.length <= 3 ? "between" : "on";

    let eventsOptions = JSON.parse(JSON.stringify(defaultBarOptions));
    eventsOptions = {
      ...eventsOptions,
      chart: {
        ...eventsOptions.chart,
        id: "events-" + latestBm?.$getAttributes().id,
        group: bmType,
      },
      xaxis: {
        ...eventsOptions.xaxis,
        min: currentBms.length - 3,
        max: currentBms.length,
        categories: categories,
        tickPlacement: tickPlacement,
      },
    };
    return { eventsOptions, eventsSeries };
  },
  convertTotalTime(time: string) {
    if (time == null) {
      return time;
    }
    const substr = time.toString().substring(0, time.length - 1);
    let convertedTime = Number(substr).toFixed(0);
    convertedTime = convertedTime + time[time.length - 1];
    return convertedTime;
  },
};
