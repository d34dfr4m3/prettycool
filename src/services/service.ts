import Target from "./target";

export default abstract class Service<T> {
    public constructor(public target: Target) {}
    abstract query(): Promise<T>;
    abstract save(entity: T): Promise<T>;
    abstract enableFeature(): boolean;
}
