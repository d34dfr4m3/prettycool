# prettycool

A fucking pretty cool tool for enumerate and discover information's about your target

### Development

You need install:

- docker
- docker-compose
- node (I recommend [nvm](https://github.com/nvm-sh/nvm))

After install, let's go to configure our setup:

```bash
npm i -g ts-node
yarn
yarn migrate
docker-compose up -d
ts-node src --domain target.com --company "Ecorp"
```

For now, only database is ported to docker. In the future, all dependencies will be migrated to docker.

### Feature

- [x] Hunter Scan
- [x] Censys Scan
- [ ] CLI Logging
- [ ] Domain Scan
- [ ] Enumerate server services/protocols
- [ ] Graphql hook using [graphql-hook](https://github.com/g4rcez/graphql-hook)
- [ ] Print domain pages
- [ ] Telegram notifications
- [ ] Web interface for monitoring
- [ ] Web tech discovery
- [ ] Whois information


### ToDo

- [ ] Express server
- [ ] WebPage
- [ ] Integrate graphql hook with express server
- [ ] Configure monorepo 
- [ ] Port dependencies to docker