import { Command } from "commander";
//@ts-ignore
import { version } from "../package.json";
import { HunterService } from "./services/hunter.service";
import Target from "./services/target";

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
    const hunter = new HunterService(target);
    const dataHunter = await hunter.query();
    hunter.save(dataHunter);
});
