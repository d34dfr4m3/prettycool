# Migration `20200614120146-init`

This migration has been generated by g4rcez at 6/14/2020, 12:01:46 PM.
You can check out the [state of the schema](./schema.prisma) after the migration.

## Database Steps

```sql
CREATE TABLE "public"."service" (
"id" text  NOT NULL ,"protocol_id" text  NOT NULL ,"server_id" text  NOT NULL ,"target_id" text   ,"url" text  NOT NULL ,
    PRIMARY KEY ("id"))

CREATE TABLE "public"."tech" (
"id" text  NOT NULL ,"serviceId" text   ,"tech" text  NOT NULL ,"tech_url" text  NOT NULL ,
    PRIMARY KEY ("id"))

CREATE UNIQUE INDEX "service.url" ON "public"."service"("url")

ALTER TABLE "public"."service" ADD FOREIGN KEY ("protocol_id")REFERENCES "public"."protocol"("id") ON DELETE CASCADE  ON UPDATE CASCADE

ALTER TABLE "public"."service" ADD FOREIGN KEY ("server_id")REFERENCES "public"."server"("id") ON DELETE CASCADE  ON UPDATE CASCADE

ALTER TABLE "public"."service" ADD FOREIGN KEY ("target_id")REFERENCES "public"."target"("id") ON DELETE SET NULL  ON UPDATE CASCADE

ALTER TABLE "public"."tech" ADD FOREIGN KEY ("serviceId")REFERENCES "public"."service"("id") ON DELETE SET NULL  ON UPDATE CASCADE
```

## Changes

```diff
diff --git schema.prisma schema.prisma
migration 20200611210611-init..20200614120146-init
--- datamodel.dml
+++ datamodel.dml
@@ -2,9 +2,9 @@
 // learn more about it in the docs: https://pris.ly/d/prisma-schema
 datasource db {
   provider = "postgresql"
-  url = "***"
+  url      = "postgresql://postgres:12345@localhost:5432/prettycool?schema=public"
 }
 generator client {
   provider = "prisma-client-js"
@@ -16,8 +16,9 @@
   domain        String          @unique
   company_email company_email[]
   protocol      protocol[]
   server        server[]
+  service       service[]
 }
 model company_email {
   id          String @default(uuid()) @id
@@ -27,15 +28,16 @@
   target_id   String
 }
 model protocol {
-  id           String  @default(uuid()) @id
+  id           String    @default(uuid()) @id
   service_name String
   port         Int
   server_id    String
-  server       server  @relation(fields: [server_id], references: [id])
-  target       target? @relation(fields: [target_id], references: [id])
+  server       server    @relation(fields: [server_id], references: [id])
+  target       target?   @relation(fields: [target_id], references: [id])
   target_id    String?
+  service      service[]
 }
 model server {
   id          String     @default(uuid()) @id
@@ -45,8 +47,9 @@
   target      target     @relation(fields: [target_id], references: [id])
   target_id   String
   protocols   protocol[]
   location    location   @relation(fields: [location_id], references: [id])
+  service     service[]
 }
 model location {
   id           String   @default(uuid()) @id
@@ -59,4 +62,24 @@
   continent    String
   country_code String
   server       server[]
 }
+
+model service {
+  id          String   @default(uuid()) @id
+  url         String   @unique
+  protocol    protocol @relation(fields: [protocol_id], references: [id])
+  protocol_id String
+  server_id   String
+  server      server   @relation(fields: [server_id], references: [id])
+  target      target?  @relation(fields: [target_id], references: [id])
+  target_id   String?
+  techs       tech[]
+}
+
+model tech {
+  id        String   @default(uuid()) @id
+  tech      String
+  tech_url  String
+  service   service? @relation(fields: [serviceId], references: [id])
+  serviceId String?
+}
```

