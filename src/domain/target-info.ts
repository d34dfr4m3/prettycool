import Target from "../services/target";
import { Domain } from './domain';

export class TargetInfo {
    constructor(public target: Target, public domains: Domain[]) {}
}
