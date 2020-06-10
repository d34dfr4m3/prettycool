import knex from "knex";

export type Tables = {
    company_email: {
        id?: string;
        email: string;
        service_url: string;
        target_id: string;
    };
    target: {
        id?: string;
        company_name: string;
        domain: string;
    };
    protocol: {
        id?: string;
        service_name: string;
        port: number;
    };
    server: {
        id?: string;
        ip: string;
        ip_version: "IPV4" | "IPV6";
        location_id: string;
        protocols: Tables["protocol"];
    };
    location: {
        id?: string;
        country: string;
        longitude: number;
        province?: string;
        city?: string;
        latitude: number;
        timezone: string;
        continent: string;
        country_code: string;
    };
};

export const connection = knex({
    client: "pg",
    wrapIdentifier: (value) => value,
    pool: { min: 1, max: 25 },
    connection: {
        host: "localhost",
        user: "postgres",
        password: "12345",
        database: "prettycool",
    },
});
