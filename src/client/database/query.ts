import { connection, Tables } from "./connection";
import coordinates from "../../helpers/coordinates";

export const TargetQuery = connection<Tables["target"]>("target");
export const CompanyEmailQuery = connection<Tables["company_email"]>("company_email");
export const ProtocolQuery = connection<Tables["protocol"]>("protocol");
export const ServerQuery = connection<Tables["server"]>("server");
export const LocationQuery = connection<Tables["location"]>("location");

export const protocolMap = async () => {
    const map = new Map<string, Tables["protocol"]>();
    const list = await ProtocolQuery.select("*");
    list.map((x) => map.set(`${x.port}/${x.service_name}`, x));
    return map;
};

export const serverMap = async () => {
    const map = new Map<string, Tables["server"]>();
    const list = await ServerQuery.select("*");
    list.map((x) => map.set(x.ip, x));
    return map;
};

export const locationMap = async () => {
    const map = new Map<string, Tables["location"]>();
    const list = await LocationQuery.select("*");
    list.forEach((x) => map.set(coordinates.fromDatabase(x), x));
    return map;
};
