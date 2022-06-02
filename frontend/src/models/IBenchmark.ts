export interface IBenchmark {
  id: string;
  spec: object;
  resource: string;
  type: string;
  node: string;
  started: Date;
  metrics: Record<string, string> | null;
}
