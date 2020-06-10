import axios from "axios";
require("dotenv").config();

export const http = axios.create({
  timeout: 40000,
  httpAgent: "prettycool",
});
