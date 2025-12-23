const fs = require("fs");
const PyTestGenerator = require("./generators/PyTestGenerator");
const CypressTestGenerator = require("./generators/CypressTestGenerator");

class CompilerTestGenPlugin {
  constructor(options = {}) {
    this.outputDir = options.outputDir || "generated-tests";

    this.generators = [
      new PyTestGenerator(this.outputDir),
      new CypressTestGenerator(this.outputDir)
    ];
  }

  run(filePath) {
    if (!filePath) {
      throw new Error("No file path provided");
    }

    if (!fs.existsSync(filePath)) {
      throw new Error(`File not found: ${filePath}`);
    }

    const generator = this.generators.find(g =>
      g.supports(filePath)
    );

    if (!generator) {
      throw new Error(`Unsupported file type: ${filePath}`);
    }

    generator.generate(filePath);
  }
}

module.exports = CompilerTestGenPlugin;
