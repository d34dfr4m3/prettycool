import Service from "./service";
import Hermes from "hermes-http";
const hermes = new Hermes();

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
    const response = await hermes.get<string>(href);
    const $ = cheerio.load(response.data);
    $(
        "#mainForm > div.container > div > div.col-lg-8 > div:nth-child(4) > div > div:nth-child(1) > div.col-9.col-md-10 > p.xsmall.mb-2 > a",
    ).map((_, e) => {
        const el = $(e);
        services.push({ site: el.attr("href")!, title });
    });
};

export class BuiltWithService extends Service<IBuiltWith[]> {
    public async query(): Promise<IBuiltWith[]> {
        const response = await hermes.get<string>(`https://builtwith.com/${this.target.domain}`);
        const $ = cheerio.load(response.data);
        const trackingTech: [string, string][] = querySelectorAll($, getQuery(1));
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
        const services: IBuiltWith[] = [];
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
        return services;
    }

    save(entity: IBuiltWith[]): Promise<IBuiltWith[]> {
        throw new Error("Method not implemented.");
    }

    enableFeature(): boolean {
        return true;
    }
}
