import Target from "./target";
import IService from "./iservice";

export default abstract class Service<T> implements IService<T> {
    public constructor(public target: Target) {}
    abstract query(): Promise<T>;
    abstract save(entity: T): Promise<T>;
    abstract enableFeature(): boolean;
}
