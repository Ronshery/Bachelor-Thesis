export default {
  benchmarkNameMapper(bmName: string): string {
    switch (bmName) {
      case "cpu":
        return "CPU benchmarks";
      case "memory":
        return "Memory benchmarks";
      case "disk":
        return "Disk benchmarks";
      case "network":
        return "Network benchmarks";
    }
    return "";
  },
};
