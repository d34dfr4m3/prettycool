import Linq from "linq-arrays";
import type { Tables } from "../client/database/connection";
import { http } from "../client/http";
import dotenv from "../dotenv";
import IService from "./iservice";
import Service from "./service";
import { v4 as uuid } from "uuid";
import { connection } from "../client/database/connection";
import { CompanyEmailQuery } from "../client/database/query";

const Hunter = {
    insert: async (data: Tables["company_email"] | Tables["company_email"][]) => {
        let q;
        if (Array.isArray(data)) {
            q = CompanyEmailQuery.insert(
                data.map((x) => ({
                    id: uuid(),
                    email: x.email,
                    target_id: x.target_id,
                    service_url: x.service_url,
                })),
            );
        } else {
            q = CompanyEmailQuery.insert({
                id: uuid(),
                email: data.email,
                target_id: data.target_id,
                service_url: data.service_url,
            });
        }
        return connection.raw(`? ON CONFLICT ("serviceUrl") DO NOTHING`, [q]);
    },
};

const getUrl = (domain: string, offset = 0) => {
    const [name] = domain.split(".");
    const url = `https://api.hunter.io/v2/domain-search?company=${name}&domain=${domain}&api_key=${dotenv.HUNTER_SECRET}&offset=${offset}`;
    return url;
};

export class HunterService extends Service implements IService<IHunter> {
    public async save(entity: IHunter): Promise<IHunter> {
        const items = [] as Tables["company_email"][];
        entity.emails.forEach((email) =>
            email.sources.forEach((source) => {
                items.push({
                    email: email.value,
                    service_url: source.uri,
                    target_id: this.target.id,
                });
            }),
        );
        try {
            return await Hunter.insert(items);
        } catch (error) {
            throw error;
        }
    }

    public async query(): Promise<IHunter> {
        try {
            const response = await http.get<{ data: IHunter; meta: Meta }>(getUrl(this.target.domain));
            const { data, meta } = response.data;
            const requestTotal = Math.round(meta.results / meta.limit);
            for (let i = 0; i < requestTotal; i += 1) {
                const secondaryLoop = await http.get<{ data: IHunter; meta: Meta }>(getUrl(this.target.domain, i + 10));
                data.emails.push(...secondaryLoop.data.data.emails);
            }
            return { ...data, emails: Linq.Unique(data.emails, "value") };
        } catch (error) {
            throw error;
        }
    }
}

export interface IHunter {
    domain: string;
    disposable: boolean;
    webmail: boolean;
    accept_all: boolean;
    pattern: string;
    organization: string;
    country: null;
    state: null;
    emails: Email[];
}

export interface Email {
    value: string;
    type: string;
    confidence: number;
    sources: Source[];
    first_name: string;
    last_name: string;
    position: string;
    seniority: string;
    department: string;
    linkedin: string | null;
    twitter: string;
    phone_number: string | null;
}

export interface Source {
    domain: string;
    uri: string;
    extracted_on: Date;
    last_seen_on: Date;
    still_on_page: boolean;
}

export interface Meta {
    results: number;
    limit: number;
    offset: number;
    params: Params;
}

export interface Params {
    domain: string;
    company: string;
    type: null;
    seniority: null;
    department: null;
}
