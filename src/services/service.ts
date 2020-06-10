import Target from "./target";

export default abstract class Service {
  public constructor(public target: Target) {}
}
