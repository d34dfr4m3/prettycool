import { Ipv4 } from "../services/censys.service";
import { Tables } from '../client/database/connection';

export default {
    fromCensysResult: ({ location: x }: Ipv4) =>
        `${parseFloat(x.latitude.toString())},${parseFloat(x.longitude.toString())}`,
    fromDatabase: (x: Tables["location"]) =>
        `${parseFloat(x.latitude.toString())},${parseFloat(x.longitude.toString())}`,
};
