import CensysIo from "censys.io";
import Service from "./service";
import IService from "./iservice";
import { Tables } from "../client/database/connection";
import { locationMap, serverMap, protocolMap, LocationQuery } from "../client/database/query";
import coordinates from "../helpers/coordinates";
import uuid from "../helpers/uuid";
require("dotenv").config();

type ICensysIpv4 = ICensys<Ipv4>;

type ICensysSites = ICensys<Sites>;

type ICensysCertificates = ICensys<Certificate>;

type ICensys<T> = {
    status: string;
    results: T[];
    metadata: Metadata;
};

type Metadata = {
    count: number;
    query: string;
    backend_time: number;
    page: number;
    pages: number;
};

type Certificate = {
    parsed: {
        fingerprint_sha256: string;
        subject_dn: string;
        issuer_dn: string;
    };
};

type Sites = {
    domain: string;
    alexa_rank: number;
};

export type Ipv4 = {
    ip: string;
    location: Location;
    protocols: string[];
};

type Location = {
    country: string;
    longitude: number;
    registered_country: string;
    registered_country_code: string;
    country_code: string;
    latitude: number;
    timezone: string;
    continent: string;
    province?: string;
    city?: string;
    postal_code?: string;
};

type CensysQuery<T> = (query: string, page?: number) => Promise<ICensys<T>>;

const instance = new CensysIo({
    apiID: process.env.CENSYS_UID,
    apiSecret: process.env.CENSYS_SECRET,
});

const search: CensysQuery<Ipv4> = async (query: string, page = 1): Promise<ICensysIpv4> =>
    instance.search("ipv4", { query, flatten: false, page }) as any;

export const websites: CensysQuery<Sites> = async (query: string, page = 1): Promise<ICensysSites> =>
    instance.search("websites", { query, flatten: false, page }) as any;

export const certificates: CensysQuery<Certificate> = async (query: string, page = 1): Promise<ICensysCertificates> =>
    instance.search("certificates", { query, flatten: false, page }) as any;

const Censys = {
    insertLocation: async (location: Location) => {
        const id = uuid();
        try {
            const o = {
                id,
                city: location.city,
                continent: location.continent,
                country: location.registered_country,
                country_code: location.registered_country_code,
                latitude: location.latitude,
                longitude: location.longitude,
                province: location.province,
                timezone: location.timezone,
            };
            await LocationQuery.insert(o);
            return o;
        } catch (error) {
            console.log("Error", id, error.message);
            return null;
        }
    },
};

const query = async <T>(domain: string, exec: CensysQuery<T>): Promise<ICensys<T>> => {
    const final = await exec(domain);
    let { pages, page } = final.metadata;
    for (page; pages !== page; page++) {
        const chunk = await exec(domain, page);
        final.results?.push(...chunk.results);
        final.metadata = chunk.metadata;
    }
    return final;
};

export class CensysIpv4Service extends Service implements IService<ICensysIpv4> {
    public async query(): Promise<ICensysIpv4> {
        return query(this.target.domain, search);
    }

    public async save(entity: ICensysIpv4): Promise<ICensysIpv4> {
        const locations = await locationMap();
        const protocols = await protocolMap();
        const servers = await serverMap();
        console.log(locations);
        const inserts = entity.results.slice(0, 5).map(async (x) => {
            const coords = coordinates.fromCensysResult(x);
            let location;
            if (!locations.has(coords)) {
                console.log("HAS", locations.has(coords), coords);
                location = (await Censys.insertLocation(x.location)) as any;
                locations.set(coords, location);
            } else {
                location = locations.get(coords);
            }
        });
        throw "";
    }
}

export class CensysSitesService extends Service implements IService<ICensysSites> {
    public async query(): Promise<ICensysSites> {
        return query(this.target.domain, websites);
    }

    save(entity: ICensysSites): Promise<ICensysSites> {
        throw new Error("Method not implemented.");
    }
}

export class CensysCertificatesService extends Service implements IService<ICensysCertificates> {
    public async query(): Promise<ICensysCertificates> {
        return query(this.target.domain, certificates);
    }

    save(entity: ICensysCertificates): Promise<ICensysCertificates> {
        throw new Error("Method not implemented.");
    }
}
