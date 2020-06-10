import { v4 as uuid } from "uuid";
import { TargetQuery } from "../client/database/query";

export default class Target {
    public id: string;

    public constructor(public domain: string, public company: string) {
        this.id = "";
    }

    public async save(): Promise<void> {
        const [previousTarget] = await TargetQuery.where("domain", "=", this.domain).select("*");
        if (!previousTarget) {
            const [target] = await TargetQuery.returning("*").insert({
                company_name: this.company,
                domain: this.domain,
                id: uuid(),
            });
            this.id = target.id;
        } else {
            this.id = previousTarget.id!;
        }
    }
}
