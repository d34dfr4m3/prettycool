import { location, protocol } from "@prisma/client";
import coordinates from "../../helpers/coordinates";
import { idProtocol } from "../../helpers/protocol";
import { connection, Tables } from "./connection";

export const TargetQuery = connection<Tables["target"]>("target");
export const CompanyEmailQuery = connection<Tables["company_email"]>("company_email");
export const ProtocolQuery = connection<protocol>("protocol");
export const ServerQuery = connection<Tables["server"]>("server");
export const LocationQuery = connection<location>("location");

export type ProtocolMap = Map<string, protocol>;

export const protocolMap = async () => {
    const map = new Map<string, protocol>();
    const list = await ProtocolQuery.select("*");
    list.map((x) => map.set(idProtocol(x.port, x.service_name, x.server_id), x));
    return map;
};

export const serverMap = async () => {
    const map = new Map<string, Tables["server"]>();
    const list = await ServerQuery.select("*");
    list.map((x) => map.set(x.ip, x));
    return map;
};

export const locationMap = async () => {
    const map = new Map<string, location>();
    const list = await LocationQuery.select("*");
    list.forEach((x) => map.set(coordinates.fromDatabase(x), x));
    return map;
};
