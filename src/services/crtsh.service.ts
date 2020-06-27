import axios from "axios";
import Linq from "linq-arrays";
import { userAgents } from "../helpers/ua";
import Service from "./service";
import dotenv from "../dotenv";

export type ICrtSh = {
    issuer_ca_id: number;
    issuer_name: string;
    name_value: string;
    id: number;
    entry_timestamp: Date;
    not_before: Date;
    not_after: Date;
}[];

const url = new URL("https://crt.sh/");
url.searchParams.append("output", "json");
export class CrtShService extends Service<string[]> {
    public enableFeature(): boolean {
        return Boolean(dotenv.CRTSH).valueOf();
    }

    public async query(): Promise<string[]> {
        try {
            url.searchParams.set("q", this.target.domain);
            const { data } = await axios.get<ICrtSh>(url.href, { timeout: 40000 });
            const items: string[] = [];
            data.forEach((crt) => {
                const domain = crt.name_value.split("\n").filter(Boolean);
                domain.forEach((domain) => items.push(domain));
            });
            return Linq.Unique(items);
        } catch (error) {
            console.log(error);
            throw error;
        }
    }
    save(entity: string[]): Promise<string[]> {
        throw new Error("Method not implemented.");
    }
}
