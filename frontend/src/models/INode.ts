export interface INode {
  id: number;
  name: string;
  color: string;
  apiVersion: any;
  kind: any;
  metadata: any;
  spec: any;
  status: any;
  show: boolean;
  bmScore: number;
}
