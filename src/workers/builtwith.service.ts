import axios from "axios";
import Linq from "linq-arrays";
import cheerio from "cheerio";
import { Domain } from "../domain/domain";
import { userAgents } from "../helpers/ua";

type IBuiltWith = { title: string; site: string };

const querySelectorAll = ($: CheerioStatic, query: string): [string, string][] => {
    const items: [string, string][] = [];
    $(query).map((_, e) => {
        const el = $(e);
        items.push([el.attr("href")!, el.text()]);
    });
    return items;
};

const getQuery = (n: number) =>
    `#mainForm > div:nth-child(3) > div > div.col-md-8.pr-1.pl-4 > div:nth-child(${n}) > div > div > div > h2 > a`;

const getServiceSite = async ([href, title]: [string, string], services: IBuiltWith[]) => {
    const response = await axios.get<string>(href);
    console.log("ANALYZE SERVICE", href, title);
    const $ = cheerio.load(response.data);
    $(
        "#mainForm > div.container > div > div.col-lg-8 > div:nth-child(4) > div > div:nth-child(1) > div.col-9.col-md-10 > p.xsmall.mb-2 > a",
    ).map((_, e) => {
        const el = $(e);
        services.push({ site: el.attr("href")!, title });
    });
};

const targetAnalyze = async (domain: string) => {
    const services: IBuiltWith[] = [];
    try {
        const replaceDomain = domain.trim().replace(/^w{3}./i, "");
        console.log(replaceDomain);
        const url = `https://builtwith.com/${replaceDomain}`;
        const response = await axios.get<string>(url, { httpAgent: Linq.Random(userAgents) });
        console.log("RESPONSE", url);
        const $ = cheerio.load(response.data);
        const trackingTech: [string, string][] = querySelectorAll($, getQuery(1));
        console.log("TECH", trackingTech);
        const widgets: [string, string][] = querySelectorAll($, getQuery(2));
        const languages: [string, string][] = querySelectorAll($, getQuery(3));
        const eCommerces: [string, string][] = querySelectorAll($, getQuery(4));
        const frameworks: [string, string][] = querySelectorAll($, getQuery(5));
        const cdn: [string, string][] = querySelectorAll($, getQuery(6));
        const mobile: [string, string][] = querySelectorAll($, getQuery(7));
        const payments: [string, string][] = querySelectorAll($, getQuery(8));
        const medias: [string, string][] = querySelectorAll($, getQuery(9));
        const cms: [string, string][] = querySelectorAll($, getQuery(10));
        const jsFrameworks: [string, string][] = querySelectorAll($, getQuery(11));
        const advertising: [string, string][] = querySelectorAll($, getQuery(12));
        const verifiedLink: [string, string][] = querySelectorAll($, getQuery(13));
        const emailHosting: [string, string][] = querySelectorAll($, getQuery(14));
        const nameServer: [string, string][] = querySelectorAll($, getQuery(15));
        const webHosting: [string, string][] = querySelectorAll($, getQuery(16));
        const sslCertificates: [string, string][] = querySelectorAll($, getQuery(17));
        const webServers: [string, string][] = querySelectorAll($, getQuery(18));
        const syndicationTechniques: [string, string][] = querySelectorAll($, getQuery(19));
        const awaitedArray = [
            trackingTech,
            widgets,
            languages,
            eCommerces,
            frameworks,
            cdn,
            mobile,
            payments,
            medias,
            cms,
            jsFrameworks,
            advertising,
            verifiedLink,
            emailHosting,
            nameServer,
            webHosting,
            sslCertificates,
            webServers,
            syndicationTechniques,
        ].map(async (service) => Promise.all(service.map(async (x) => getServiceSite(x, services))));
        await Promise.all(awaitedArray);
    } catch (error) {
        console.log(error);
    }
    return services;
};

export class BuiltWith {
    public static async query(domains: Domain[]) {
        const items = await Promise.all(
            domains.slice(0, 1).map(async (x) => {
                const response = await targetAnalyze(x.site);
                console.log(response);
                return { site: x, analytics: response };
            }),
        );
        return Linq.Unique(items, "site");
    }

    save(entity: IBuiltWith[]): Promise<IBuiltWith[]> {
        throw new Error("Method not implemented.");
    }

    enableFeature(): boolean {
        return true;
    }
}
