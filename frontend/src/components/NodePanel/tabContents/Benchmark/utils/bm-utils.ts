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
