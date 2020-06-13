export const censysProtocol = (s: string): [number, string] => {
    const [port, service] = s.split("/");
    return [Number.parseInt(port, 10), service];
};

export const idProtocol = (port: number | string, service: string, ip: string) => `${port}/${service}-${ip}`;
