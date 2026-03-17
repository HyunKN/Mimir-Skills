#!/usr/bin/env node
"use strict";

const { spawnSync } = require("child_process");
const path = require("path");

const PACKAGE_ROOT = path.resolve(__dirname, "..");

function findPython() {
  for (const cmd of ["python3", "python"]) {
    const result = spawnSync(cmd, ["--version"], { stdio: "ignore" });
    if (result.status === 0) return cmd;
  }
  return null;
}

const python = findPython();
if (!python) {
  console.error(
    "Error: Python 3 is required but not found in PATH.\n" +
      "Install Python 3.10+ from https://www.python.org/ and try again."
  );
  process.exit(1);
}

const args = ["-m", "mimir_skills", ...process.argv.slice(2)];
const result = spawnSync(python, args, {
  stdio: "inherit",
  cwd: PACKAGE_ROOT,
  env: {
    ...process.env,
    PYTHONPATH:
      PACKAGE_ROOT +
      (process.env.PYTHONPATH
        ? path.delimiter + process.env.PYTHONPATH
        : ""),
  },
});

process.exit(result.status ?? 1);
