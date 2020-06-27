import { Command } from "commander";
//@ts-ignore
import { version } from "../package.json";
import { CensysIpv4Service } from "./services/censys.service";
import { CrtShService } from "./services/crtsh.service";
import { HunterService } from "./services/hunter.service";
import Target from "./services/target";
import cheerio from "cheerio";
import Hermes from "hermes-http";
import { TargetInfo } from "./domain/target-info";
import { BuiltWith } from "./workers/builtwith.service";
import { Domain } from "./domain/domain";
const prettyCool = new Command();

prettyCool
    .version(version)
    .option("-c, --company <company>", "Define company name")
    .option("-d, --domain <domain>", "Define domain of company")
    .allowUnknownOption(false);

prettyCool.parse(process.argv);

if (!prettyCool.domain || !prettyCool.company) {
    prettyCool.help();
    process.exit(1);
}

const target = new Target(prettyCool.domain, prettyCool.company);

target.save().then(async () => {
    // const hunter = new HunterService(target);
    // const dataHunter = await hunter.query();
    // hunter.save(dataHunter);
    // const censysIp = new CensysIpv4Service(target);
    // const censysData = await censysIp.query();
    // await censysIp.save(censysData);
    console.time("Init");
    const crt = new CrtShService(target);
    const data = await crt.query();
    const domains = data.map((x) => new Domain(target, x));
    const built = await BuiltWith.query(domains);
    console.timeEnd("Init");
});
