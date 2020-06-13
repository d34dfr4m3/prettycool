import { location } from "@prisma/client";
import { Ipv4 } from "../services/censys.service";

export default {
    fromCensysResult: ({ location: x }: Ipv4) =>
        `${parseFloat(x.latitude.toString())},${parseFloat(x.longitude.toString())}`,
    fromDatabase: (x: location) => `${parseFloat(x.latitude.toString())},${parseFloat(x.longitude.toString())}`,
};
