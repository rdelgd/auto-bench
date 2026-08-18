import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

test("active package metadata and README use the Lasm identity", async () => {
  const packageJson = JSON.parse(await readFile(new URL("../../package.json", import.meta.url), "utf8")) as {
    readonly name?: string;
    readonly description?: string;
  };
  const readme = await readFile(new URL("../../README.md", import.meta.url), "utf8");

  assert.equal(packageJson.name, "@lasm/core");
  assert.match(packageJson.description ?? "", /operational meaning/);
  assert.match(readme, /from "@lasm\/core"/);
  assert.doesNotMatch(readme, /Nuveris Core|@nuveris\/core/);
});
