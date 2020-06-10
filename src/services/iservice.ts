import Target from "./target";

export default interface IService<T> {
    query(): Promise<T>;
    save(entity: T): Promise<T>;
}
