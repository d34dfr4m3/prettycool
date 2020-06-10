# Migration `20200607135754-init`

This migration has been generated by g4rcez at 6/7/2020, 1:57:54 PM.
You can check out the [state of the schema](./schema.prisma) after the migration.

## Database Steps

```sql
CREATE TABLE "public"."Target" (
"companyName" text  NOT NULL ,"domain" text  NOT NULL ,"id" text  NOT NULL ,
    PRIMARY KEY ("id"))

CREATE TABLE "public"."CompanyEmail" (
"email" text  NOT NULL ,"id" text  NOT NULL ,"serviceUrl" text  NOT NULL ,"targetId" text  NOT NULL ,
    PRIMARY KEY ("id"))

CREATE UNIQUE INDEX "CompanyEmail.serviceUrl" ON "public"."CompanyEmail"("serviceUrl")

ALTER TABLE "public"."CompanyEmail" ADD FOREIGN KEY ("targetId")REFERENCES "public"."Target"("id") ON DELETE CASCADE  ON UPDATE CASCADE
```

## Changes

```diff
diff --git schema.prisma schema.prisma
migration ..20200607135754-init
--- datamodel.dml
+++ datamodel.dml
@@ -1,0 +1,27 @@
+// This is your Prisma schema file,
+// learn more about it in the docs: https://pris.ly/d/prisma-schema
+
+datasource db {
+  provider = "postgresql"
+  url      = "postgresql://postgres:12345@localhost:5432/prettycool?schema=public"
+}
+
+generator client {
+  provider = "prisma-client-js"
+}
+
+model Target {
+  id           String         @default(uuid()) @id
+  companyName  String
+  domain       String
+  CompanyEmail CompanyEmail[]
+}
+
+model CompanyEmail {
+  id         String @default(uuid()) @id
+  email      String
+  serviceUrl String @unique
+
+  target   Target @relation(fields: [targetId], references: [id])
+  targetId String
+}
```

