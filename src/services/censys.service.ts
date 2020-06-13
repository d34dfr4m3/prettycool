import { server } from "@prisma/client";
import CensysIo from "censys.io";
import { prisma } from "../client/database/connection";
import { locationMap, protocolMap, ProtocolMap, serverMap } from "../client/database/query";
import coordinates from "../helpers/coordinates";
import { censysProtocol, idProtocol } from "../helpers/protocol";
import Service from "./service";
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
    insertLocation: async (location: Location, target: string) => {
        try {
            const o = await prisma.location.create({
                data: {
                    city: location.city,
                    continent: location.continent,
                    country: location.registered_country,
                    country_code: location.registered_country_code,
                    latitude: location.latitude,
                    longitude: location.longitude,
                    province: location.province,
                    timezone: location.timezone,
                },
            });
            return o;
        } catch (error) {
            return null;
        }
    },
    upsertProtocols: async (x: Ipv4, server: server, protocols: ProtocolMap, targetId: string) => {
        try {
            const promises = x.protocols.map(async (p) => {
                const [port, service] = censysProtocol(p);
                const key = idProtocol(port, service, x.ip);
                const id = protocols.get(key)?.id || "";
                const protocol = {
                    port,
                    target: { connect: { id: targetId } },
                    service_name: service,
                    server: { connect: { id: server.id } },
                };
                const save = await prisma.protocol.upsert({
                    create: protocol,
                    update: protocol,
                    where: { id },
                });
                protocols.set(key, save);
                return save;
            });
            return Promise.all(promises);
        } catch (error) {
            return null;
        }
    },
    upsertServerIpv4: async (x: Ipv4, idLocation: string, target: string) => {
        try {
            const data = {
                ip: x.ip,
                target: {
                    connect: { id: target },
                },
                ip_version: "IPV4",
                location: { connect: { id: idLocation } },
            };
            return prisma.server.upsert({ where: { ip: x.ip }, create: data, update: data });
        } catch (error) {
            throw error;
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

export class CensysIpv4Service extends Service<ICensysIpv4> {
    public enableFeature(): boolean {
        return !!process.env.CENSYS_UID && !!process.env.CENSYS_SECRET;
    }

    public async query(): Promise<ICensysIpv4> {
        return query(this.target.domain, search);
    }

    public async save(entity: ICensysIpv4): Promise<ICensysIpv4> {
        try {
            const locations = await locationMap();
            const protocols = await protocolMap();
            const servers = await serverMap();
            const inserts = entity.results.map(async (x) => {
                const coords = coordinates.fromCensysResult(x);
                let location;
                if (!locations.has(coords)) {
                    location = (await Censys.insertLocation(x.location, this.target.id)) as any;
                    locations.set(coords, location);
                } else {
                    location = locations.get(coords);
                }
                const save = await Censys.upsertServerIpv4(x, location.id, this.target.id);
                servers.set(save?.ip!, save as any);
                await Censys.upsertProtocols(x, save, protocols, this.target.id);
            });
            await Promise.all(inserts);
        } catch (error) {
            throw error;
        } finally {
            return entity;
        }
    }
}

export class CensysSitesService extends Service<ICensysSites> {
    enableFeature(): boolean {
        throw new Error("Method not implemented.");
    }
    public async query(): Promise<ICensysSites> {
        return query(this.target.domain, websites);
    }

    save(entity: ICensysSites): Promise<ICensysSites> {
        throw new Error("Method not implemented.");
    }
}

export class CensysCertificatesService extends Service<ICensysCertificates> {
    enableFeature(): boolean {
        throw new Error("Method not implemented.");
    }
    public async query(): Promise<ICensysCertificates> {
        return query(this.target.domain, certificates);
    }

    save(entity: ICensysCertificates): Promise<ICensysCertificates> {
        throw new Error("Method not implemented.");
    }
}
