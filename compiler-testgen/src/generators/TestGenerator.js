const fs = require("fs");
const path = require("path");

class TestGenerator {
  constructor(outputDir) {
    this.outputDir = outputDir;
  }

  supports(filePath) {
    throw new Error("supports() not implemented");
  }

  generate(filePath) {
    throw new Error("generate() not implemented");
  }

  writeFile(relativePath, content) {
    const targetPath = path.join(this.outputDir, relativePath);
    fs.mkdirSync(path.dirname(targetPath), { recursive: true });
    fs.writeFileSync(targetPath, content, "utf8");
    console.log("WROTE:", targetPath);
  }
}

module.exports = TestGenerator;
